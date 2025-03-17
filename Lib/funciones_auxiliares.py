import numpy as np

#obtener índices cercanos
def obtener_indice_cercano(valores, objetivo):
    return int(np.argmin(np.abs(np.array(valores) - objetivo)))

#obtener índice de tiempo 
def obtener_indice_tiempo(py_times, t_objetivo):
    diffs = np.array([abs((t - t_objetivo).total_seconds()) for t in py_times])
    return int(np.argmin(diffs))

#obtener altura de la ola
def obtener_altura_ola(t_objetivo, py_times_wave, wave_var, indice_lat, indice_lon):
    if wave_var is None:
        return 0.0
    indice_tiempo = obtener_indice_tiempo(py_times_wave, t_objetivo)
    altura = wave_var[indice_tiempo, indice_lat, indice_lon]
    return float(altura) if not np.ma.is_masked(altura) else 0.0

#Comparar valores para obtener colores
def comparar_valores(olas_list, lluvia_list, viento_list, visibilidad_list, nocturnidad_list, temperatura_list, cantidad_lluvia_list, techo_list):
    horas = ["06a1", "12", "18", "00", "06a2"]
    colores_mar_asuw = {}
    colores_mar_asw = {}
    colores_lluvia = {}
    colores_mar_aaw = {}
    colores_viento_RASFAS = {}
    colores_mar_RASFAS = {}
    colores_visibilidad_RASFAS = {}
    colores_nocturnidad_RASFAS = {}
    colores_viento_RHIB = {}
    colores_mar_RHIB = {}
    colores_visibilidad_RHIB = {}
    colores_nocturnidad_RHIB = {}
    colores_mar_LND = {}
    colores_viento_SCAT = {}
    colores_mar_SCAT = {}
    colores_visibilidad_SCAT = {}
    colores_nocturnidad_SCAT = {}
    colores_temperatura_PERSONNEL = {}
    colores_lluvia_PERSONNEL = {}
    colores_mar_PERSONNEL = {}
    colores_lluvia_VEHICLES = {}
    colores_mar_STOVL = {}
    colores_viento_STOVL = {}
    colores_visibilidad_STOVL = {}
    colores_temperatura_STOVL = {}
    colores_techo_STOVL = {}
    colores_mar_HELO = {}
    colores_viento_HELO = {}
    colores_visibilidad_HELO = {}
    colores_techo_HELO = {}

    print("Comparando valores...")
    
    for i, altura in enumerate(olas_list):
        if altura < 2.5:
            color = "00E500"
        elif 2.5 <= altura <= 4:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_mar_asuw[f"color_mar_ASUW_{horas[i]}"] = color
        colores_mar_asw[f"color_mar_ASW_{horas[i]}"] = color
        colores_mar_PERSONNEL[f"color_mar_PERSONNEL_{horas[i]}"] = color
        colores_mar_HELO[f"color_mar_HELO_{horas[i]}"] = color

    for i, lluvia in enumerate(lluvia_list):
        color = "00E500" if lluvia == "no" else "FFFE25"
        colores_lluvia[f"color_lluvia_ASUW_{horas[i]}"] = color

    for i, altura in enumerate(olas_list):
        if altura < 4:
            color = "00E500"
        elif 4 <= altura <= 6:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_mar_aaw[f"color_mar_AAW_{horas[i]}"] = color

    for i, viento in enumerate(viento_list):
        if viento < 11:
            color = "00E500"
        elif 11 <= viento <= 17:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_viento_RASFAS[f"color_viento_RASFAS_{horas[i]}"] = color
        colores_viento_RHIB[f"color_viento_RHIB_{horas[i]}"] = color
        colores_viento_SCAT[f"color_viento_SCAT_{horas[i]}"] = color

    for i, altura in enumerate(olas_list):
        if altura < 1.25:
            color = "00E500"
        elif 1.25 <= altura <= 2.5:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_mar_RASFAS[f"color_mar_RASFAS_{horas[i]}"] = color

    for i, visibilidad in enumerate(visibilidad_list):
        if visibilidad > 5500:
            color = "00E500"
        elif 500 <= altura <= 5500:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_visibilidad_RASFAS[f"color_visibilidad_RASFAS_{horas[i]}"] = color
        colores_visibilidad_SCAT[f"color_visibilidad_SCAT_{horas[i]}"] = color

    for i, nocturnidad in enumerate(nocturnidad_list):
        color = "00E500" if nocturnidad == "Día" else "FFFE25"
        colores_nocturnidad_RASFAS[f"color_nocturnidad_RASFAS_{horas[i]}"] = color
        colores_nocturnidad_SCAT[f"color_nocturnidad_SCAT_{horas[i]}"] = color
        colores_nocturnidad_RHIB[f"color_nocturnidad_RHIB_{horas[i]}"] = color

    for i, altura in enumerate(olas_list):
        if altura < 1.25:
            color = "00E500"
        elif 1.25 <= altura <= 2.5:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_mar_RHIB[f"color_mar_RHIB_{horas[i]}"] = color
        colores_mar_SCAT[f"color_mar_SCAT_{horas[i]}"] = color

    for i, visibilidad in enumerate(visibilidad_list):
        if visibilidad > 5500:
            color = "00E500"
        elif 1800 <= visibilidad <= 5500:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_visibilidad_RHIB[f"color_visibilidad_RHIB_{horas[i]}"] = color
    
    for i, altura in enumerate(olas_list):
        if altura < 0.5:
            color = "00E500"
        elif 0.5 <= altura <= 1.25:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_mar_LND[f"color_mar_LND_{horas[i]}"] = color

    for i, temperatura in enumerate(temperatura_list):
        if 0 < temperatura < 30:
            color = "00E500"
        elif -4 <= temperatura <= 0:
            color = "FFFE25"
        elif 30 <= temperatura <= 35:
            color = "FFFE25"
        elif temperatura < -4:
            color = "FF0000"
        #elif temperatura > 50:
        #    color = "ERROR"
        else:
            color = "FF0000"
        colores_temperatura_PERSONNEL[f"color_temperatura_PERSONNEL_{horas[i]}"] = color

    for i, cantidad_lluvia in enumerate(cantidad_lluvia_list):
        if cantidad_lluvia < 2.5:
            color = "00E500"
        elif 2.5 <= cantidad_lluvia <= 10:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_lluvia_PERSONNEL[f"color_lluvia_PERSONNEL_{horas[i]}"] = color
        colores_lluvia_VEHICLES[f"color_lluvia_VEHICLES_{horas[i]}"] = color

    for i, altura in enumerate(olas_list):
        if altura < 2.5:
            color = "00E500"
        elif 2.5 <= altura <= 6:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_mar_STOVL[f"color_mar_STOVL_{horas[i]}"] = color

    for i, viento in enumerate(viento_list):
        if viento < 49:
            color = "00E500"
        elif 49 <= viento <= 68:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_viento_STOVL[f"color_viento_STOVL_{horas[i]}"] = color

    for i, visibilidad in enumerate(visibilidad_list):
        if visibilidad > 3500:
            color = "00E500"
        elif 1000 <= altura <= 3500:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_visibilidad_STOVL[f"color_visibilidad_STOVL_{horas[i]}"] = color

    for i, temperatura in enumerate(temperatura_list):
        if temperatura < 30:
            color = "00E500"
        elif 30 < temperatura < 35:
            color = "FF0000"
        else:
            color = "FF0000"
        colores_temperatura_STOVL[f"color_temperatura_STOVL_{horas[i]}"] = color

    for i, techo in enumerate(techo_list):
        if techo > 460:
            color = "00E500"
        elif 150 <= altura <= 460:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_techo_STOVL[f"color_techo_STOVL_{horas[i]}"] = color

    for i, viento in enumerate(viento_list):
        if viento < 40:
            color = "00E500"
        elif 40 <= viento <= 58:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_viento_HELO[f"color_viento_HELO_{horas[i]}"] = color

    for i, visibilidad in enumerate(visibilidad_list):
        if visibilidad > 4000:
            color = "00E500"
        elif 2000 <= altura <= 4000:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_visibilidad_HELO[f"color_visibilidad_HELO_{horas[i]}"] = color

    for i, techo in enumerate(techo_list):
        if techo > 915:
            color = "00E500"
        elif 150 <= altura <= 915:
            color = "FFFE25"
        else:
            color = "FF0000"
        colores_techo_HELO[f"color_techo_HELO_{horas[i]}"] = color
    
    escribir_matriz(colores_mar_HELO, colores_viento_HELO, colores_visibilidad_HELO, colores_techo_HELO, colores_mar_STOVL, colores_viento_STOVL, colores_visibilidad_STOVL, colores_techo_STOVL, colores_temperatura_STOVL, colores_lluvia_VEHICLES, colores_mar_PERSONNEL, colores_lluvia_PERSONNEL, colores_temperatura_PERSONNEL, colores_viento_SCAT, colores_mar_SCAT, colores_visibilidad_SCAT, colores_nocturnidad_SCAT, colores_mar_LND, colores_viento_RHIB, colores_mar_RHIB, colores_visibilidad_RHIB, colores_nocturnidad_RHIB, colores_viento_RASFAS, colores_mar_RASFAS, colores_visibilidad_RASFAS, colores_nocturnidad_RASFAS, colores_mar_aaw, colores_mar_asw, colores_mar_asuw, colores_lluvia)
    return colores_mar_asuw, colores_mar_asw, colores_lluvia, colores_mar_aaw, colores_viento_RASFAS, colores_mar_RASFAS, colores_visibilidad_RASFAS, colores_nocturnidad_RASFAS, colores_viento_RHIB, colores_mar_RHIB, colores_visibilidad_RHIB, colores_nocturnidad_RHIB, colores_mar_LND, colores_viento_SCAT, colores_mar_SCAT, colores_visibilidad_SCAT, colores_nocturnidad_SCAT, colores_temperatura_PERSONNEL, colores_lluvia_PERSONNEL, colores_mar_PERSONNEL, colores_lluvia_VEHICLES, colores_mar_STOVL, colores_viento_STOVL, colores_visibilidad_STOVL, colores_temperatura_STOVL, colores_techo_STOVL, colores_mar_HELO, colores_viento_HELO, colores_visibilidad_HELO, colores_techo_HELO

# Hallar los colores para cada operación
def escribir_matriz(colores_mar_HELO, colores_viento_HELO, colores_visibilidad_HELO, colores_techo_HELO, colores_mar_STOVL, colores_viento_STOVL, colores_visibilidad_STOVL, colores_techo_STOVL, colores_temperatura_STOVL, colores_lluvia_VEHICLES, colores_mar_PERSONNEL, colores_lluvia_PERSONNEL, colores_temperatura_PERSONNEL, colores_viento_SCAT, colores_mar_SCAT, colores_visibilidad_SCAT, colores_nocturnidad_SCAT, colores_mar_LND, colores_viento_RHIB, colores_mar_RHIB, colores_visibilidad_RHIB, colores_nocturnidad_RHIB, colores_viento_RASFAS, colores_mar_RASFAS, colores_visibilidad_RASFAS, colores_nocturnidad_RASFAS, colores_mar_AAW, colores_mar_ASW, colores_mar_ASUW, colores_lluvia_ASUW):
    horas = ["06a1", "12", "18", "00", "06a2"]
    matriz = {}
    matriz_t = {}

    print("Generando matriz...")

    for hora in horas:
        # HELO
        color_mar_HELO = colores_mar_HELO[f"color_mar_HELO_{hora}"]
        color_viento_HELO = colores_viento_HELO[f"color_viento_HELO_{hora}"]
        color_visibilidad_HELO = colores_visibilidad_HELO[f"color_visibilidad_HELO_{hora}"]
        color_techo_HELO = colores_techo_HELO[f"color_techo_HELO_{hora}"]

        texto_HELO = []
        if color_mar_HELO == "FFFE25" or color_mar_HELO == "FF0000":
            texto_HELO.append("SS")
        if color_viento_HELO == "FFFE25" or color_viento_HELO == "FF0000":
            texto_HELO.append("W")
        if color_visibilidad_HELO == "FFFE25" or color_visibilidad_HELO == "FF0000":
            texto_HELO.append("V")
        if color_techo_HELO == "FFFE25" or color_techo_HELO == "FF0000":
            texto_HELO.append("CC")

        if "FF0000" in [color_mar_HELO, color_viento_HELO, color_visibilidad_HELO, color_techo_HELO]:
            matriz[f"HELOa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_HELO, color_viento_HELO, color_visibilidad_HELO, color_techo_HELO]:
            matriz[f"HELOa{hora}aC"] = "FFFE25"
        else:
            matriz[f"HELOa{hora}aC"] = "00E500"

        matriz_t[f"HELOa{hora}aT"] = ", ".join(texto_HELO) if texto_HELO else ""

        # STOVL
        color_mar_STOVL = colores_mar_STOVL[f"color_mar_STOVL_{hora}"]
        color_viento_STOVL = colores_viento_STOVL[f"color_viento_STOVL_{hora}"]
        color_visibilidad_STOVL = colores_visibilidad_STOVL[f"color_visibilidad_STOVL_{hora}"]
        color_techo_STOVL = colores_techo_STOVL[f"color_techo_STOVL_{hora}"]
        color_temperatura_STOVL = colores_temperatura_STOVL[f"color_temperatura_STOVL_{hora}"]

        texto_STOVL = []
        if color_mar_STOVL == "FFFE25" or color_mar_STOVL == "FF0000":
            texto_STOVL.append("SS")
        if color_viento_STOVL == "FFFE25" or color_viento_STOVL == "FF0000":
            texto_STOVL.append("W")
        if color_visibilidad_STOVL == "FFFE25" or color_visibilidad_STOVL == "FF0000":
            texto_STOVL.append("V")
        if color_techo_STOVL == "FFFE25" or color_techo_STOVL == "FF0000":
            texto_STOVL.append("CC")
        if color_temperatura_STOVL == "FFFE25" or color_temperatura_STOVL == "FF0000":
            texto_STOVL.append("T")

        if "FF0000" in [color_mar_STOVL, color_viento_STOVL, color_visibilidad_STOVL, color_techo_STOVL, color_temperatura_STOVL]:
            matriz[f"STOVLa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_STOVL, color_viento_STOVL, color_visibilidad_STOVL, color_techo_STOVL, color_temperatura_STOVL]:
            matriz[f"STOVLa{hora}aC"] = "FFFE25"
        else:
            matriz[f"STOVLa{hora}aC"] = "00E500"

        matriz_t[f"STOVLa{hora}aT"] = ", ".join(texto_STOVL) if texto_STOVL else ""

        # VEHICLES
        color_lluvia_VEHICLES = colores_lluvia_VEHICLES[f"color_lluvia_VEHICLES_{hora}"]

        texto_VEHICLES = []
        if color_lluvia_VEHICLES == "FFFE25" or color_lluvia_VEHICLES == "FF0000":
            texto_VEHICLES.append("P")

        if "FF0000" in [color_lluvia_VEHICLES]:
            matriz[f"VEHICLESa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_lluvia_VEHICLES]:
            matriz[f"VEHICLESa{hora}aC"] = "FFFE25"
        else:
            matriz[f"VEHICLESa{hora}aC"] = "00E500"

        matriz_t[f"VEHICLESa{hora}aT"] = ", ".join(texto_VEHICLES) if texto_VEHICLES else ""

        # PERSONNEL
        color_mar_PERSONNEL = colores_mar_PERSONNEL[f"color_mar_PERSONNEL_{hora}"]
        color_lluvia_PERSONNEL = colores_lluvia_PERSONNEL[f"color_lluvia_PERSONNEL_{hora}"]
        color_temperatura_PERSONNEL = colores_temperatura_PERSONNEL[f"color_temperatura_PERSONNEL_{hora}"]

        texto_PERSONNEL = []
        if color_mar_PERSONNEL == "FFFE25" or color_mar_PERSONNEL == "FF0000":
            texto_PERSONNEL.append("SS")
        if color_lluvia_PERSONNEL == "FFFE25" or color_lluvia_PERSONNEL == "FF0000":
            texto_PERSONNEL.append("P")
        if color_temperatura_PERSONNEL == "FFFE25" or color_temperatura_PERSONNEL == "FF0000":
            texto_PERSONNEL.append("T")

        if "FF0000" in [color_mar_PERSONNEL, color_lluvia_PERSONNEL, color_temperatura_PERSONNEL]:
            matriz[f"PERSONNELa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_PERSONNEL, color_lluvia_PERSONNEL, color_temperatura_PERSONNEL]:
            matriz[f"PERSONNELa{hora}aC"] = "FFFE25"
        else:
            matriz[f"PERSONNELa{hora}aC"] = "00E500"

        matriz_t[f"PERSONNELa{hora}aT"] = ", ".join(texto_PERSONNEL) if texto_PERSONNEL else ""

        # SCAT
        color_viento_SCAT = colores_viento_SCAT[f"color_viento_SCAT_{hora}"]
        color_mar_SCAT = colores_mar_SCAT[f"color_mar_SCAT_{hora}"]
        color_visibilidad_SCAT = colores_visibilidad_SCAT[f"color_visibilidad_SCAT_{hora}"]
        color_nocturnidad_SCAT = colores_nocturnidad_SCAT[f"color_nocturnidad_SCAT_{hora}"]

        texto_SCAT = []
        if color_viento_SCAT == "FFFE25" or color_viento_SCAT == "FF0000":
            texto_SCAT.append("W")
        if color_mar_SCAT == "FFFE25" or color_mar_SCAT == "FF0000":
            texto_SCAT.append("SS")
        if color_visibilidad_SCAT == "FFFE25" or color_visibilidad_SCAT == "FF0000":
            texto_SCAT.append("V")
        if color_nocturnidad_SCAT == "FFFE25" or color_nocturnidad_SCAT == "FF0000":
            texto_SCAT.append("N")

        if "FF0000" in [color_viento_SCAT, color_mar_SCAT, color_visibilidad_SCAT, color_nocturnidad_SCAT]:
            matriz[f"SCATa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_viento_SCAT, color_mar_SCAT, color_visibilidad_SCAT, color_nocturnidad_SCAT]:
            matriz[f"SCATa{hora}aC"] = "FFFE25"
        else:
            matriz[f"SCATa{hora}aC"] = "00E500"

        matriz_t[f"SCATa{hora}aT"] = ", ".join(texto_SCAT) if texto_SCAT else ""

        # LND
        color_mar_LND = colores_mar_LND[f"color_mar_LND_{hora}"]

        texto_LND = []
        if color_mar_LND == "FFFE25" or color_mar_LND == "FF0000":
            texto_LND.append("SS")

        if "FF0000" in [color_mar_LND]:
            matriz[f"LNDa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_LND]:
            matriz[f"LNDa{hora}aC"] = "FFFE25"
        else:
            matriz[f"LNDa{hora}aC"] = "00E500"

        matriz_t[f"LNDa{hora}aT"] = ", ".join(texto_LND) if texto_LND else ""

        # RHIB
        color_viento_RHIB = colores_viento_RHIB[f"color_viento_RHIB_{hora}"]
        color_mar_RHIB = colores_mar_RHIB[f"color_mar_RHIB_{hora}"]
        color_visibilidad_RHIB = colores_visibilidad_RHIB[f"color_visibilidad_RHIB_{hora}"]
        color_nocturnidad_RHIB = colores_nocturnidad_RHIB[f"color_nocturnidad_RHIB_{hora}"]

        texto_RHIB = []
        if color_viento_RHIB == "FFFE25" or color_viento_RHIB == "FF0000":
            texto_RHIB.append("W")
        if color_mar_RHIB == "FFFE25" or color_mar_RHIB == "FF0000":
            texto_RHIB.append("SS")
        if color_visibilidad_RHIB == "FFFE25" or color_visibilidad_RHIB == "FF0000":
            texto_RHIB.append("V")
        if color_nocturnidad_RHIB == "FFFE25" or color_nocturnidad_RHIB == "FF0000":
            texto_RHIB.append("N")

        if "FF0000" in [color_viento_RHIB, color_mar_RHIB, color_visibilidad_RHIB, color_nocturnidad_RHIB]:
            matriz[f"RHIBa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_viento_RHIB, color_mar_RHIB, color_visibilidad_RHIB, color_nocturnidad_RHIB]:
            matriz[f"RHIBa{hora}aC"] = "FFFE25"
        else:
            matriz[f"RHIBa{hora}aC"] = "00E500"

        matriz_t[f"RHIBa{hora}aT"] = ", ".join(texto_RHIB) if texto_RHIB else ""

        # RASFAS
        color_viento_RASFAS = colores_viento_RASFAS[f"color_viento_RASFAS_{hora}"]
        color_mar_RASFAS = colores_mar_RASFAS[f"color_mar_RASFAS_{hora}"]
        color_visibilidad_RASFAS = colores_visibilidad_RASFAS[f"color_visibilidad_RASFAS_{hora}"]
        color_nocturnidad_RASFAS = colores_nocturnidad_RASFAS[f"color_nocturnidad_RASFAS_{hora}"]

        texto_RASFAS = []
        if color_viento_RASFAS == "FFFE25" or color_viento_RASFAS == "FF0000":
            texto_RASFAS.append("W")
        if color_mar_RASFAS == "FFFE25" or color_mar_RASFAS == "FF0000":
            texto_RASFAS.append("SS")
        if color_visibilidad_RASFAS == "FFFE25" or color_visibilidad_RASFAS == "FF0000":
            texto_RASFAS.append("V")
        if color_nocturnidad_RASFAS == "FFFE25" or color_nocturnidad_RASFAS == "FF0000":
            texto_RASFAS.append("N")

        if "FF0000" in [color_viento_RASFAS, color_mar_RASFAS, color_visibilidad_RASFAS, color_nocturnidad_RASFAS]:
            matriz[f"RASFASa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_viento_RASFAS, color_mar_RASFAS, color_visibilidad_RASFAS, color_nocturnidad_RASFAS]:
            matriz[f"RASFASa{hora}aC"] = "FFFE25"
        else:
            matriz[f"RASFASa{hora}aC"] = "00E500"

        matriz_t[f"RASFASa{hora}aT"] = ", ".join(texto_RASFAS) if texto_RASFAS else ""

        # AAW
        color_mar_AAW = colores_mar_AAW[f"color_mar_AAW_{hora}"]

        texto_AAW = []
        if color_mar_AAW == "FFFE25" or color_mar_AAW == "FF0000":
            texto_AAW.append("SS")

        if "FF0000" in [color_mar_AAW]:
            matriz[f"AAWa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_AAW]:
            matriz[f"AAWa{hora}aC"] = "FFFE25"
        else:
            matriz[f"AAWa{hora}aC"] = "00E500"

        matriz_t[f"AAWa{hora}aT"] = ", ".join(texto_AAW) if texto_AAW else ""

        # ASW
        color_mar_ASW = colores_mar_ASW[f"color_mar_ASW_{hora}"]

        texto_ASW = []
        if color_mar_ASW == "FFFE25" or color_mar_ASW == "FF0000":
            texto_ASW.append("SS")

        if "FF0000" in [color_mar_ASW]:
            matriz[f"ASWa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_ASW]:
            matriz[f"ASWa{hora}aC"] = "FFFE25"
        else:
            matriz[f"ASWa{hora}aC"] = "00E500"

        matriz_t[f"ASWa{hora}aT"] = ", ".join(texto_ASW) if texto_ASW else ""

        # ASUW
        color_mar_ASUW = colores_mar_ASUW[f"color_mar_ASUW_{hora}"]
        color_lluvia_ASUW = colores_lluvia_ASUW[f"color_lluvia_ASUW_{hora}"]

        texto_ASUW = []
        if color_mar_ASUW == "FFFE25" or color_mar_ASUW == "FF0000":
            texto_ASUW.append("SS")
        if color_lluvia_ASUW == "FFFE25" or color_lluvia_ASUW == "FF0000":
            texto_ASUW.append("P")

        if "FF0000" in [color_mar_ASUW, color_lluvia_ASUW]:
            matriz[f"ASUWa{hora}aC"] = "FF0000"
        elif "FFFE25" in [color_mar_ASUW, color_lluvia_ASUW]:
            matriz[f"ASUWa{hora}aC"] = "FFFE25"
        else:
            matriz[f"ASUWa{hora}aC"] = "00E500"

        matriz_t[f"ASUWa{hora}aT"] = ", ".join(texto_ASUW) if texto_ASUW else ""

    with open("../Output/Matriz.tex", "w", encoding="utf-8") as f:
        for hora in horas:
            for operacion in ["HELO", "STOVL", "VEHICLES", "PERSONNEL", "SCAT", "LND", "RHIB", "RASFAS", "AAW", "ASW", "ASUW"]:
                clave_c = f"{operacion}a{hora}aC"
                clave_t = f"{operacion}a{hora}aT"
                if clave_c in matriz:
                    f.write(f"\\expandafter\\def\\csname {clave_c}\\endcsname{{{matriz[clave_c]}}}\n")
                if clave_t in matriz_t:
                    f.write(f"\\expandafter\\def\\csname {clave_t}\\endcsname{{{matriz_t[clave_t]}}}\n")

def definir_area(lat_usuario, lon_usuario):
    if 30 <= lat_usuario <= 70 and -30 <= lon_usuario <= 50:
        area = "europe"
    elif 66 <= lat_usuario <= 90:
        area = "arctic"
    elif 0 <= lat_usuario <= 30 and 30 <= lon_usuario <= 90:
        area = "middle_east_and_india"
    elif -50 <= lat_usuario <= -10 and 105 <= lon_usuario <= 180:
        area = "australasia"
    elif -10 <= lat_usuario < 30 and 80 <= lon_usuario <= 160:
        area = "south_east_asia_and_indonesia"
    elif 30 <= lat_usuario <= 70 and -60 <= lon_usuario < 0:
        area = "north_atlantic"
    elif -60 <= lat_usuario < 20 and -40 <= lon_usuario <= 100:
        area = "south_atlantic_and_indian_ocean"
    elif -60 <= lat_usuario <= 60 and -180 <= lon_usuario <= -70:
        area = "pacific"
    elif -60 <= lat_usuario <= 60 and 100 <= lon_usuario <= 180:
        area = "pacific"
    else:
        area = "global"
    
    print(f"Área definida: {area}")
    return area

def construir_URL(area, Ano_Ej, Mes_Ej, Dia_Ej):
    URL_06_presion = f"https://charts.ecmwf.int/products/medium-mslp-rain?base_time={Ano_Ej}{Mes_Ej}{Dia_Ej}0000&interval=6&projection=opencharts_{area}&valid_time={Ano_Ej}{Mes_Ej}{Dia_Ej}0600"
    URL_12_presion = f"https://charts.ecmwf.int/products/medium-mslp-rain?base_time={Ano_Ej}{Mes_Ej}{Dia_Ej}0000&interval=6&projection=opencharts_{area}&valid_time={Ano_Ej}{Mes_Ej}{Dia_Ej}1200"
    URL_visible = f"https://charts.ecmwf.int/products/medium-simulated-vis?base_time={Ano_Ej}{Mes_Ej}{Dia_Ej}0000&layer_name=sim_image_vis_ch2&projection=opencharts_{area}&valid_time={Ano_Ej}{Mes_Ej}{Dia_Ej}0600"
    print(URL_06_presion)
    print("\n\n")
    print(URL_12_presion)
    print("\n\n")
    print(URL_visible)