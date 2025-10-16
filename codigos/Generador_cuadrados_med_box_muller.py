"""
=========================================
ALGORITMO : Generación de Datos Normales
(Cuadrados Medios + Transformación de Box–Muller)
-----------------------------------------
Propósito:
    Generar una muestra de números pseudoaleatorios con distribución
    normal (media 0, varianza 1) utilizando el método de los cuadrados
    medios como generador base y la transformación Box–Muller.

Contexto de aplicación:
    Este tipo de generadores se utiliza en simulaciones estadísticas,
    estudios de variabilidad experimental y modelado de fenómenos
    con comportamiento normal.

Descripción:
    - Se genera una secuencia uniforme con el método de los cuadrados medios.
    - Se aplica la transformación Box–Muller para obtener valores normales.
    - Los resultados se guardan en archivo y se genera una gráfica como imagen.
    - No usa `input()` ni `plt.show()` para compatibilidad web.
=========================================
"""

import matplotlib.pyplot as plt
import math

class Aleatorio:
    def __init__(self, x0, n, d=4):
        """
        x0 : semilla (entero)
        n  : cantidad de números normales a generar
        d  : cantidad de dígitos de precisión del generador base
        """
        self.x0 = x0
        self.n = n
        self.d = d

    def cuadrados_medios(self, cantidad):
        """Genera números pseudoaleatorios U(0,1) mediante cuadrados medios."""
        numeros = []
        x = self.x0
        for _ in range(cantidad):
            x_cuadrado = str(x**2).zfill(2*self.d)
            inicio = (len(x_cuadrado) - self.d) // 2
            x = int(x_cuadrado[inicio:inicio+self.d])
            numeros.append(x / (10**self.d))
        return numeros

    def generar_normal(self):
        """Genera números con distribución normal usando Box–Muller."""
        uniformes = self.cuadrados_medios(2 * self.n)
        normales = []

        for i in range(0, len(uniformes), 2):
            u1, u2 = uniformes[i], uniformes[i+1]
            if u1 == 0:  # evitar log(0)
                u1 = 1e-10
            z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            normales.append(z1)
            if len(normales) < self.n:
                normales.append(z2)
        return normales

    def graficar(self, datos, ruta_guardado="static/img/normal_cm.png"):
        """Genera y guarda el histograma de los datos generados."""
        plt.hist(datos, bins=20, density=True, edgecolor="black", color="skyblue")
        plt.title("Distribución Aproximada Normal Generada (Box–Muller)")
        plt.xlabel("Valor")
        plt.ylabel("Densidad")
        plt.grid(alpha=0.3)
        plt.savefig(ruta_guardado)
        plt.close()
        print(f"Gráfico guardado en: {ruta_guardado}")

    def guardar_en_txt(self, datos, nombre_archivo="numeros_normales.txt"):
        """Guarda los datos generados en un archivo de texto."""
        with open(nombre_archivo, "w") as f:
            for num in datos:
                f.write(f"{num}\n")
        print(f"Números aleatorios guardados en: {nombre_archivo}")


# ===== Ejecución (valores fijos, sin input) =====
semilla = 5735       # semilla inicial
cantidad = 100       # cantidad de números normales
generador = Aleatorio(semilla, cantidad)

datos = generador.generar_normal()
generador.graficar(datos)
generador.guardar_en_txt(datos)

print("Primeros 5 valores generados:", datos[:5])
