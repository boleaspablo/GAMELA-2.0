import netCDF4
import numpy as np
import os,sys
from datetime import datetime, timedelta, timezone

from astral import LocationInfo
from astral.sun import sun
from colorama import init, Fore, Style
from funciones_auxiliares import *

from datetime import datetime,timezone


ahora = datetime.now(timezone.utc)
Ano_Ej    = str(ahora.year).zfill(4)
Mes_Ej    = str(ahora.month).zfill(2)
Dia_Ej    = str(ahora.day).zfill(2)
Hora_Ej   = str(ahora.hour).zfill(2)
Minuto_Ej = str(ahora.minute).zfill(2) 

Hora_ejecucion = "%s%s%s_%s%s (UTC)"%(Ano_Ej,Mes_Ej,Dia_Ej,Hora_Ej,Minuto_Ej)


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

    area = definir_area(lat_usuario, lon_usuario)
    urls = construir_URL(area, Ano_Ej, Mes_Ej, Dia_Ej)

    # Conversión para HYCOM: se usan longitudes de 0 a 360
    lon_wave = lon_usuario if lon_usuario >= 0 else 360 + lon_usuario

    hoy = datetime.utcnow().date()
    manana = hoy + timedelta(days=1)
    forecast_horas = [6, 12, 18, 0, 6]
    target_times = [
        datetime(hoy.year, hoy.month, hoy.day, hora, 0, 0, tzinfo=timezone.utc) if hora != 0 else datetime(manana.year, manana.month, manana.day, hora, 0, 0, tzinfo=timezone.utc)
        for hora in forecast_horas
    ]

    # Cálculo del amanecer y ocaso
    ubicacion = LocationInfo(name="Local", region="Local", timezone="UTC",
                             latitude=lat_usuario, longitude=lon_usuario)
    s = sun(ubicacion.observer, date=hoy, tzinfo=timezone.utc)
    ocaso = s["sunset"]
    amanecer = s["sunrise"]

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
        rain_gfs = ds_gfs.variables.get("Precipitation_rate_surface_Mixed_intervals_Average", None)
        ceiling_gfs = ds_gfs.variables.get("Geopotential_height_cloud_ceiling", None)
        temperature_gfs = ds_gfs.variables.get("Temperature_surface", None)
        visibility_gfs = ds_gfs.variables.get("Visibility_surface", None)

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

                #Escritura de la previsión en un archivo de texto
                with open("../Output/prevision.tex", "w", encoding="utf-8") as f:
                    f.write(rf"""{{\bf Fecha y hora del informe:}} {Dia_Ej}/{Mes_Ej}/{Ano_Ej} a las {Hora_Ej} : {Minuto_Ej} UTC\\""")
                    f.write(f"\n")
                    f.write(rf"""Coordenadas: latitud = {lat_usuario}, longitud = {lon_usuario}\\""")
                    f.write(f"\n")
                    f.write(rf"""Orto: {amanecer.strftime('%H:%M UTC')} \, -- \, Ocaso: {ocaso.strftime('%H:%M UTC')}""")
                    f.write(f"\n\n")
                    olas_list = []
                    lluvia_list = []
                    viento_list = []
                    visibilidad_list = []
                    nocturnidad_list = []
                    temperatura_list = []
                    cantidad_lluvia_list = []
                    techo_list = []

                    for t_target in target_times:
                        t_objetivo = t_target.replace(tzinfo=None)

                        estado = "Día" if amanecer.replace(tzinfo=None) <= t_objetivo < ocaso.replace(tzinfo=None) else "Noche"
                        
                        #GFS: obtener índice de tiempo más cercano
                        i_t_gfs = obtener_indice_tiempo(py_times_gfs, t_objetivo)
                        u_val = u_gfs[i_t_gfs, i_altura_viento, i_lat_gfs, i_lon_gfs]
                        v_val = v_gfs[i_t_gfs, i_altura_viento, i_lat_gfs, i_lon_gfs]
                        velocidad_viento = np.sqrt(u_val**2 + v_val**2)
                        direccion_viento = (270 - np.arctan2(v_val, u_val) * 180 / np.pi) % 360


                        temperatura = temperature_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs] if temperature_gfs is not None else 0.0
                        temperatura -= 273.15  

                        cantidad_lluvia = (rain_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs])*3600 if rain_gfs is not None else 0.0
                        lluvia = "sí" if cantidad_lluvia > 0.0 else "no"
                        techo_nubes = ceiling_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs] if ceiling_gfs is not None else 1000.0
                        visibilidad = visibility_gfs[i_t_gfs, i_lat_gfs, i_lon_gfs] if visibility_gfs is not None else 20000.0

                        altura_ola = obtener_altura_ola(t_objetivo, py_times_wave, wave_var, i_lat_wave, i_lon_wave)
                        olas_list.append(altura_ola)
                        lluvia_list.append(lluvia)
                        viento_list.append(velocidad_viento)
                        visibilidad_list.append(visibilidad)
                        nocturnidad_list.append(estado)
                        temperatura_list.append(temperatura)
                        cantidad_lluvia_list.append(cantidad_lluvia)
                        techo_list.append(techo_nubes)

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


                        #Escribir los resultados en el archivo
                        f.write(rf"""{{\bf Previsión para {t_target.date()} a las {t_target.hour} UTC}}\\""")
                        f.write(f"\n")
                        f.write(rf"""  Viento: {velocidad_viento:.2f} m/s, {direccion_viento:.2f}$^\circ$\\""")
                        f.write(f"\n")
                        f.write(rf"""  Olas: {altura_ola:.2f} m\\""")
                        f.write(f"\n")
                        f.write(rf"""  Corriente: {velocidad_corriente:.2f} m/s\\""")
                        f.write(f"\n")
                        f.write(rf"""  Lluvia: {lluvia} ({cantidad_lluvia:.2f} mm/h)\\""")
                        f.write(f"\n")
                        f.write(rf"""  Temperatura: {temperatura:.2f} $^\circ$C\\""")
                        f.write(f"\n")
                        f.write(rf"""  Techo de nubes: {techo_nubes:.2f} m\\""")
                        f.write(f"\n")
                        f.write(rf"""  Visibilidad: {visibilidad:.2f} m\\""")
                        f.write(f"\n")
                        f.write(rf"""  Estado: {estado}""")
                        f.write(f"\n\n")
            colores_mar_asuw, colores_mar_asw, colores_lluvia, colores_mar_aaw, colores_viento_RASFAS, colores_mar_RASFAS, colores_visibilidad_RASFAS, colores_nocturnidad_RASFAS, colores_viento_RHIB, colores_mar_RHIB, colores_visibilidad_RHIB, colores_nocturnidad_RHIB, colores_mar_LND, colores_viento_SCAT, colores_mar_SCAT, colores_visibilidad_SCAT, colores_nocturnidad_SCAT, colores_temperatura_PERSONNEL, colores_lluvia_PERSONNEL, colores_mar_PERSONNEL, colores_lluvia_VEHICLES, colores_mar_STOVL, colores_viento_STOVL, colores_visibilidad_STOVL, colores_temperatura_STOVL, colores_techo_STOVL, colores_mar_HELO, colores_viento_HELO, colores_visibilidad_HELO, colores_techo_HELO = comparar_valores(olas_list, lluvia_list, viento_list, visibilidad_list, nocturnidad_list, temperatura_list, cantidad_lluvia_list, techo_list)
            print("Obteniendo mapas...") 

    for i, url in enumerate(urls):
        output_file = f"../Output/img_mapa_{i+1}.webp"
        result = extraer_mapas(url, output_file)
        if result:
            print(f"Imagen {i+1}: Imagen guardada en {result}")
        else:
            print("No se pudo guardar la imagen.")
    
    ruta_output = "../Output"
    
    convertir_a_png(ruta_output)

#Modo manual
def Main_manual(debug_mode):
    
    print("\nModo de operación manual.\n")
    print("Información geográfica de la zona de operaciones.\n")
    lat_usuario = float(input("Introduzca la latitud (grados decimales, -90..90): "))
    lon_usuario = float(input("Introduzca la longitud (grados decimales, -180..180): "))

    hoy = datetime.utcnow().date()
    manana = hoy + timedelta(days=1)
    forecast_horas = [6, 12, 18, 0, 6]
    target_times = [
        datetime(hoy.year, hoy.month, hoy.day, hora, 0, 0, tzinfo=timezone.utc) if hora != 0 else datetime(manana.year, manana.month, manana.day, hora, 0, 0, tzinfo=timezone.utc)
        for hora in forecast_horas
    ]

    # Cálculo del ocaso para mañana usando Astral
    ubicacion = LocationInfo(name="Local", region="Local", timezone="UTC",
                             latitude=lat_usuario, longitude=lon_usuario)
    s = sun(ubicacion.observer, date=manana, tzinfo=timezone.utc)
    ocaso = s["sunset"]
    amanecer = s["sunrise"]

    # Recoger datos manualmente para cada horario
    datos_prevision = []
    for t in target_times:
        os.system("clear")
        print(Style.BRIGHT + Fore.GREEN + f"Datos para las {t.hour:02d}:00" + Style.RESET_ALL)
        viento = float(input("Introduzca la velocidad del viento (m/s): "))
        direccion = float(input("Introduzca la dirección del viento (º): "))
        ola = float(input("Introduzca la altura de la ola (m): "))
        corriente = float(input("Introduzca la velocidad de la corriente (m/s): "))
        lluvia = input("¿Lluvia? (S/N): ")
        lluvia = "sí" if lluvia.lower() == "s" else "no"
        cantidad_lluvia = float(input("Introduzca la cantidad de lluvia (mm/h): ")) if lluvia == "sí" else 0.0
        temp = float(input("Introduzca la temperatura (°C): "))
        techo = float(input("Introduzca el techo de nubes (m): "))
        visibilidad = float(input("Introduzca la visibilidad (m): "))
        estado = input("Estado (Día/Noche): ")
        datos_prevision.append({
            "hora": t,
            "viento": viento,
            "direccion": direccion,
            "ola": ola,
            "corriente": corriente,
            "lluvia": lluvia,
            "cantidad_lluvia": cantidad_lluvia,
            "temperatura": temp,
            "techo": techo,
            "visibilidad": visibilidad,
            "estado": estado
        })

    # Escribir los resultados en el archivo prevision.tex
    with open("../Output/prevision.tex", "w", encoding="utf-8") as f:
        f.write(rf"""{{\bf Fecha y hora del informe:}} {Dia_Ej}/{Mes_Ej}/{Ano_Ej} a las {Hora_Ej} : {Minuto_Ej} UTC\\""")
        f.write(f"\n")
        f.write(rf"""Coordenadas: latitud = {lat_usuario}, longitud = {lon_usuario}\\""")
        f.write(f"\n")
        f.write(rf"""Orto: {amanecer.strftime('%H:%M UTC')} \, -- \, Ocaso: {ocaso.strftime('%H:%M UTC')}""")
        f.write(f"\n\n")
        olas_list = []
        lluvia_list = []
        viento_list = []
        visibilidad_list = []
        nocturnidad_list = []
        temperatura_list = []
        cantidad_lluvia_list = []
        techo_list = []
        for datos in datos_prevision:
            t = datos["hora"]
            olas_list.append(datos["ola"])
            lluvia_list.append(datos["lluvia"])
            viento_list.append(datos["viento"])
            visibilidad_list.append(datos["visibilidad"])
            nocturnidad_list.append(datos["estado"])
            temperatura_list.append(datos["temperatura"])
            cantidad_lluvia_list.append(datos["cantidad_lluvia"])
            techo_list.append(datos["techo"])
            f.write(rf"""{{\bf Previsión para {t.date()} a las {t.hour} UTC}}\\""")
            f.write(f"\n")
            f.write(rf"""  Viento: {datos['viento']:.2f} m/s, {datos['direccion']:.2f}$^\circ$\\""")
            f.write(f"\n")
            f.write(rf"""  Olas: {datos['ola']:.2f} m\\""")
            f.write(f"\n")
            f.write(rf"""  Corriente: {datos['corriente']:.2f} m/s\\""")
            f.write(f"\n")
            f.write(rf"""  Lluvia: {datos['lluvia']} ({datos['cantidad_lluvia']:.2f} mm/h)\\""")
            f.write(f"\n")
            f.write(rf"""  Temperatura: {datos['temperatura']:.2f} $^\circ$C\\""")
            f.write(f"\n")
            f.write(rf"""  Techo de nubes: {datos['techo']:.2f} m\\""")
            f.write(f"\n")
            f.write(rf"""  Visibilidad: {datos['visibilidad']:.2f} m\\""")
            f.write(f"\n")
            f.write(rf"""  Estado: {datos['estado']}""")
            f.write(f"\n\n")

    colores_mar_asuw, colores_mar_asw, colores_lluvia, colores_mar_aaw, colores_viento_RASFAS, colores_mar_RASFAS, colores_visibilidad_RASFAS, colores_nocturnidad_RASFAS, colores_viento_RHIB, colores_mar_RHIB, colores_visibilidad_RHIB, colores_nocturnidad_RHIB, colores_mar_LND, colores_viento_SCAT, colores_mar_SCAT, colores_visibilidad_SCAT, colores_nocturnidad_SCAT, colores_temperatura_PERSONNEL, colores_lluvia_PERSONNEL, colores_mar_PERSONNEL, colores_lluvia_VEHICLES, colores_mar_STOVL, colores_viento_STOVL, colores_visibilidad_STOVL, colores_temperatura_STOVL, colores_techo_STOVL, colores_mar_HELO, colores_viento_HELO, colores_visibilidad_HELO, colores_techo_HELO = comparar_valores(olas_list, lluvia_list, viento_list, visibilidad_list, nocturnidad_list, temperatura_list, cantidad_lluvia_list, techo_list)
    print("La previsión se ha guardado en Output/prevision.tex")
