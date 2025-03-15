import sys, os
from colorama import init, Fore, Style
import urllib.request
import urllib.error

debug_mode = 1  # Modo de control de errores e información de desarrollo.

sys.path.append("./Lib")
#sys.path.append("./Lib_dependencies")

from Lib import *

os.system("clear")
print(Style.BRIGHT + Fore.RED + "#" + Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW + "##" + Style.RESET_ALL + Style.BRIGHT + Fore.RED + "#" + Style.RESET_ALL + " GAMELA v0.2 " + Style.RESET_ALL + Style.BRIGHT + Fore.RED + "#" + Style.RESET_ALL + Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW + "##" + Style.RESET_ALL + Style.RESET_ALL + Style.BRIGHT + Fore.RED + "#\n" + Style.RESET_ALL)

try:
    # Se intenta acceder a Google con un timeout de 5 segundos para verificar la conexión a internet. 
    urllib.request.urlopen("http://www.google.com", timeout=5)
    conexion = True
    print(Style.BRIGHT + Fore.GREEN + "El buque dispone de conexión a la red. Modos Automático y Manual habilitados.\n" + Style.RESET_ALL)
except urllib.error.URLError:
    conexion = False
    print(Style.BRIGHT + Fore.GREEN + "El buque NO dispone de conexión a la red. Solo modo Manual habilitado.\n" + Style.RESET_ALL)
    print()

Modo = input("Introduzca modo de operación:\n 1. Automático\n 2. Manual\nSelección:")

if Modo == "1":
    Main_automatico(debug_mode)

if Modo == "2":
    Main_manual(debug_mode)
