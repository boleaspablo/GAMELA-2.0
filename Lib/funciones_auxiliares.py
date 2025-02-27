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
def comparar_valores(olas_list, lluvia_list):
    horas = ["00", "06", "12", "18"]
    colores_mar_asuw = {}
    colores_mar_asw = {}
    colores_lluvia = {}
    
    for i, altura in enumerate(olas_list):
        if altura < 2.5:
            color = "verde"
        elif 2.5 <= altura <= 4:
            color = "amarillo"
        else:
            color = "rojo"
        colores_mar_asuw[f"color_mar_ASUW_{horas[i]}"] = color
        colores_mar_asw[f"color_mar_ASW_{horas[i]}"] = color

    for i, lluvia in enumerate(lluvia_list):
        color = "verde" if lluvia == "no" else "amarillo"
        colores_lluvia[f"color_lluvia_ASUW_{horas[i]}"] = color

    with open("colores.txt", "w", encoding="utf-8") as f:
        for clave, valor in colores_mar_asuw.items():
            f.write(f"{clave}: {valor}\n")
        for clave, valor in colores_mar_asw.items():
            f.write(f"{clave}: {valor}\n")
        for clave, valor in colores_lluvia.items():
            f.write(f"{clave}: {valor}\n")
    
    return colores_mar_asuw, colores_mar_asw, colores_lluvia
