"""
============================================================
PRUEBA DE SERIES — INDEPENDENCIA DE NÚMEROS ALEATORIOS
------------------------------------------------------------
Propósito:
    Evaluar si una secuencia de números pseudoaleatorios
    es independiente (no correlacionada) mediante la prueba
    de series de pares consecutivos (rᵢ, rᵢ₊₁).

Fundamento:
    Si los números son verdaderamente independientes,
    los pares (rᵢ, rᵢ₊₁) deberían distribuirse de forma
    uniforme sobre el cuadrado [0,1)x[0,1).

Hipótesis:
    H₀: Los números son independientes.
    H₁: Los números NO son independientes.


"""

import numpy as np
import matplotlib.pyplot as plt

# --- Tabla de valores críticos χ² (α = 0.05) ---
CHI2_CRITICOS_005 = {
    1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
    6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
    11: 19.675, 12: 21.026, 13: 22.362, 14: 23.685, 15: 24.996,
    16: 26.296, 17: 27.587, 18: 28.869, 19: 30.144, 20: 31.410,
    21: 32.671, 22: 33.924, 23: 35.172, 24: 36.415, 25: 37.652,
    26: 38.885, 27: 40.113, 28: 41.337, 29: 42.557, 30: 43.773
}

# ============================================================
# Funciones
# ============================================================

def leer_datos(archivo: str):
    """Lee un archivo de texto con números separados por espacio o salto de línea."""
    with open(archivo, "r") as f:
        return [float(x) for x in f.read().split()]


def prueba_series(datos, alpha=0.05, mostrar_pares=False):
    """
    Aplica la prueba de series usando numpy para eficiencia.

    Parámetros:
        datos : list[float]
            Secuencia de números en (0,1).
        alpha : float
            Nivel de significancia.
        mostrar_pares : bool
            Si es True, muestra todos los pares generados.

    Retorna:
        dict : resultados principales (chi² calculado, gl, decisión).
    """
    n = len(datos)
    pares = [(datos[i], datos[i + 1]) for i in range(n - 1)]
    m = int(round(n ** 0.5))  # número de intervalos por eje

    # --- Matriz de frecuencias observadas ---
    O = np.zeros((m, m), dtype=int)
    for x, y in pares:
        i = min(int(x * m), m - 1)
        j = min(int(y * m), m - 1)
        O[i, j] += 1

    # --- Frecuencia esperada por celda ---
    E = (n - 1) / (m * m)
    chi2_calc = np.sum((O - E) ** 2 / E)
    gl = m * m - 1

    # --- Valor crítico ---
    chi2_crit = CHI2_CRITICOS_005.get(gl, None)

    # --- Mostrar resultados ---
    print("\n=== PRUEBA DE SERIES ===")
    print(f"Número de datos: {n}")
    print(f"Número de pares: {len(pares)}")
    print(f"Casillas por eje (m): {m}")
    print(f"Frecuencia esperada (E): {E:.4f}")
    print(f"Chi² calculado: {chi2_calc:.4f}")
    print(f"Grados de libertad: {gl}")

    if chi2_crit:
        print(f"Chi² crítico (α={alpha}): {chi2_crit}")
        if chi2_calc <= chi2_crit:
            decision = "✅ Se acepta H₀: Los números son independientes."
        else:
            decision = "❌ Se rechaza H₀: Los números son dependientes."
        print(decision)
    else:
        decision = "⚠ No hay valor crítico precargado para gl = " + str(gl)
        print(decision)

    # --- Mostrar pares opcional ---
    if mostrar_pares:
        print("\nPares (rᵢ, rᵢ₊₁):")
        for i, (a, b) in enumerate(pares, start=1):
            print(f"{i:>3}: ({a:.4f}, {b:.4f})")

    # --- Gráfico de dispersión ---
    x_vals, y_vals = zip(*pares)
    plt.figure(figsize=(6, 6))
    plt.scatter(x_vals, y_vals, c="red", marker="o", alpha=0.6)
    plt.title("Prueba de Series — Dispersión de Pares Consecutivos")
    plt.xlabel("r(i)")
    plt.ylabel("r(i+1)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("static/img/series_test.png")
    plt.close()

    # --- Retornar resultados para usar en GUI o reporte ---
    return {
        "chi2_calc": chi2_calc,
        "gl": gl,
        "chi2_crit": chi2_crit,
        "decision": decision,
    }


# ============================================================
# Ejecución directa
# ============================================================
if __name__ == "__main__":
    datos = leer_datos("datos_tarea_estadistica_comput.txt")
    prueba_series(datos, alpha=0.05, mostrar_pares=False)
