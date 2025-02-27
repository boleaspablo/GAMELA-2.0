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
