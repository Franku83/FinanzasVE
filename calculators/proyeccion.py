# calculators/proyeccion.py

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.helpers import limpiar_pantalla, formatear_moneda
from utils.data_manager import cargar_datos
from calculators.inflacion import obtener_datos_analisis

def iniciar_asistente_precios():
    """Función principal para el asistente de precios, ahora basado en USD."""
    limpiar_pantalla()
    print("--- Asistente de Precios con Proyección (Basado en USD) ---")
    
    #Obtener datos de inflación de los últimos 30 días
    datos_inflacion = obtener_datos_analisis(30)
    if not datos_inflacion:
        print("\nError: No hay suficientes datos históricos (últimos 30 días) para realizar una proyección.")
        input("Presiona Enter para volver...")
        return

    # Preguntar el modelo de negocio para determinar qué inflación usar
    print("\n¿La inflación que más afecta tu negocio se refleja en la variación de qué tasa?")
    print("1. Tasa BCV (Si tus costos dependen de proveedores nacionales)")
    print("2. Tasa USDT (Si tus costos dependen de importaciones o precios dolarizados)")
    modelo_negocio = input("Elige una opción: ")

    if modelo_negocio == '1':
        inflacion_mensual = datos_inflacion['var_bcv_usd']
        tasa_referencia_nombre = "BCV"
    elif modelo_negocio == '2':
        inflacion_mensual = datos_inflacion['var_usdt']
        tasa_referencia_nombre = "USDT"
    else:
        print("\nOpción no válida.")
        input("Presiona Enter para volver...")
        return
        
    print(f"\nUsando una inflación proyectada del {inflacion_mensual:.2f}% mensual (basada en la variación de la tasa {tasa_referencia_nombre}).")

    #Recopilar datos del producto en dolares
    try:
        costo_actual_usd = float(input("\nIntroduce el costo de compra de tu producto (en USD): "))
        
        tipo_ganancia = input("¿Calculas tu ganancia por [P]orcentaje o [M]onto fijo en USD?: ").upper()
        
        if tipo_ganancia == 'P':
            porcentaje_ganancia = float(input("Introduce el porcentaje de ganancia deseado (ej: 60): "))
            ganancia_actual_usd = costo_actual_usd * (porcentaje_ganancia / 100)
        elif tipo_ganancia == 'M':
            ganancia_actual_usd = float(input("Introduce el monto fijo de ganancia deseado (en USD): "))
        else:
            print("\nOpción de ganancia no válida.")
            input("Presiona Enter para volver...")
            return

    except ValueError:
        print("\nError: Valor no numérico introducido.")
        input("Presiona Enter para volver...")
        return

    # 4. Calcular y mostrar escenario actual en USD.
    precio_venta_actual_usd = costo_actual_usd + ganancia_actual_usd
    print("\n--- Situación Actual ---")
    print(f"- Costo del Producto:   ${costo_actual_usd:,.2f} USD")
    print(f"- Tu Ganancia:          ${ganancia_actual_usd:,.2f} USD")
    print(f"- Precio de Venta Hoy:  ${precio_venta_actual_usd:,.2f} USD")

    # 5. Calcular proyecciones directamente en USD.
    inflacion_mensual_decimal = inflacion_mensual / 100
    inflacion_semanal_aprox = inflacion_mensual_decimal / 4 

    # Proyección amortiguada para la próxima semana
    precio_competitivo_usd = precio_venta_actual_usd * (1 + inflacion_semanal_aprox)
    # Proyección completa a 30 días
    precio_proyectado_real_usd = precio_venta_actual_usd * (1 + inflacion_mensual_decimal)

    # 6. Presentar resultados en USD.
    print("\n--- Sugerencias de Precios de Venta en USD ---")
    print(f"\n1. >> PRECIO COMPETITIVO SUGERIDO: ${precio_competitivo_usd:,.2f} USD <<")
    print("   - Este precio protege tu ganancia contra la inflación esperada para los próximos 7-10 días.")
    
    print(f"\n2. PRECIO DE REPOSICIÓN A 30 DÍAS: ${precio_proyectado_real_usd:,.2f} USD")
    print("   - Este es el precio al que deberías vender en un mes para mantener el valor de tu ganancia.")

    # 7. (Extra) Mostrar equivalencia en Bolívares usando la última tasa USDT registrada.
    historial = cargar_datos()
    if historial:
        ultima_tasa_usdt = historial[-1]['usdt']
        print("\n--- Equivalencia en Bolívares (informativo) ---")
        print(f"Usando la última tasa USDT registrada: {formatear_moneda(ultima_tasa_usdt)}")
        print(f"- Precio Competitivo: {formatear_moneda(precio_competitivo_usd * ultima_tasa_usdt)}")
        print(f"- Precio a 30 días:   {formatear_moneda(precio_proyectado_real_usd * ultima_tasa_usdt)}")

    input("\nPresiona Enter para volver al Menú Principal...")

# --- Bloque de Prueba --- 
if __name__ == "__main__":
    iniciar_asistente_precios()