"""
============================================================
PRUEBA DE AJUSTE — KOLMOGOROV-SMIRNOV (Distribución Weibull)
------------------------------------------------------------
Propósito:
    Verificar si un conjunto de datos puede considerarse
    proveniente de una distribución Weibull con parámetros
    dados (alfa, beta), utilizando el método de Kolmogorov-Smirnov.

Contexto de aplicación:
    Este método es útil en simulación y análisis de confiabilidad
    (tiempos de vida, fallas, duraciones), donde se desea evaluar
    el ajuste de los datos experimentales a una distribución teórica.


============================================================
"""

import numpy as np
import math
import matplotlib.pyplot as plt


# --- 1. Datos de entrada ---
datos = np.array([
    4.33, 9.97, 2.81, 4.34, 1.36, 1.61, 7.86, 14.39, 1.76, 3.53,
    2.16, 5.49, 3.44, 2.30, 6.58, 2.88, 0.98, 9.92, 5.24, 1.46,
    0.70, 4.52, 4.38, 11.65, 8.42, 0.44, 2.12, 8.04, 10.92, 3.69,
    1.59, 4.44, 2.18, 12.16, 2.44, 2.15, 0.82, 6.19, 6.60, 0.28,
    8.59, 6.96, 4.48, 0.85, 1.90, 7.36, 3.04, 9.66, 4.82, 2.89
])

# --- 2. Parámetros del modelo Weibull ---
alpha = 1.38   # parámetro de forma
beta = 5.19    # parámetro de escala

# --- 3. Configuración de intervalos ---
m = 8          # número de intervalos
A = 2          # amplitud por intervalo
bins = np.arange(0, m * A + 2, A)

# --- 4. Cálculo de frecuencias observadas ---
Oi, _ = np.histogram(datos, bins=bins)
Ni = np.cumsum(Oi)
POi = Oi / len(datos)
POAi = Ni / len(datos)

# --- 5. Cálculo de probabilidades esperadas acumuladas (Weibull) ---
lim_sup = bins[1:]
PEAi = 1 - np.exp(-((lim_sup / beta) ** alpha))

# --- 6. Estadístico KS ---
diferencias = np.abs(POAi - PEAi)
c = np.max(diferencias)

# --- 7. Mostrar resultados en tabla ---
print("\nPRUEBA DE KOLMOGOROV–SMIRNOV — DISTRIBUCIÓN WEIBULL")
print("----------------------------------------------------------")
print(f"{'Intervalo':<10} {'Oi':<5} {'POi':<8} {'POAi':<8} {'PEAi':<8} {'|POAi-PEAi|':<10}")
print("-"*65)
for i in range(len(Oi)):
    intervalo = f"{bins[i]:.0f}-{bins[i+1]:.0f}"
    print(f"{intervalo:<10} {Oi[i]:<5} {POi[i]:<8.4f} {POAi[i]:<8.4f} {PEAi[i]:<8.4f} {diferencias[i]:<10.4f}")
print("-"*65)
print(f"Estadístico KS (c) = {c:.4f}")
print("----------------------------------------------------------")

# --- 8. Valor crítico (α = 0.05) ---
n = len(datos)
D_critico = 1.36 / math.sqrt(n)
print(f"Valor crítico (α=0.05): {D_critico:.4f}")

# --- 9. Conclusión ---
if c < D_critico:
    print("✅ No se rechaza H₀: Los datos siguen la distribución Weibull.")
else:
    print("❌ Se rechaza H₀: Los datos no siguen la distribución Weibull.")

# --- 10. Histograma ---
plt.figure(figsize=(8, 5))
plt.hist(datos, bins=bins, edgecolor='black', color='lightblue', alpha=0.7)
plt.title("Histograma de frecuencias — Prueba de Kolmogorov–Smirnov (Weibull)")
plt.xlabel("Intervalos")
plt.ylabel("Frecuencia")
plt.grid(axis="y", alpha=0.75)
plt.xticks(bins)
plt.tight_layout()
plt.savefig("static/img/kolmogorov_weibull.png")  # para uso en hosting
plt.close()
