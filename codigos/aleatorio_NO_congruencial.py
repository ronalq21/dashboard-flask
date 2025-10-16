"""
=========================================
ALGORITMO : Método de los Cuadrados Medios
-----------------------------------------
Propósito:
    Generar una secuencia de números pseudoaleatorios
    utilizando el método de los cuadrados medios.

Contexto de aplicación:
    Este método fue uno de los primeros generadores
    de números pseudoaleatorios usados en simulaciones
    y experimentos computacionales.

Descripción:
    - Se eleva al cuadrado la semilla inicial.
    - Se extraen los dígitos centrales para formar la nueva semilla.
    - Cada valor generado (r_i) se normaliza entre 0 y 1.
    - No se usa `input()` ni interfaces gráficas, para compatibilidad
      con servidores web.
=========================================
"""
"""
    Genera una secuencia de números pseudoaleatorios
    con el método de los cuadrados medios.

    Parámetros:
        semilla (int): valor inicial X0
        d (int): cantidad de dígitos en la semilla
        n (int): cantidad de números a generar

    Retorna:
        list: lista de valores pseudoaleatorios normalizados
    """

def cuadrados_medios(semilla, d, n):
    
    x = semilla
    resultados = []

    print("Método de los Cuadrados Medios")
    print(f"Semilla inicial: X0 = {semilla}")
    print("Yi\t\tXi\t\tri")

    for i in range(1, n + 1):
        y = x * x
        y_str = str(y).zfill(2 * d)  # Asegura longitud 2d

        inicio = (len(y_str) - d) // 2
        x_str = y_str[inicio:inicio + d]
        x = int(x_str)

        r = x / (10 ** d)
        resultados.append(r)

        print(f"Y{i-1} = {y_str}  X{i} = {x_str}  r{i} = {r:.4f}")

    print("\nSecuencia Generada:")
    print(resultados)
    return resultados


# ===== Ejecución (valores fijos, sin input) =====
semilla = 5735
d = 4
n = 5

cuadrados_medios(semilla, d, n)
