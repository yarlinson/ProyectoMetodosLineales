import numpy as np
from pulp import *

class MetodoSimplex:
    def __init__(self):
        pass

    def listas_a_matrices(self, restricciones, funcion_objetivo):
        A = np.array(restricciones, dtype=float)
        b = A[:, -1]
        A = A[:, :-1]
        c = np.array(funcion_objetivo, dtype=float)
        return A, b, c

    def crear_tabla(self, A, b, c):
        m, n = A.shape
        tabla = np.zeros((m + 1, m + n + 1))
        tabla[:-1, :-1] = np.hstack([A, np.eye(m)])
        tabla[:-1, -1] = b
        tabla[-1, :n] = -c  # Modificación aquí
        tabla[-1, -1] = 0
        return tabla

    def imprimir_tabla(self, tabla, iteracion):
        print(f"Iteración {iteracion}:\n{tabla}\n")

    def encontrar_columna_pivote(self, tabla):
        columna_pivote = np.argmin(tabla[-1, :-1])
        return columna_pivote

    def encontrar_fila_pivote(self, tabla, columna_pivote):
        ratios = tabla[:-1, -1] / tabla[:-1, columna_pivote]
        fila_pivote = np.argmin(ratios)
        return fila_pivote

    def actualizar_tabla(self, tabla, fila_pivote, columna_pivote):
        m, n = tabla.shape
        tabla[fila_pivote] = tabla[fila_pivote] / tabla[fila_pivote, columna_pivote]
        for i in range(m):
            if i == fila_pivote:
                continue
            tabla[i] = tabla[i] - tabla[i, columna_pivote] * tabla[fila_pivote]
        return tabla

    def verificar_optimalidad(self, tabla):
        return np.all(tabla[-1, :-1] >= 0)

    def resolver_simplex(self, restricciones, funcion_objetivo):
        A, b, c = self.listas_a_matrices(restricciones, funcion_objetivo)
        tabla = self.crear_tabla(A, b, c)
        iteraciones = [tabla.copy()] 
        iteracion = 0

        self.imprimir_tabla(tabla, iteracion)
        while not self.verificar_optimalidad(tabla):
            iteracion += 1
            columna_pivote = self.encontrar_columna_pivote(tabla)
            fila_pivote = self.encontrar_fila_pivote(tabla, columna_pivote)
            tabla = self.actualizar_tabla(tabla, fila_pivote, columna_pivote)
            self.imprimir_tabla(tabla, iteracion)
            iteraciones.append(tabla.copy())
        print(iteraciones)
        return iteraciones
    
def resolver_problema_optimizacion(N_str, coeficientes_objetivo_str, restricciones_str):
    # Convertir los datos de cadena a enteros
    N = int(N_str)
    
    # Manejo de excepciones para la conversión de coeficientes objetivos
    try:
        coeficientes_objetivo = [int(coef.strip()) for coef in coeficientes_objetivo_str]
    except ValueError:
        print("Error: No se pudieron convertir todos los coeficientes objetivos a enteros.")
        return None
    
    restricciones = []
    for restr in restricciones_str:
        try:
            restriccion = [int(val.strip()) for val in restr]
            restricciones.append(restriccion)
        except ValueError:
            print(f"Error: No se pudo convertir la restricción '{restr}' a números enteros. Se omitirá esta restricción.")
            continue

    # Crear un problema de optimización
    problema = LpProblem("PROBLEMA_DE_OPTIMIZACION_LINEAL", LpMaximize)

    # Crear variables dinámicamente y agregarlas a una lista
    variables = [LpVariable(f"X{i}", lowBound=0, cat='Integer') for i in range(1, N+1)]

    # Función objetivo
    problema += lpSum(coeficientes_objetivo[i] * variables[i] for i in range(N))

    # Restricciones
    for restriccion in restricciones:
        problema += lpSum(restriccion[i] * variables[i] for i in range(N)) <= restriccion[-1]

    # Resolver el problema
    problema.solve()

    # Imprimir el resultado
    resultados = {}
    for variable in variables:
        resultados[variable.name] = variable.varValue
    print(resultados)
    return resultados

# Ejemplo de uso

if __name__ == "__main__":
    N_str = 2
    coeficientes_objetivo_str = ['10', '20']
    restricciones_str = [['3', '1', '90'], ['1', '1', '50'], ['0', '1', '35']]

    resultados = resolver_problema_optimizacion(N_str, coeficientes_objetivo_str, restricciones_str)
    if resultados is not None:
        for variable, valor in resultados.items():
            print(f"El óptimo se obtiene con {variable} = {valor}")
 