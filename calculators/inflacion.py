# calculators/inflacion.py
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.data_manager import cargar_datos
from utils.helpers import limpiar_pantalla


def calcular_variacion_porcentual(valor_nuevo, valor_antiguo):
    if valor_antiguo == 0:
        return float('inf')
    return ((valor_nuevo - valor_antiguo) / valor_antiguo) * 100

def calcular_brecha(usdt, bcv):
    if bcv == 0:
        return float('inf')
    return ((usdt / bcv) - 1) * 100


def obtener_datos_analisis(periodo_dias=30):
    historial = cargar_datos()
    
    if not historial:
        return None 

    fecha_limite = datetime.now() - timedelta(days=periodo_dias)
    historial_filtrado = [
        reg for reg in historial 
        if datetime.fromisoformat(reg['fecha']) >= fecha_limite
    ]
    
    if len(historial_filtrado) < 2:
        return None 

    registro_antiguo = historial_filtrado[0]
    registro_nuevo = historial_filtrado[-1]


    var_bcv_usd = calcular_variacion_porcentual(registro_nuevo['bcv_usd'], registro_antiguo['bcv_usd'])
    var_usdt = calcular_variacion_porcentual(registro_nuevo['usdt'], registro_antiguo['usdt'])
    brecha_antigua = calcular_brecha(registro_antiguo['usdt'], registro_antiguo['bcv_usd'])
    brecha_nueva = calcular_brecha(registro_nuevo['usdt'], registro_nuevo['bcv_usd'])

    return {
        "periodo": periodo_dias,
        "fecha_inicio": registro_antiguo['fecha'],
        "fecha_fin": registro_nuevo['fecha'],
        "var_bcv_usd": var_bcv_usd,
        "var_usdt": var_usdt,
        "brecha_antigua": brecha_antigua,
        "brecha_nueva": brecha_nueva
    }


def mostrar_reporte_analisis(datos_analisis):
    if not datos_analisis:
        print("\nNo hay suficientes datos para generar un reporte.")
        return

    periodo_texto = f"en los últimos {datos_analisis['periodo']} días"
    print(f"\nAnálisis comparando desde {datos_analisis['fecha_inicio'][:10]} hasta {datos_analisis['fecha_fin'][:10]} ({periodo_texto}):")
    
    print("\n--- Variación de Tasas ---")
    print(f"  - Tasa BCV Dólar:     {datos_analisis['var_bcv_usd']:+.2f}%")
    print(f"  - Tasa USDT:          {datos_analisis['var_usdt']:+.2f}%")
    
    print("\n--- Brecha Cambiaria (USDT vs BCV) ---")
    print(f"  - Brecha al inicio:   {datos_analisis['brecha_antigua']:.2f}%")
    print(f"  - Brecha al final:    {datos_analisis['brecha_nueva']:.2f}%")
    var_brecha = datos_analisis['brecha_nueva'] - datos_analisis['brecha_antigua']
    print(f"  - Variación de brecha: {var_brecha:+.2f} puntos porcentuales")


def iniciar_analisis_inflacion():
    while True:
        limpiar_pantalla()
        print("--- Menú de Análisis de Inflación ---")
        print("\nSelecciona el período que deseas analizar:")
        print("1. Últimos 7 días")
        print("2. Últimos 30 días")
        print("0. Volver al Menú Principal")
        
        opcion = input("\nElige una opción: ")
        
        datos = None
        if opcion == '1':
            datos = obtener_datos_analisis(7)
        elif opcion == '2':
            datos = obtener_datos_analisis(30)
        elif opcion == '0':
            return
        else:
            print("\nOpción no válida.")
            input("\nPresiona Enter para continuar...")
            continue
            
        mostrar_reporte_analisis(datos)
        input("\nPresiona Enter para continuar...")
        
# --- Bloque de Prueba ---
if __name__ == "__main__":
    iniciar_analisis_inflacion()
