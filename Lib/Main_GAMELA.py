import netCDF4
import numpy as np
import os
from datetime import datetime, timedelta, timezone
from astral import LocationInfo
from astral.sun import sun
from colorama import init, Fore, Style
from funciones_auxiliares import *

# Inicializar colorama
init(autoreset=True)

# URLs de los datasets
URL_GFS = "https://tds.scigw.unidata.ucar.edu/thredds/dodsC/grib/NCEP/GFS/Global_0p5deg/Best"
URL_WAVE = "https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/WW3/Global/Best"
URL_HYCOM = "https://tds.hycom.org/thredds/dodsC/FMRC_ESPC-D-V02_uv3z/FMRC_ESPC-D-V02_uv3z_best.ncd"

def Main_automatico(debug_mode):
    # Solicitar coordenadas al usuario
    print("\nModo de operación automático.\n")
    print("Información geográfica de la zona de operaciones.\n")
    lat_usuario = float(input("Introduzca la latitud (grados decimales, -90..90): "))
    lon_usuario = float(input("Introduzca la longitud (grados decimales, -180..180): "))

    # Conversión para HYCOM: se usan longitudes de 0 a 360
    lon_wave = lon_usuario if lon_usuario >= 0 else 360 + lon_usuario

    hoy = datetime.utcnow().date()
    manana = hoy + timedelta(days=1)
    forecast_horas = [0, 6, 12, 18]
    target_times = [
        datetime(manana.year, manana.month, manana.day, hora, 0, 0, tzinfo=timezone.utc)
        for hora in forecast_horas
    ]

    #Dataset GFS
    print("Descargando datos de GFS...")
    with netCDF4.Dataset(URL_GFS) as ds_gfs:
        time_var = ds_gfs.variables["time"]
        py_times_gfs = netCDF4.num2date(time_var[:], units=time_var.units,
                                        calendar=getattr(time_var, "calendar", "standard"))
        lat_gfs = ds_gfs.variables["lat"][:]
        lon_gfs = ds_gfs.variables["lon"][:]
        i_lat_gfs = obtener_indice_cercano(lat_gfs, lat_usuario)
        i_lon_gfs = obtener_indice_cercano(lon_gfs, lon_usuario if lon_usuario >= 0 else 360 + lon_usuario)
        height_levels = ds_gfs.variables["height_above_ground"][:]
        i_altura_viento = obtener_indice_cercano(height_levels, 10)
        u_gfs = ds_gfs.variables["u-component_of_wind_height_above_ground"]
        v_gfs = ds_gfs.variables["v-component_of_wind_height_above_ground"]
        rain_gfs = ds_gfs.variables.get("Total_precipitation_surface_Mixed_intervals_Accumulation", None)
        ceiling_gfs = ds_gfs.variables.get("Geopotential_height_cloud_ceiling", None)
        temperature_gfs = ds_gfs.variables.get("Temperature_surface", None)

        #Dataset WW3 para olas
        print("Descargando datos de WW3...")
        with netCDF4.Dataset(URL_WAVE) as ds_wave:
            time_wave = ds_wave.variables["time"]
            py_times_wave = netCDF4.num2date(time_wave[:], units=time_wave.units,
                                             calendar=getattr(time_wave, "calendar", "standard"))
            lat_wave = ds_wave.variables["lat"][:]
            lon_wave_arr = ds_wave.variables["lon"][:]
            i_lat_wave = obtener_indice_cercano(lat_wave, lat_usuario)
            i_lon_wave = obtener_indice_cercano(lon_wave_arr, lon_wave)
            wave_var = ds_wave.variables.get("Significant_height_of_combined_wind_waves_and_swell_surface",
                                             ds_wave.variables.get("Significant_height_of_waves", None))

            #Dataset HYCOM para la corriente
            print("Descargando datos de HYCOM...")
            with netCDF4.Dataset(URL_HYCOM) as ds_hycom:
                time_hycom = ds_hycom.variables["time"]
                py_times_hycom = netCDF4.num2date(time_hycom[:], units=time_hycom.units,
                                                 calendar=getattr(time_hycom, "calendar", "standard"))
                lat_hycom = ds_hycom.variables["lat"][:]
                lon_hycom = ds_hycom.variables["lon"][:]
                i_lat_hycom = obtener_indice_cercano(lat_hycom, lat_usuario)
                i_lon_hycom = obtener_indice_cercano(lon_hycom, lon_wave)
                try:
                    u_current = ds_hycom.variables["water_u"]
                except KeyError:
                    raise KeyError("La variable 'water_u' no se encontró en el dataset HYCOM.")
                try:
                    v_current = ds_hycom.variables["water_v"]
                except KeyError:
                    raise KeyError("La variable 'water_v' no se encontró en el dataset HYCOM.")

                #Ocaso para mañana
                ubicacion = LocationInfo(name="Local", region="Local", timezone="UTC",
                                         latitude=lat_usuario, longitude=lon_usuario)
                s = sun(ubicacion.observer, date=manana, tzinfo=timezone.utc)
                ocaso = s["sunset"]

                #Escritura de la previsión en un archivo de texto
                with open("prevision.txt", "w", encoding="utf-8") as f:
                    f.write(f"Coordenadas: latitud = {lat_usuario}, longitud = {lon_usuario}\n")
                    f.write(f"Hora del ocaso: {ocaso.strftime('%H:%M UTC')}\n\n")
                    olas_list = []
                    lluvia_list = []

                    for t_target in target_times:
                        t_objetivo = t_target.replace(tzinfo=None)
                        #GFS: obtener índice de tiempo más cercano
                        i_t_gfs = obtener_indice_tiempo(py_times_gfs, t_objetivo)
                        u_val = u_gfs[i_t_gfs, i_altura_viento, i_lat_gfs, i_lon_gfs]
                        v_val = v_gfs[i_t_gfs, i_altura_viento, i_lat_gfs, i_lon_gfs]
                        velocidad_viento = np.sqrt(u_val**2 + v_val**2)

                        temperatura = temperature_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs] if temperature_gfs is not None else 0.0
                        temperatura -= 273.15  

                        cantidad_lluvia = rain_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs] if rain_gfs is not None else 0.0
                        lluvia = "sí" if cantidad_lluvia > 0 else "no"
                        techo_nubes = ceiling_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs] if ceiling_gfs is not None else 1000.0

                        estado = "Día" if t_objetivo < ocaso.replace(tzinfo=None) else "Noche"
                        altura_ola = obtener_altura_ola(t_objetivo, py_times_wave, wave_var, i_lat_wave, i_lon_wave)
                        olas_list.append(altura_ola)
                        lluvia_list.append(lluvia)

                        #HYCOM: obtener velocidad de la corriente
                        diffs_hycom = np.array([abs((t - t_objetivo).total_seconds()) for t in py_times_hycom])
                        indices_ordenados = np.argsort(diffs_hycom)
                        velocidad_corriente = 0.0
                        for idx in indices_ordenados:
                            try:
                                if len(u_current.shape) == 4:
                                    corriente_u = u_current[idx, 1, i_lat_hycom, i_lon_hycom]
                                    corriente_v = v_current[idx, 1, i_lat_hycom, i_lon_hycom]
                                else:
                                    corriente_u = u_current[idx, i_lat_hycom, i_lon_hycom]
                                    corriente_v = v_current[idx, i_lat_hycom, i_lon_hycom]
                                velocidad_corriente = np.sqrt(corriente_u**2 + corriente_v**2)
                                break
                            except Exception:
                                continue

                        # Determinar color de lluvia
                        color_lluvia_asuw = Fore.GREEN if lluvia == "no" else Fore.YELLOW

                        #Escribir los resultados en el archivo
                        f.write(f"Previsión para {t_target.date()} a las {t_target.hour} UTC:\n")
                        f.write(f"  Viento: {velocidad_viento:.2f} m/s\n")
                        f.write(f"  Olas: {altura_ola:.2f} m\n")
                        f.write(f"  Corriente: {velocidad_corriente:.2f} m/s\n")
                        f.write(f"  Lluvia: {color_lluvia_asuw}{lluvia}{Style.RESET_ALL}\n")
                        f.write(f"  Temperatura: {temperatura:.2f} °C\n")
                        f.write(f"  Techo de nubes: {techo_nubes:.2f} m\n")
                        f.write(f"  Estado: {estado}\n\n")
            colores_mar_asuw, colores_mar_asw, colores_lluvia = comparar_valores(olas_list, lluvia_list)
            print("La previsión se ha guardado en prevision.txt") 

#Modo manual
def Main_manual(debug_mode):
    
    print("\nModo de operación manual.\n")
    print("Información geográfica de la zona de operaciones.\n")
    lat_usuario = float(input("Introduzca la latitud (grados decimales, -90..90): "))
    lon_usuario = float(input("Introduzca la longitud (grados decimales, -180..180): "))

    hoy = datetime.utcnow().date()
    manana = hoy + timedelta(days=1)
    forecast_horas = [0, 6, 12, 18]
    target_times = [
        datetime(manana.year, manana.month, manana.day, hora, 0, 0, tzinfo=timezone.utc)
        for hora in forecast_horas
    ]

    # Cálculo del ocaso para mañana usando Astral
    ubicacion = LocationInfo(name="Local", region="Local", timezone="UTC",
                             latitude=lat_usuario, longitude=lon_usuario)
    s = sun(ubicacion.observer, date=manana, tzinfo=timezone.utc)
    ocaso = s["sunset"]

    # Recoger datos manualmente para cada horario
    datos_prevision = []
    for t in target_times:
        os.system("clear")
        print(Style.BRIGHT + Fore.GREEN + f"Datos para las {t.hour:02d}:00" + Style.RESET_ALL)
        viento = float(input("Introduzca la velocidad del viento (m/s): "))
        ola = float(input("Introduzca la altura de la ola (m): "))
        corriente = float(input("Introduzca la velocidad de la corriente (m/s): "))
        lluvia = input("¿Lluvia? (S/N): ")
        lluvia = "sí" if lluvia.lower() == "s" else "no"
        temp = float(input("Introduzca la temperatura (°C): "))
        techo = float(input("Introduzca el techo de nubes (m): "))
        estado = input("Estado (Día/Noche): ")
        datos_prevision.append({
            "hora": t,
            "viento": viento,
            "ola": ola,
            "corriente": corriente,
            "lluvia": lluvia,
            "temperatura": temp,
            "techo": techo,
            "estado": estado
        })

    # Escribir los resultados en el archivo prevision.txt
    with open("prevision.txt", "w", encoding="utf-8") as f:
        f.write(f"Coordenadas: latitud = {lat_usuario}, longitud = {lon_usuario}\n")
        f.write(f"Hora del ocaso: {ocaso.strftime('%H:%M UTC')}\n\n")
        olas_list = []
        lluvia_list = []
        for datos in datos_prevision:
            t = datos["hora"]
            olas_list.append(datos["ola"])
            lluvia_list.append(datos["lluvia"])
            color_lluvia_asuw = Fore.GREEN if datos["lluvia"] == "no" else Fore.YELLOW
            f.write(f"Previsión para {t.date()} a las {t.hour} UTC:\n")
            f.write(f"Viento: {datos['viento']:.2f} m/s\n")
            f.write(f"Olas: {datos['ola']:.2f} m\n")
            f.write(f"Corriente: {datos['corriente']:.2f} m/s\n")
            f.write(f"Lluvia: {color_lluvia_asuw}{datos['lluvia']}{Style.RESET_ALL}\n")
            f.write(f"Temperatura: {datos['temperatura']:.2f} °C\n")
            f.write(f"Techo de nubes: {datos['techo']:.2f} m\n")
            f.write(f"Estado: {datos['estado']}\n\n")

    colores_mar_asuw, colores_mar_asw, colores_lluvia = comparar_valores(olas_list, lluvia_list)
    print("La previsión se ha guardado en prevision.txt")
