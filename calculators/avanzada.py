# calculators/avanzada.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.api_handler import obtener_tasas_bcv
from utils.data_manager import cargar_datos
from utils.helpers import limpiar_pantalla, formatear_moneda

def calcular_equivalente_bcv_vs_usdt(tasa_bcv_usd):
    print("\n--- Calculando Equivalente BCV vs USDT ---")
    try:
        precio_usdt = float(input("Introduce el precio del producto en USD (basado en USDT): "))
        tasa_usdt_personalizada = float(input("Introduce la tasa USDT que usarás para el cálculo: "))
        
        total_bolivares = precio_usdt * tasa_usdt_personalizada
        if tasa_bcv_usd == 0:
            print("\nError: La tasa BCV del dólar es 0. No se puede calcular.")
            return

        precio_equivalente_bcv = total_bolivares / tasa_bcv_usd
        
        print("\n" + "="*45)
        print("  RESULTADO DEL CÁLCULO DE PRECIO EQUIVALENTE:")
        print(f"\n  Para obtener el valor de: {precio_usdt:,.2f} USD (a {formatear_moneda(tasa_usdt_personalizada)})")
        print(f"  Lo que equivale a: {formatear_moneda(total_bolivares)}")
        print(f"\n  >> DEBES COBRAR: {precio_equivalente_bcv:,.2f} USD (a tasa BCV) <<")
        print("="*45)

    except ValueError:
        print("\nError: Has introducido un valor no numérico.")

def calcular_dolar_euro_1a1(tasa_bcv_eur):
    """Simula la estrategia de cobrar en Euros BCV un precio fijado en Dólares."""
    print("\n--- Simulación de Estrategia Dólar-Euro (1 a 1) ---")
    try:
        precio_en_usd = float(input("Introduce el precio del producto en USD: "))
        
        precio_en_eur = precio_en_usd
        
        if tasa_bcv_eur == 0:
            print("\nError: La tasa BCV del euro es 0. No se puede calcular.")
            return
            
        total_bolivares_obtenido = precio_en_eur * tasa_bcv_eur
        
        print("\n" + "="*40)
        print("  RESULTADO DE LA SIMULACIÓN:")
        print(f"\n  Si un producto de {precio_en_usd:,.2f} USD...")
        print(f"  Lo cobras como {precio_en_eur:,.2f} EUR (a tasa BCV)")
        print(f"\n  >> OBTENDRÁS: {formatear_moneda(total_bolivares_obtenido)} <<")
        print("="*40)
        
    except ValueError:
        print("\nError: Has introducido un valor no numérico.")

def iniciar_calculadora_avanzada():
    """Función principal para la calculadora avanzada."""
    while True:
        limpiar_pantalla()
        print("--- Calculadora de Precio Equivalente (Avanzada) ---")
        
        tasas_actuales = obtener_tasas_bcv()
        if not tasas_actuales:
            print("\nError: No se pudieron obtener las tasas de referencia.")
            input("\nPresiona Enter para volver...")
            return

        tasa_bcv_usd = tasas_actuales.get('usd', 0)
        tasa_bcv_eur = tasas_actuales.get('eur', 0)
        
        print("\nElige una de las siguientes herramientas:")
        print("1. Calcular Precio Equivalente (BCV vs USDT)")
        print("2. Simular Estrategia Dólar-Euro 1 a 1")
        print("0. Volver al Menú Principal")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            calcular_equivalente_bcv_vs_usdt(tasa_bcv_usd)
        elif opcion == '2':
            calcular_dolar_euro_1a1(tasa_bcv_eur)
        elif opcion == '0':
            return
        else:
            print("\nOpción no válida.")
            
        input("\nPresiona Enter para continuar...")
        
# --- Bloque de Prueba ---
if __name__ == "__main__":
    iniciar_calculadora_avanzada()
