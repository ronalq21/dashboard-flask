"""
=========================================
ALGORITMO : Simulacion Monte Carlo - Sistema de Colas M/M/1
-----------------------------------------
Proposito:
    Modelar y simular una cafeteria con un solo empleado
    (1 servidor) donde los estudiantes llegan aleatoriamente
    y son atendidos en tiempos exponenciales.

Parametros del sistema:
    - Llegan 20 estudiantes por hora (lambda = 20/60 por minuto)
    - Cada servicio dura 2 minutos en promedio (mu = 1/2)
    - Total de iteraciones simuladas: 500

Calculos requeridos:
    a) Factor de utilizacion: rho = lambda / mu
    b) Numero promedio de estudiantes en la cola: Lq = rho^2 / (1 - rho)
    c) Tiempo promedio de espera analitico: Wq = Lq / lambda
    d) Resultados experimentales mediante simulacion Monte Carlo

Contexto de aplicacion:
    Evaluacion del rendimiento de sistemas de atencion al cliente,
    analisis de colas en cafeterias, bancos, call centers, etc.

Autor:
     y Ronaldhino Jinez Incacutipa
=========================================
"""

import random
import math

def simular_MM1(lambd=20/60, mu=1/2, iteraciones=500):
    """
    Simulacion Monte Carlo de un sistema M/M/1.
    Retorna un diccionario con resultados analiticos y simulados.
    """
    # Variables acumuladoras
    tiempos_espera = []
    tiempos_sistema = []
    tiempo_actual = 0
    tiempo_servidor_libre = 0

    # Simulacion Monte Carlo
    for _ in range(iteraciones):
        tiempo_llegada = -math.log(random.random()) / lambd
        tiempo_servicio = -math.log(random.random()) / mu

        tiempo_actual += tiempo_llegada

        espera = max(0, tiempo_servidor_libre - tiempo_actual)
        total = espera + tiempo_servicio
        tiempo_servidor_libre = tiempo_actual + total

        tiempos_espera.append(espera)
        tiempos_sistema.append(total)

    # Resultados analiticos
    rho = lambd / mu
    Lq = (rho ** 2) / (1 - rho) if rho < 1 else float('inf')
    Wq_analitico = Lq / lambd if rho < 1 else float('inf')

    # Resultados simulados
    promedio_espera = sum(tiempos_espera) / iteraciones
    promedio_sistema = sum(tiempos_sistema) / iteraciones

    mensaje = (
        "RESULTADOS - SIMULACION M/M/1\n"
        f"Factor de utilizacion (rho): {rho:.3f}\n"
        f"Numero promedio en la cola (Lq): {Lq:.3f}\n"
        f"Tiempo promedio de espera (Wq analitico): {Wq_analitico:.2f} minutos\n"
        f"Tiempo promedio de espera (Monte Carlo): {promedio_espera:.2f} minutos\n"
        f"Tiempo promedio total en el sistema (Monte Carlo): {promedio_sistema:.2f} minutos"
    )

    return {
        "rho": rho,
        "Lq_analitico": Lq,
        "Wq_analitico": Wq_analitico,
        "promedio_espera_MC": promedio_espera,
        "promedio_sistema_MC": promedio_sistema,
        "mensaje": mensaje
    }

# --- Ejecucion segura ---
if __name__ == "__main__":
    try:
        resultados = simular_MM1()
        print(resultados["mensaje"])
    except Exception as e:
        print("Error en la simulacion:", str(e))
