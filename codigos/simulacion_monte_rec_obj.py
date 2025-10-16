"""
=====================================================================
SIMULACIÓN MONTE CARLO — EFICIENCIA DE UN ROBOT RECOLECTOR
---------------------------------------------------------------------
Objetivo:
    Estimar la probabilidad de que un robot que se mueve aleatoriamente
    por una cuadrícula de 10x10 celdas (cada una con probabilidad p=0.1
    de contener un objeto) logre recolectar al menos 5 objetos en 20 movimientos.

Método:
    Monte Carlo con M simulaciones independientes.

s
"""

import random
import math

def validar_parametros(filas, columnas, p, movimientos, M):
    if filas <= 0 or columnas <= 0:
        raise ValueError("filas y columnas deben ser positivos.")
    if not (0 <= p <= 1):
        raise ValueError("p debe estar entre 0 y 1.")
    if movimientos < 0:
        raise ValueError("movimientos debe ser no negativo.")
    if M <= 0:
        raise ValueError("M (número de simulaciones) debe ser positivo.")

def simular_un_recorrido(filas, columnas, p, movimientos):
    grid = [[1 if random.random() < p else 0 for _ in range(columnas)] for _ in range(filas)]
    fila, col = random.randint(0, filas - 1), random.randint(0, columnas - 1)
    visitadas = {(fila, col)}
    recolectados = 0
    if grid[fila][col] == 1:
        recolectados += 1
        grid[fila][col] = 0
    for _ in range(movimientos):
        posibles = []
        if fila > 0: posibles.append((fila - 1, col))
        if fila < filas - 1: posibles.append((fila + 1, col))
        if col > 0: posibles.append((fila, col - 1))
        if col < columnas - 1: posibles.append((fila, col + 1))
        posibles = [c for c in posibles if c not in visitadas]
        if not posibles:
            break
        fila, col = random.choice(posibles)
        visitadas.add((fila, col))
        if grid[fila][col] == 1:
            recolectados += 1
            grid[fila][col] = 0
    return recolectados

def simulacion_robot_recolector(filas=10, columnas=10, p=0.1, movimientos=20, M=10000, objetivo=5, seed=None):
    """
    Retorna un diccionario con resultados de la simulación Monte Carlo,
    sin imprimir ni generar gráficos.
    """
    validar_parametros(filas, columnas, p, movimientos, M)
    if seed is not None:
        random.seed(seed)

    exitos = 0
    resultados = []
    for _ in range(M):
        recolectados = simular_un_recorrido(filas, columnas, p, movimientos)
        resultados.append(recolectados)
        if recolectados >= objetivo:
            exitos += 1

    prob_estimada = exitos / M
    se = math.sqrt(prob_estimada * (1 - prob_estimada) / M)
    z = 1.96
    ci_lower = max(0.0, prob_estimada - z * se)
    ci_upper = min(1.0, prob_estimada + z * se)

    mensaje = (
        "Simulación Monte Carlo - Robot Recolector\n"
        f"Cuadrícula: {filas}x{columnas}\n"
        f"Probabilidad p de objeto: {p}\n"
        f"N° movimientos: {movimientos}\n"
        f"N° simulaciones: {M}\n"
        f"Objetivo: >= {objetivo} objetos\n"
        f"Casos exitosos: {exitos}\n"
        f"Probabilidad estimada: {prob_estimada:.6f}\n"
        f"Error estándar: {se:.6f}\n"
        f"IC 95%: [{ci_lower:.6f}, {ci_upper:.6f}]\n"
    )

    return {
        "resultados_simulacion": resultados,
        "M": M,
        "exitos": exitos,
        "probabilidad_estimada": prob_estimada,
        "error_estandar": se,
        "IC_95": (ci_lower, ci_upper),
        "mensaje": mensaje
    }

# --- Ejecución segura para pruebas ---
if __name__ == "__main__":
    try:
        salida = simulacion_robot_recolector(M=1000, seed=42)
        print(salida["mensaje"])
    except Exception as e:
        print("Error en la simulación:", str(e))
