"""
=====================================================================
SIMULACIÓN MONTE CARLO — PROBABILIDAD DE COLISIÓN EN RED DE SENSORES
---------------------------------------------------------------------
Propósito:
    Estimar la probabilidad de que ocurra al menos una colisión
    en una red de sensores inalámbricos, cuando los tiempos de 
    transmisión son aleatorios.


"""
"""
    Simula colisiones en una red de sensores donde cada nodo transmite
    en un instante aleatorio dentro de [0,1]. Si dos transmisiones
    ocurren con diferencia menor que delta, se considera colisión.

    Parámetros:
        N (int): Número de nodos transmisores.
        delta (float): Diferencia mínima para considerar colisión.
        M (int): Número de simulaciones Monte Carlo.
        seed (int, opcional): Semilla para reproducibilidad.

    Retorna:
        dict: Contiene resultados y mensaje para dashboard:
            - 'nodos', 'delta', 'simulaciones', 'colisiones', 'probabilidad', 'mensaje'
    """
import random

def simulacion_colisiones(N=10, delta=0.05, M=100000, seed=None):
    
    if N <= 0 or delta <= 0 or M <= 0:
        return {"mensaje": "Parámetros inválidos. Todos deben ser mayores que 0."}

    if seed is not None:
        random.seed(seed)

    colisiones = 0

    for _ in range(M):
        tiempos = sorted(random.random() for _ in range(N))
        if any(tiempos[i+1] - tiempos[i] < delta for i in range(N-1)):
            colisiones += 1

    probabilidad = colisiones / M

    mensaje = (
        "=== MÉTODO MONTE CARLO ===\n"
        f"Número de nodos: {N}\n"
        f"Número de simulaciones: {M}\n"
        f"Ventana de colisión delta = {delta} s\n"
        f"Simulaciones con colisión: {colisiones}\n"
        f"Probabilidad estimada de al menos una colisión: {probabilidad:.5f}\n"
    )

    resultado = {
        "nodos": N,
        "delta": delta,
        "simulaciones": M,
        "colisiones": colisiones,
        "probabilidad": probabilidad,
        "mensaje": mensaje
    }

    return resultado

# --- Ejecución segura ---
if __name__ == "__main__":
    try:
        salida = simulacion_colisiones(N=10, delta=0.05, M=100000, seed=42)
        print(salida["mensaje"])
    except Exception as e:
        print("Error en la simulación:", str(e))
