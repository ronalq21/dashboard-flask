"""
=========================================
ALGORITMO : Generador Normal (LCG + Box–Muller)
-----------------------------------------
Propósito:
    Generar una muestra de números pseudoaleatorios con distribución
    normal estándar (media 0, desviación 1) usando un LCG como generador
    uniforme y la transformación de Box–Muller.

Contexto de aplicación:
    Simulaciones Monte Carlo, pruebas estadísticas, generación de datos
    sintéticos para modelos que requieren ruido gaussiano.

Descripción técnica:
    - Se genera una secuencia uniforme U(0,1) con un LCG (parámetros por defecto: a=16807, m=2^31-1).
    - Se aplican pares de uniformes a la transformación de Box–Muller
      para obtener variables normales N(0,1).
    - Se normalizan los valores para garantizar media ≈ 0 y sigma ≈ 1.
    - Se guarda un histograma como imagen (ruta por defecto: static/img/normal_lcg.png)
      y los números en un archivo de texto (ruta por defecto: numeros_normales.txt).
    - No utiliza input() ni muestra ventanas gráficas (compatible con hosting web).
=========================================
"""

import math
import matplotlib.pyplot as plt
import os

class Aleatorio:
    def __init__(self, seed, n, a=16807, c=0, m=(2**31 - 1)):
        """
        seed : int   -> semilla inicial del LCG
        n    : int   -> cantidad de números normales a generar
        a,c,m: int   -> parámetros del LCG (por defecto: MINSTD)
        """
        self.seed = int(seed)
        self.n = int(n)
        self.a = int(a)
        self.c = int(c)
        self.m = int(m)

    def lcg(self, cantidad):
        """Generador congruencial lineal: retorna lista de U(0,1)."""
        numeros = []
        x = self.seed
        for _ in range(cantidad):
            x = (self.a * x + self.c) % self.m
            u = x / self.m
            # evitar extremos que provoquen log(0) o 1 exacto
            u = max(min(u, 1 - 1e-12), 1e-12)
            numeros.append(u)
        return numeros

    def generar_normal(self):
        """Genera y normaliza una lista de n números ~N(0,1) usando Box–Muller."""
        uniformes = self.lcg(2 * self.n)
        normales = []
        for i in range(0, len(uniformes), 2):
            u1, u2 = uniformes[i], uniformes[i + 1]
            r = math.sqrt(-2.0 * math.log(u1))
            theta = 2.0 * math.pi * u2
            z1 = r * math.cos(theta)
            z2 = r * math.sin(theta)
            normales.append(z1)
            if len(normales) < self.n:
                normales.append(z2)

        # Normalizar media y desviación estándar
        mu = sum(normales) / len(normales)
        sigma = math.sqrt(sum((x - mu)**2 for x in normales) / len(normales))
        sigma = sigma if sigma != 0 else 1.0
        normales = [(x - mu) / sigma for x in normales]

        return normales

    def graficar_y_guardar(self, datos, ruta_img="static/img/normal_lcg.png", bins=30):
        """Genera y guarda el histograma (sin mostrar ventana)."""
        # Crear carpeta si no existe
        carpeta = os.path.dirname(ruta_img)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

        plt.figure(figsize=(8, 5))
        plt.hist(datos, bins=bins, density=True, edgecolor="black")
        plt.title("Histograma — Números normales (LCG + Box–Muller)")
        plt.xlabel("Valor")
        plt.ylabel("Densidad")
        plt.grid(alpha=0.3)
        plt.savefig(ruta_img)
        plt.close()
        print(f"Gráfico guardado en: {ruta_img}")

    def guardar_en_txt(self, datos, nombre_archivo="numeros_normales.txt", decimales=5):
        """Guarda la muestra normal en un archivo de texto."""
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("Números normales (media~0, sigma~1) generados con LCG + Box-Muller\n")
            for num in datos:
                f.write(f"{num:.{decimales}f}\n")
        print(f"Archivo guardado en: {ruta}")


# ===== Ejecución ejemplo (valores fijos para hosting) =====
if __name__ == "__main__":
    # Valores fijos (evitar input() para que funcione en servidores)
    semilla = 12345
    cantidad = 200

    gen = Aleatorio(seed=semilla, n=cantidad)
    datos = gen.generar_normal()
    gen.graficar_y_guardar(datos, ruta_img="static/img/normal_lcg.png")
    gen.guardar_en_txt(datos, nombre_archivo="numeros_normales.txt")

    print("Primeros 5 valores generados:", datos[:5])
