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
        # Filtrar solo coeficientes positivos para evitar división por cero
        coeficientes = tabla[:-1, columna_pivote]
        terminos_independientes = tabla[:-1, -1]
        
        # Encontrar filas con coeficientes positivos
        filas_validas = coeficientes > 1e-10  # Tolerancia para evitar problemas numéricos
        
        if not np.any(filas_validas):
            raise ValueError("No hay solución factible: todos los coeficientes de la columna pivote son no positivos")
        
        # Calcular ratios solo para filas válidas
        ratios = np.full(len(coeficientes), np.inf)
        ratios[filas_validas] = terminos_independientes[filas_validas] / coeficientes[filas_validas]
        
        # Encontrar la fila con el ratio mínimo positivo
        ratios_positivos = ratios[ratios > 0]
        if len(ratios_positivos) == 0:
            raise ValueError("No hay solución factible: todos los ratios son no positivos")
        
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
        # Usar tolerancia para comparaciones numéricas
        return np.all(tabla[-1, :-1] >= -1e-10)

    def resolver_simplex(self, restricciones, funcion_objetivo):
        try:
            A, b, c = self.listas_a_matrices(restricciones, funcion_objetivo)
            
            # Verificar que no hay valores negativos en b
            if np.any(b < 0):
                raise ValueError("El método simplex estándar requiere que todos los términos independientes sean no negativos")
            
            tabla = self.crear_tabla(A, b, c)
            iteraciones = [tabla.copy()] 
            iteracion = 0
            max_iteraciones = 100  # Prevenir bucles infinitos

            self.imprimir_tabla(tabla, iteracion)
            
            while not self.verificar_optimalidad(tabla) and iteracion < max_iteraciones:
                iteracion += 1
                
                # Verificar si hay degeneración (múltiples ratios mínimos)
                columna_pivote = self.encontrar_columna_pivote(tabla)
                fila_pivote = self.encontrar_fila_pivote(tabla, columna_pivote)
                
                # Verificar si el elemento pivote es muy pequeño
                if abs(tabla[fila_pivote, columna_pivote]) < 1e-10:
                    raise ValueError("Elemento pivote muy pequeño, posible degeneración")
                
                tabla = self.actualizar_tabla(tabla, fila_pivote, columna_pivote)
                self.imprimir_tabla(tabla, iteracion)
                iteraciones.append(tabla.copy())
            
            if iteracion >= max_iteraciones:
                raise ValueError("Se alcanzó el número máximo de iteraciones. El problema puede ser no acotado o degenerado")
            
            print(f"Simplex completado en {iteracion} iteraciones")
            return iteraciones
            
        except Exception as e:
            print(f"Error en el método simplex: {str(e)}")
            raise
    
def resolver_problema_optimizacion(N_str, coeficientes_objetivo_str, restricciones_str):
    try:
        # Convertir los datos de cadena a números
        N = int(N_str)
        
        # Manejo de excepciones para la conversión de coeficientes objetivos
        try:
            coeficientes_objetivo = [float(coef.strip()) for coef in coeficientes_objetivo_str]
        except ValueError:
            print("Error: No se pudieron convertir todos los coeficientes objetivos a números.")
            return None
        
        restricciones = []
        for restr in restricciones_str:
            try:
                restriccion = [float(val.strip()) for val in restr]
                restricciones.append(restriccion)
            except ValueError:
                print(f"Error: No se pudo convertir la restricción '{restr}' a números. Se omitirá esta restricción.")
                continue

        # Crear un problema de optimización
        problema = LpProblem("PROBLEMA_DE_OPTIMIZACION_LINEAL", LpMaximize)

        # Crear variables continuas (no enteras por defecto)
        variables = [LpVariable(f"X{i}", lowBound=0) for i in range(1, N+1)]

        # Función objetivo
        problema += lpSum(coeficientes_objetivo[i] * variables[i] for i in range(N))

        # Restricciones
        for restriccion in restricciones:
            problema += lpSum(restriccion[i] * variables[i] for i in range(N)) <= restriccion[-1]

        # Resolver el problema
        problema.solve()

        # Verificar el estado de la solución
        if problema.status != 1:  # 1 = Optimal
            print(f"Estado de la solución: {LpStatus[problema.status]}")
            return None

        # Obtener los resultados
        resultados = {}
        for variable in variables:
            resultados[variable.name] = variable.varValue if variable.varValue is not None else 0
        
        print(f"Valor óptimo: {value(problema.objective)}")
        print(resultados)
        return resultados
        
    except Exception as e:
        print(f"Error en resolver_problema_optimizacion: {str(e)}")
        return None

# Ejemplo de uso

if __name__ == "__main__":
    N_str = 2
    coeficientes_objetivo_str = ['10', '20']
    restricciones_str = [['3', '1', '90'], ['1', '1', '50'], ['0', '1', '35']]

    resultados = resolver_problema_optimizacion(N_str, coeficientes_objetivo_str, restricciones_str)
    if resultados is not None:
        for variable, valor in resultados.items():
            print(f"El óptimo se obtiene con {variable} = {valor}")
 