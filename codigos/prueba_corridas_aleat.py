"""
============================================================
PRUEBA DE CORRIDAS (RUN TEST) PARA ALEATORIEDAD
------------------------------------------------------------
Propósito:
    Verificar si una secuencia de números pseudoaleatorios
    presenta independencia entre valores consecutivos,
    evaluando los "aumentos" y "disminuciones".

Pasos:
    1 Se compara cada número con el anterior.
         - Si aumenta → 1
         - Si no aumenta → 0
    2 Se cuentan las "corridas": cambios de 0 → 1 o 1 → 0
    3 Se obtiene el número total de corridas C = len(Cambios) + 1
============================================================
"""

def compar(lista):
    """
    Genera una lista binaria S indicando si cada elemento
    es mayor (1) o menor/igual (0) que el anterior.
    """
    S = []
    for i in range(1, len(lista)):
        if lista[i] > lista[i-1]:
            S.append(1)
        else:
            S.append(0)
    return S


def corridas(S):
    """
    Cuenta las corridas (cambios entre 0 y 1 consecutivos).
    """
    C = []
    for i in range(len(S) - 1):
        if S[i] != S[i + 1]:
            C.append(1)
    return C


# --- Ejemplo de datos ---
r = [0.89, 0.26, 0.01, 0.98, 0.13, 0.12, 0.69, 0.11, 0.05, 0.65,
     0.21, 0.04, 0.03, 0.11, 0.07, 0.97, 0.27, 0.12, 0.95, 0.02, 0.06]

# --- Paso 1: Generar secuencia comparativa ---
S = compar(r)
print("S =", S)

# --- Paso 2: Contar corridas ---
C = corridas(S)
num_corridas = len(C) + 1
print(f"Número total de corridas (C) = {num_corridas}")

# --- Paso 3 (opcional): Evaluación estadística ---
# Si deseas comparar con el valor esperado de corridas bajo H0:
n = len(S)
esperado = (2 * n - 1) / 3
varianza = (16 * n - 29) / 90
Z = (num_corridas - esperado) / (varianza ** 0.5)

print(f"Valor esperado de corridas (E[C]) = {esperado:.3f}")
print(f"Varianza teórica (Var[C]) = {varianza:.3f}")
print(f"Estadístico Z = {Z:.3f}")

# Interpretación (nivel de significancia 5%)
if abs(Z) < 1.96:
    print("✅ No se rechaza H₀ → Los números parecen aleatorios.")
else:
    print("❌ Se rechaza H₀ → La secuencia no es aleatoria.")
