"""
==========================================================
SIMULACION MONTECARLO — CAMINATA ALEATORIA 2D
----------------------------------------------------------
Proposito:
    Estimar por simulacion la probabilidad de que un caminante,
    partiendo del origen (0,0) y moviendose en pasos aleatorios
    de igual probabilidad en cuatro direcciones (N, S, E, O),
    termine con distancia de Manhattan |x| + |y| = condicion.

Modelo:
    - Cada movimiento tiene probabilidad 0.25 hacia cada direccion.
    - Movimiento en eje X o Y (±1 por paso).
    - Al final de 'movimientos' pasos se mide la distancia.

Parametros:
    simulaciones = 10000  # numero de experimentos Montecarlo
    movimientos = 10      # pasos por simulacion
    condicion = 2         # condicion de exito: |x| + |y| == 2

Resultados:
    - Probabilidad estimada (por frecuencia relativa)
==========================================================
"""

import random

def caminata_aleatoria_2D(simulaciones=10000, movimientos=10, condicion=2):
    aciertos = 0
    exitos = []          # 1 si cumple la condicion, 0 si no
    prob_acumulada = []  # probabilidad acumulada por simulacion

    for i in range(simulaciones):
        x, y = 0, 0
        for _ in range(movimientos):
            NA = random.randint(0, 100)
            if NA < 25:
                x += 1  # Este
            elif NA < 50:
                x -= 1  # Oeste
            elif NA < 75:
                y -= 1  # Sur
            else:
                y += 1  # Norte

        # Evaluar si cumple la condición |x| + |y| == condicion
        if abs(x) + abs(y) == condicion:
            aciertos += 1
            exitos.append(1)
        else:
            exitos.append(0)

        # Probabilidad acumulada hasta la simulacion actual
        prob_actual = aciertos / (i + 1)
        prob_acumulada.append(prob_actual)

    mensaje = (
        "=================================================\n"
        "RESULTADOS DE LA SIMULACION\n"
        "-------------------------------------------------\n"
        f"Numero total de simulaciones: {simulaciones}\n"
        f"Numero de pasos por caminata: {movimientos}\n"
        f"Condicion de exito: |x| + |y| = {condicion}\n"
        "-------------------------------------------------\n"
        f"Exitos observados: {aciertos}\n"
        f"Probabilidad estimada: {prob_acumulada[-1]:.4f}\n"
        "=================================================\n"
    )

    return {
        "simulaciones": simulaciones,
        "movimientos": movimientos,
        "condicion": condicion,
        "exitos": aciertos,
        "probabilidad_estimada": prob_acumulada[-1],
        "mensaje": mensaje
    }

# --- Ejecucion segura ---
if __name__ == "__main__":
    try:
        resultados = caminata_aleatoria_2D()
        print(resultados["mensaje"])
    except Exception as e:
        print("Error en la simulacion:", str(e))
