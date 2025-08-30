# utils/api_handler.py
import requests
import json

#--- OBTENER TASAS DE CAMBIO ---
def _obtener_usd_dolarapi():
    url = "https://ve.dolarapi.com/v1/dolares"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        for item in data:
            if item.get('fuente') == 'oficial':
                return float(item.get('promedio'))
        print("Error: No se encontró la tasa 'oficial' en la respuesta.")
        return None
    except Exception as e:
        print(f"Fallo en Paso 1: {e}")
        return None

def _obtener_eur_usd_internacional():
    url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        tasa_eur_usd = data.get('rates', {}).get('USD')
        if tasa_eur_usd:
            return float(tasa_eur_usd)
        return None
    except Exception as e:
        print(f"Fallo en Paso 2: {e}")
        return None

# --- FUNCIÓN PRINCIPAL QUE USA EL RESTO DEL PROGRAMA ---
def obtener_tasas_bcv():
    
    tasa_usd_ves = _obtener_usd_dolarapi()
    
    if tasa_usd_ves is None:
        print("\nFallo crítico: No se pudo obtener la tasa base de Dólar/Bolívar.")
        return None
    
    tasa_eur_usd = _obtener_eur_usd_internacional()
    
    tasa_eur_ves_final = 0.0
    if tasa_eur_usd:
        tasa_eur_ves_final = tasa_usd_ves * tasa_eur_usd
        print(f"Tasa EUR/VES = {tasa_usd_ves:.4f} (USD/VES) * {tasa_eur_usd:.4f} (EUR/USD) = {tasa_eur_ves_final:.4f}")
    else:
        print("\nAdvertencia: No se pudo obtener la tasa internacional para calcular el Euro.")

    return {
        'usd': tasa_usd_ves,
        'eur': tasa_eur_ves_final
    }

# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("Realizando una prueba del módulo 'api_handler' (versión con cálculo de Euro)...")
    tasas_obtenidas = obtener_tasas_bcv()
    
    if tasas_obtenidas:
        print("\n---------------------------------")
        print("--- ¡Prueba Final Exitosa! ---")
        print(f"Tasa Dólar BCV:   {tasas_obtenidas['usd']:.4f} Bs.")
        print(f"Tasa Euro BCV (Calculada): {tasas_obtenidas['eur']:.4f} Bs.")
        print("---------------------------------")
    else:
        print("\n--- La prueba falló ---")
        print("Revisa los mensajes de error para ver qué paso falló.")
