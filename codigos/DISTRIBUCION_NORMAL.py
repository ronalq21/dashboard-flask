"""
=========================================
ALGORITMO : Generación de Datos Normales (Box–Muller)
-----------------------------------------
Propósito:
    Generar una muestra de datos con distribución normal (N(μ, σ²))
    usando un generador congruencial lineal (LCG) y la transformación
    de Box–Muller.

Contexto de aplicación:
    Este método se utiliza ampliamente en simulaciones, modelado estadístico
    y generación de datos aleatorios con comportamiento gaussiano.

Descripción:
    - Se usa un LCG para producir números uniformes U(0,1).
    - Se transforman esos valores mediante Box–Muller para obtener
      una distribución normal estándar.
    - Se aplica la prueba de Kolmogorov–Smirnov (KS) para verificar
      la normalidad.
    - La gráfica se guarda como archivo (sin plt.show()) para compatibilidad web.
=========================================
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm

class GeneradorNormal:
    def __init__(self, semilla):
        # Parámetros del LCG
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.x = semilla

    def _uniforme(self):
        """Genera un número uniforme U(0,1) usando LCG."""
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m

    def generar_muestra(self, n, mu, sigma):
        """Genera una muestra normal de tamaño n con media mu y desviación sigma."""
        datos = []
        for _ in range(n // 2):
            u1 = self._uniforme()
            u2 = self._uniforme()
            R = math.sqrt(-2 * math.log(u1))
            theta = 2 * math.pi * u2
            z1 = R * math.cos(theta)
            z2 = R * math.sin(theta)
            datos.append(mu + sigma * z1)
            datos.append(mu + sigma * z2)
        return np.array(datos[:n])

    def verificar_normalidad(self, muestra, mu, sigma):
        """Aplica la prueba KS para verificar la normalidad de la muestra."""
        ks_stat, p_valor = kstest(muestra, 'norm', args=(mu, sigma))
        print("\nVerificación de normalidad")
        print(f"Estadístico KS = {ks_stat:.5f}")
        print(f"Valor-p = {p_valor:.5f}")

        if p_valor > 0.05:
            interpretacion = "No se rechaza la normalidad (p > 0.05)"
        else:
            interpretacion = "Se rechaza la normalidad (p ≤ 0.05)"

        print("Interpretación:", interpretacion)
        return ks_stat, p_valor, interpretacion

    def graficar_normal(self, muestra, mu, sigma, ruta_guardado="static/img/normal1.png"):
        """Genera y guarda el histograma comparado con la curva teórica normal."""
        plt.figure(figsize=(8, 5))
        plt.hist(muestra, bins=20, density=True, alpha=0.6,
                 color='skyblue', edgecolor='black', label='Muestra simulada')

        x = np.linspace(min(muestra), max(muestra), 200)
        y = norm.pdf(x, mu, sigma)
        plt.plot(x, y, 'r', linewidth=2, label=f'N({mu}, {sigma}²) teórica')

        plt.title("Simulación de Datos Normales")
        plt.xlabel("Valores")
        plt.ylabel("Densidad")
        plt.legend()
        plt.grid(alpha=0.3)

        # Guardar imagen en carpeta accesible desde Flask
        plt.savefig(ruta_guardado)
        plt.close()
        print(f"Gráfico guardado en: {ruta_guardado}")


# ===== Ejecución (valores fijos, sin input) =====
semilla = 123456789
n = 200
mu = 0
sigma = 1

gen = GeneradorNormal(semilla)
muestra = gen.generar_muestra(n, mu, sigma)

print("Primeros 5 valores generados:", muestra[:5])
gen.verificar_normalidad(muestra, mu, sigma)
gen.graficar_normal(muestra, mu, sigma)
