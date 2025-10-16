"""
=========================================
ALGORITMO : Generador Congruencial Lineal (LCG)
-----------------------------------------
Propósito:
    Generar una secuencia de números pseudoaleatorios uniformes
    mediante el método congruencial lineal.

Contexto de aplicación:
    Es uno de los generadores más usados en simulaciones, juegos,
    criptografía básica y generación de muestras aleatorias.

Descripción:
    - Se utiliza la fórmula:
          Xₙ₊₁ = (a * Xₙ + c) mod m
    - Luego se normaliza cada valor dividiéndolo entre m:
          Uₙ = Xₙ / m
    - No usa `input()` y está preparado para ejecutarse en entornos web.
=========================================
"""

class GeneradorCongruencial:
    def __init__(self, a, X0, c, m):
        self.a = a      # Multiplicador
        self.X0 = X0    # Semilla
        self.c = c      # Incremento
        self.m = m      # Módulo

    def generar(self, n_iteraciones):
        """Genera y muestra la secuencia congruencial."""
        Xn = self.X0
        resultados = []

        print("n\tXn\t\tUn")
        print(f"0\t{Xn}\t\t--")

        for i in range(1, n_iteraciones + 1):
            Xn = (self.a * Xn + self.c) % self.m
            Un = Xn / self.m
            resultados.append(Un)
            print(f"{i}\t{Xn}\t\t{Un:.4f}")

        print("\nSecuencia generada:")
        print(resultados)
        return resultados


# ===== Ejecución con valores fijos =====
# Ejemplo clásico de parámetros LCG
a = 5       # Multiplicador
X0 = 7      # Semilla
c = 3       # Incremento
m = 7       # Módulo
n_iter = 10 # Cantidad de valores a generar

generador = GeneradorCongruencial(a, X0, c, m)
generador.generar(n_iter)
