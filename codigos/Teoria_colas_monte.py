import pandas as pd
import numpy as np

def simular_cola_banco(num_clientes: int, tasa_llegada: float, tasa_servicio: float):
    """
    Simulación de Cola de Banco (Modelo M/M/1)
    Retorna resultados como texto o diccionario
    """

    # Verificación básica
    if num_clientes <= 0 or tasa_llegada <= 0 or tasa_servicio <= 0:
        return {"mensaje": "Parametros invalidos. Todos deben ser mayores que 0."}

    # Advertencia si el sistema es inestable
    advertencia = ""
    if tasa_llegada >= tasa_servicio:
        advertencia = "El sistema podria volverse inestable (lambda >= mu)."

    # Generar tiempos de llegada y servicio
    tiempos_llegada = np.random.exponential(1 / tasa_llegada, num_clientes)
    tiempos_servicio = np.random.exponential(1 / tasa_servicio, num_clientes)

    llegada_acumulada = 0
    fin_cajero = 0
    registros = []

    for i in range(num_clientes):
        llegada_acumulada += tiempos_llegada[i]
        inicio_servicio = max(llegada_acumulada, fin_cajero)
        espera = inicio_servicio - llegada_acumulada
        fin_servicio = inicio_servicio + tiempos_servicio[i]
        tiempo_total = fin_servicio - llegada_acumulada
        fin_cajero = fin_servicio

        registros.append({
            "Cliente": i + 1,
            "Llegada": round(llegada_acumulada, 3),
            "Inicio": round(inicio_servicio, 3),
            "Fin": round(fin_servicio, 3),
            "Espera": round(espera, 3),
            "Tiempo_Total": round(tiempo_total, 3),
        })

    df = pd.DataFrame(registros)

    # Métricas observadas
    promedio_espera = float(df["Espera"].mean())
    promedio_total = float(df["Tiempo_Total"].mean())
    clientes_esperaron = int((df["Espera"] > 0).sum())
    porcentaje_esperaron = round((clientes_esperaron / num_clientes) * 100, 2)

    # Resultados teóricos M/M/1
    rho = tasa_llegada / tasa_servicio
    if rho < 1:
        Lq = (rho ** 2) / (1 - rho)
        Wq = Lq / tasa_llegada
        L = rho / (1 - rho)
        W = L / tasa_llegada
        estabilidad = "Sistema estable (rho < 1)"
    else:
        Lq = Wq = L = W = 0
        estabilidad = "Sistema inestable (rho >= 1)"

    # Mensaje final
    mensaje = (
        "Simulacion de Cola de Banco (M/M/1)\n"
        f"Clientes simulados: {num_clientes}\n"
        f"lambda = {tasa_llegada:.3f}, mu = {tasa_servicio:.3f}, rho = {rho:.3f}\n"
        f"{estabilidad}\n\n"
        f"Promedio espera: {promedio_espera:.3f}\n"
        f"Promedio total: {promedio_total:.3f}\n"
        f"Clientes que esperaron: {clientes_esperaron} ({porcentaje_esperaron}%)\n\n"
        f"Valores teoricos M/M/1:\n"
        f"Lq = {Lq:.3f}   Wq = {Wq:.3f}\n"
        f"L = {L:.3f}   W = {W:.3f}\n\n"
        f"{advertencia}"
    )

    resultados = {
        "promedio_espera": promedio_espera,
        "promedio_total": promedio_total,
        "rho": rho,
        "clientes_esperaron": clientes_esperaron,
        "porcentaje_esperaron": porcentaje_esperaron,
        "Lq": Lq,
        "Wq": Wq,
        "L": L,
        "W": W,
    }

    return {"tabla": df, "resultados": resultados, "mensaje": mensaje}


# --- Ejecución segura ---
if __name__ == "__main__":
    try:
        salida = simular_cola_banco(50, 0.8, 1.0)
        print(salida["mensaje"])
    except Exception as e:
        print("Error en la simulacion:", str(e))
