# utils/helpers.py

import os
import platform

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def formatear_moneda(valor):
    return f"{valor:,.2f} Bs."

