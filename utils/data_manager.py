# utils/data_manager.py

import json
import os
from datetime import datetime

# --- CONFIGURACIÓN ---

DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE_PATH = os.path.join(DATA_FOLDER, 'historial_tasas.json')

# --- FUNCIONES PRINCIPALES ---

def _ensure_data_folder_exists():
    if not os.path.exists(DATA_FOLDER):
        print(f"La carpeta '{DATA_FOLDER}' no existe. Creándola ahora...")
        os.makedirs(DATA_FOLDER)

def cargar_datos():
    _ensure_data_folder_exists() 
    
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Advertencia: El archivo de historial está vacío o corrupto. Se empezará de cero.")
        return []

def guardar_datos(datos):
    """
    Guarda la lista de datos en el archivo JSON.

    Args:
        datos (list): La lista de diccionarios del historial para guardar.
    """
    _ensure_data_folder_exists()

    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error crítico: No se pudo escribir en el archivo de historial: {e}")

def agregar_registro(tasas_oficiales, tasa_usdt, tasa_fisico):
    """
    Crea un nuevo registro con la fecha y hora actual y lo añade al historial.

    Args:
        tasas_oficiales (dict): El diccionario {'usd': valor, 'eur': valor} de la API.
        tasa_usdt (float): La tasa USDT ingresada por el usuario.
        tasa_fisico (float): La tasa de dólar físico ingresada por el usuario.
    """
    if not tasas_oficiales:
        print("Error: No se pueden agregar registros sin las tasas oficiales.")
        return

    historial = cargar_datos()
    
    nuevo_registro = {
        "fecha": datetime.now().isoformat(),
        "bcv_usd": tasas_oficiales['usd'],
        "bcv_eur": tasas_oficiales['eur'],
        "usdt": tasa_usdt,
        "fisico_calle": tasa_fisico
    }
    
    historial.append(nuevo_registro)
    
    guardar_datos(historial)
    print("\n¡Registro guardado exitosamente en el historial!")


# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("Realizando una prueba del módulo 'data_manager'...")
    
    tasas_simuladas_api = {'usd': 141.88, 'eur': 152.50}
    usdt_simulado = 155.50
    fisico_simulado = 153.00
    
    print("\nAgregando un nuevo registro de prueba...")
    agregar_registro(tasas_simuladas_api, usdt_simulado, fisico_simulado)
    
    print("\nLeyendo el historial completo para verificar...")
    historial_leido = cargar_datos()
    
    if historial_leido:
        print("El archivo de historial contiene ahora:")
        print(json.dumps(historial_leido, indent=2, ensure_ascii=False))
    else:
        print("--- La prueba falló ---")
        print("No se pudo leer el historial después de guardarlo.")

