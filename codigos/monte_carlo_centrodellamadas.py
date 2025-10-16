"""
=========================================
ALGORITMO : Sistema de Colas M/M/c (Call center)
-----------------------------------------
Propósito:
    Analizar un call center M/M/c con llegadas y servicios exponenciales:
    - Determinar estabilidad
    - Probabilidad de que todas las lineas (operadores) esten ocupadas (Erlang-C)
    - Tiempo promedio de espera en cola (Wq)
    - Calcular cuántos operadores se necesitan para que Wq < 30 s

Contexto:
    Aplicable a centros de atencion telefonica, puntos de venta, ventanillas, etc.

Parámetros usados (ejemplo):
    - Llegadas: 60 llamadas/hora → λ = 60/60 = 1 llamada/minuto
    - Servicio promedio: 4 minutos → μ = 1/4 llamadas/minuto
    - Intensidad de tráfico: a = λ/μ = 4.0
=========================================
"""
import math

# Parámetros (fijos para hosting)
lambd = 60 / 60.0   # llamadas por minuto = 1.0
mu = 1 / 4.0        # servicio por minuto = 0.25
a = lambd / mu      # intensidad de tráfico

def erlang_c(a, c):
    """
    Calcula la probabilidad de espera (Erlang-C), que coincide con la probabilidad
    de que todas las c lineas/servidores esten ocupadas en el instante de llegada.
    Devuelve None si el sistema no es estable (c <= a).
    """
    if c <= a:
        return None
    sum0 = sum(a**k / math.factorial(k) for k in range(c))
    ac = a**c / math.factorial(c)
    factor = c / (c - a)
    Pw = (ac * factor) / (sum0 + ac * factor)
    return Pw

def Wq_from_Pw(Pw, c, lambd, mu):
    """Calcula Wq (minutos) dado Pw: Wq = Pw / (c*mu - lambda)."""
    return Pw / (c * mu - lambd)

def Lq_from_Wq(Wq, lambd):
    """Número promedio en cola Lq = λ * Wq."""
    return lambd * Wq

def simulacion_call_center(c_min=3, c_max=50, umbral_segundos=30):
    """
    Retorna los resultados del call center M/M/c en un diccionario,
    listo para dashboard.
    """
    resultados_tabla = []
    mensaje = []

    # 1) Estabilidad para c = c_min
    estable_c_min = c_min > a
    mensaje.append("Parametros:")
    mensaje.append(f"lambda = {lambd:.3f} llamadas/minuto, mu = {mu:.3f} servicio/minuto, tráfico a = {a:.3f}")
    mensaje.append("Estabilidad:")
    if estable_c_min:
        mensaje.append(f"Con c = {c_min} el sistema es estable.")
    else:
        mensaje.append(f"Con c = {c_min} el sistema NO es estable (a >= c). Se requiere c > a para estabilidad.")

    # 2) Probabilidades y Wq para varios c
    for c_test in range(c_min, c_max + 1):
        Pw = erlang_c(a, c_test)
        if Pw is None:
            resultados_tabla.append({
                "c": c_test, "Pw": None, "Wq_minutos": None, "Wq_segundos": None, "Lq": None
            })
        else:
            Wq = Wq_from_Pw(Pw, c_test, lambd, mu)
            Lq = Lq_from_Wq(Wq, lambd)
            resultados_tabla.append({
                "c": c_test, "Pw": Pw, "Wq_minutos": Wq, "Wq_segundos": Wq*60, "Lq": Lq
            })

    # 3) Buscar número mínimo de operadores para Wq < umbral
    umbral_minutos = umbral_segundos / 60.0
    min_c = None
    for entry in resultados_tabla:
        if entry["Wq_minutos"] is not None and entry["Wq_minutos"] < umbral_minutos:
            min_c = entry["c"]
            Wq_min = entry["Wq_minutos"]
            Pw_min = entry["Pw"]
            Lq_min = entry["Lq"]
            break

    if min_c is None:
        mensaje.append(f"No se encontro un numero de operadores <= {c_max} que reduzca Wq por debajo de {umbral_segundos} segundos.")
    else:
        mensaje.append("Numero minimo de operadores para Wq < 30 s:")
        mensaje.append(f"c_min = {min_c}, Pw = {Pw_min:.6f}, Wq = {Wq_min:.4f} min = {Wq_min*60:.1f} s, Lq = {Lq_min:.4f}")

    return {
        "tabla": resultados_tabla,
        "mensaje": "\n".join(mensaje)
    }

# --- Ejecución segura ---
if __name__ == "__main__":
    try:
        salida = simulacion_call_center()
        print(salida["mensaje"])
    except Exception as e:
        print("Error en la simulacion:", str(e))
