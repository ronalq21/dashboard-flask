"""
=========================================
ALGORITMO : Estimacion de pi — Metodo de Monte Carlo
-----------------------------------------
Proposito:
    Estimar el valor de pi simulando puntos aleatorios
    dentro de un cuadrado y verificando cuantos caen
    dentro del circulo inscrito.

Contexto de aplicacion:
    Este metodo se utiliza para ensenar simulacion
    estocastica, integracion numerica y generacion
    de numeros pseudoaleatorios.

Descripcion:
    1. Se generan puntos (x, y) uniformes en el rango [-1, 1].
    2. Se verifica si cada punto cumple x^2 + y^2 <= 1.
    3. La proporcion de puntos dentro del circulo
       respecto al total se multiplica por 4 para estimar pi.

No requiere entrada del usuario ni entorno grafico interactivo.
Guarda el resultado como imagen para visualizacion en dashboard.
=========================================
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def estimar_pi_montecarlo(n=1000, ruta_img="static/img/montecarlo_pi.png"):
    """
    Simula la estimacion de pi usando el metodo Monte Carlo.
    Retorna un diccionario con los resultados y guarda la imagen.
    """
    # Generar puntos
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)

    # Condicion: puntos dentro del circulo unitario
    dentro = (x**2 + y**2) <= 1
    total_dentro = np.sum(dentro)

    # Aproximacion de pi
    pi_aprox = 4 * total_dentro / n

    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta_img), exist_ok=True)

    # Graficar
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(x[dentro], y[dentro], color="blue", s=5, label="Dentro del circulo")
    ax.scatter(x[~dentro], y[~dentro], color="red", s=5, label="Fuera del circulo")
    circulo = plt.Circle((0, 0), radius=1, edgecolor="black", fill=False, linewidth=2)
    ax.add_patch(circulo)
    ax.set_aspect("equal")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    plt.title("Estimacion de pi — Metodo de Monte Carlo")
    plt.legend()
    plt.savefig(ruta_img)
    plt.close()

    # Resultados
    mensaje = (
        "RESULTADOS - METODO DE MONTECARLO PARA PI\n"
        f"Puntos generados: {n}\n"
        f"Puntos dentro del circulo: {total_dentro}\n"
        f"Aproximacion de pi: {pi_aprox:.5f}\n"
        f"Imagen guardada en: {ruta_img}"
    )

    return {
        "puntos_generados": n,
        "puntos_dentro": int(total_dentro),
        "pi_aproximado": pi_aprox,
        "ruta_imagen": ruta_img,
        "mensaje": mensaje
    }

# --- Ejecucion segura ---
if __name__ == "__main__":
    try:
        resultados = estimar_pi_montecarlo()
        print(resultados["mensaje"])
    except Exception as e:
        print("Error en la simulacion:", str(e))
