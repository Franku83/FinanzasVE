#calculators/simple.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.api_handler import obtener_tasas_bcv
from utils.data_manager import cargar_datos
from utils.helpers import limpiar_pantalla, formatear_moneda

def iniciar_calculadora_simple():
    """
    Función principal para la calculadora de divisas simple.
    Se ejecuta en un bucle hasta que el usuario decide salir.
    """
    while True:
        limpiar_pantalla()
        print("--- Calculadora de Divisas (Simple) ---")

        tasas_actuales = obtener_tasas_bcv()
        historial = cargar_datos()
        ultimo_registro = historial[-1] if historial else {}

        if not tasas_actuales and not ultimo_registro:
            print("\nError: No hay tasas disponibles para realizar cálculos.")
            print("Por favor, registra las tasas del día primero (Opción 1).")
            input("\nPresiona Enter para volver al menú principal...")
            return

        tasa_bcv_usd = tasas_actuales.get('usd', 0)
        tasa_bcv_eur = tasas_actuales.get('eur', 0)
        tasa_usdt = ultimo_registro.get('usdt', 0)
        
        print("\nTasas de Referencia para el Cálculo:")
        print(f"  - BCV Dólar:    {formatear_moneda(tasa_bcv_usd)}")
        print(f"  - BCV Euro:     {formatear_moneda(tasa_bcv_eur)}")
        print(f"  - USDT:         {formatear_moneda(tasa_usdt)}")

        print("\n¿Qué conversión deseas realizar?")
        print("\n  [ De Bolívares a Divisas ]")
        print("  11. Bolívares a Dólar BCV")
        print("  12. Bolívares a Euro BCV")
        print("  13. Bolívares a USDT")
        print("\n  [ De Divisas a Bolívares ]")
        print("  21. Dólar BCV a Bolívares")
        print("  22. Euro BCV a Bolívares")
        print("  23. USDT a Bolívares")
        print("\n  0. Volver al Menú Principal")

        opcion = input("\nElige una opción: ")


        conversiones = {
            '11': ('Bs.', 'Dólar BCV', lambda monto: monto / tasa_bcv_usd if tasa_bcv_usd else 0),
            '12': ('Bs.', 'Euro BCV', lambda monto: monto / tasa_bcv_eur if tasa_bcv_eur else 0),
            '13': ('Bs.', 'USDT', lambda monto: monto / tasa_usdt if tasa_usdt else 0),
            '21': ('Dólar BCV', 'Bs.', lambda monto: monto * tasa_bcv_usd),
            '22': ('Euro BCV', 'Bs.', lambda monto: monto * tasa_bcv_eur),
            '23': ('USDT', 'Bs.', lambda monto: monto * tasa_usdt),
        }

        if opcion == '0':
            return 

        if opcion in conversiones:
            try:
                moneda_origen, moneda_destino, operacion = conversiones[opcion]
                
                monto_str = input(f"\nIntroduce el monto en {moneda_origen}: ")
                monto_inicial = float(monto_str)
                
                resultado = operacion(monto_inicial)

                if resultado == 0:
                     print(f"\nError: La tasa de referencia para '{moneda_destino}' es 0. No se puede calcular.")
                else:
                    resultado_formateado = formatear_moneda(resultado) if "Bs." in moneda_destino else f"{resultado:,.2f}"
                    print("\n" + "="*25)
                    print(f"  RESULTADO:")
                    print(f"  {monto_inicial:,.2f} {moneda_origen} son")
                    print(f"  {resultado_formateado} {moneda_destino}")
                    print("="*25)

            except ValueError:
                print("\nError: Monto no válido. Debes introducir un número.")
            except Exception as e:
                print(f"\nOcurrió un error inesperado: {e}")
        else:
            print("\nOpción no válida. Inténtalo de nuevo.")

        input("\nPresiona Enter para realizar otro cálculo...")
        
# --- Bloque de Prueba ---

if __name__ == "__main__":
    iniciar_calculadora_simple()

