# main.py

from utils.api_handler import obtener_tasas_bcv
from utils.data_manager import agregar_registro, cargar_datos
from utils.helpers import limpiar_pantalla, formatear_moneda
from calculators.simple import iniciar_calculadora_simple
from calculators.avanzada import iniciar_calculadora_avanzada
from calculators.inflacion import iniciar_analisis_inflacion
from calculators.proyeccion import iniciar_asistente_precios

def mostrar_panel_bienvenida():
    print("--- FinanzasVE | Resumen del Mercado ---")
    
    tasas_actuales = obtener_tasas_bcv()
    
    if tasas_actuales:
        print("\nTasas Oficiales Actuales (BCV):")
        print(f"  - Dólar: {formatear_moneda(tasas_actuales['usd'])}")
        print(f"  - Euro:  {formatear_moneda(tasas_actuales['eur'])}")
    else:
        print("\nNo se pudieron obtener las tasas oficiales actuales.")

    historial = cargar_datos()
    if historial:
        ultimo_registro = historial[-1]
        print("\nÚltimo Registro Manual Guardado:")
        print(f"  - Fecha:   {ultimo_registro['fecha']}")
        print(f"  - USDT:    {formatear_moneda(ultimo_registro['usdt'])}")
        print(f"  - Físico:  {formatear_moneda(ultimo_registro['fisico_calle'])}")
    
    print("-----------------------------------------")

def registrar_tasas_del_dia():
    limpiar_pantalla()
    print("--- Registrar Tasas del Día ---")
    
    tasas_oficiales = obtener_tasas_bcv()
    if not tasas_oficiales:
        print("\nError: No se pudieron obtener las tasas oficiales del BCV. No se puede continuar.")
        input("Presiona Enter para volver al menú...")
        return

    print(f"\nTasas BCV obtenidas: Dólar={formatear_moneda(tasas_oficiales['usd'])}, Euro={formatear_moneda(tasas_oficiales['eur'])}")
    
    try:
        tasa_usdt = float(input("Introduce la tasa USDT de hoy: "))
        tasa_fisico = float(input("Introduce la tasa de Dólar Físico/Calle de hoy: "))
    except ValueError:
        print("\nError: Has introducido un valor no numérico.")
        input("Presiona Enter para volver al menú...")
        return
        
    agregar_registro(tasas_oficiales, tasa_usdt, tasa_fisico)
    input("\nPresiona Enter para volver al menú...")

def main():
    while True:
        limpiar_pantalla()
        mostrar_panel_bienvenida()
        
        print("\n--- Menú Principal ---")
        print("1. Registrar Tasas del Día")
        print("2. Calculadora de Divisas (Simple)")
        print("3. Calculadora de Precio Equivalente (Avanzada)")
        print("4. Análisis de Inflación y Brecha Cambiaria")
        print("5. Asistente de Precios con Proyección")
        print("6. Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            registrar_tasas_del_dia()
        elif opcion == '2':
           iniciar_calculadora_simple()
        elif opcion == '3':
            iniciar_calculadora_avanzada()
        elif opcion == '4':
            iniciar_analisis_inflacion()
        elif opcion == '5':
            iniciar_asistente_precios()
        elif opcion == '6':
            print("\n¡Gracias por usar FinanzasVE! Hasta luego.")
            break
        else:
            print("\nOpción no válida. Por favor, elige un número del 1 al 6.")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()


