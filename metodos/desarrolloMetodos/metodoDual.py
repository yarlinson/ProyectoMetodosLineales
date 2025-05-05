import numpy as np
from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, lpSum, value, LpStatus

def simplex_dual_pulp(restricciones, signos, funcion_objetivo, tipo):
    
    
    
    # Convertir las entradas de cadenas de texto a números
    A = [[float(num) for num in restriccion[:-1]] for restriccion in restricciones]
    b = [float(restriccion[-1]) for restriccion in restricciones]
    c = [float(num) for num in funcion_objetivo]

    # Definir el problema de PuLP
    prob = LpProblem("Simplex Dual", LpMinimize if tipo == "minimizar" else LpMaximize)
    
    # Crear las variables de decisión
    variables = [LpVariable(f'x{i}', lowBound=0) for i in range(len(c))]
    
    # Crear las restricciones
    for i in range(len(A)):
        if signos[i] == ">=":
            prob += lpSum(A[i][j] * variables[j] for j in range(len(c))) >= b[i]
        else:
            prob += lpSum(A[i][j] * variables[j] for j in range(len(c))) <= b[i]
    
    # Crear la función objetivo
    prob += lpSum(c[i] * variables[i] for i in range(len(c)))
    
    # Resolver el problema
    prob.solve()
    
    # Obtener los resultados
    estado = LpStatus[prob.status]
    valor_optimo = value(prob.objective)
    valores_variables = {v.name: v.varValue for v in prob.variables()}
    
    # Retornar los resultados
    return {
        "Estado de la solución": estado,
        "Valor óptimo": valor_optimo,
        "Valores de las variables": valores_variables
    }

class Simplex:
    def __init__(self, restricciones, signos, funcion_objetivo, tipo):
        self.restricciones = restricciones
        self.signos = signos
        self.funcion_objetivo = funcion_objetivo
        self.tipo = tipo
        self.totalHolguras = len(restricciones)
        self.cantHolguras = 0
        self.matriz_final_np = None
        self.matrices_resultado = []

    def preparar_datos(self):
        self.funcion_objetivo = [-1 * float(val) for val in self.funcion_objetivo]
        self.restricciones = [list(map(float, restr)) for restr in self.restricciones]
        self.funcion_objetivo = list(map(float, self.funcion_objetivo))

        for i in range(len(self.restricciones)):
            if self.signos[i] == '>=':
                self.cantHolguras += 1
                self.restricciones[i] = [-1 * float(val) for val in self.restricciones[i]] 
                for j in range(self.cantHolguras - 1):
                    self.restricciones[i].insert(-1, 0)
                self.restricciones[i].insert(-1, -1)
                for j in range(self.totalHolguras - (self.cantHolguras - 1) - 1):
                    self.restricciones[i].insert(-1, 0)
                self.signos[i] = '='
            elif self.signos[i] == '<=':
                self.cantHolguras += 1
                self.restricciones[i] = [1 * float(val) for val in self.restricciones[i]]
                for j in range(self.cantHolguras - 1):
                    self.restricciones[i].insert(-1, 0)
                self.restricciones[i].insert(-1, 1)
                for j in range(self.totalHolguras - (self.cantHolguras - 1) - 1):
                    self.restricciones[i].insert(-1, 0)
                self.signos[i] = '='
            self.funcion_objetivo.append(0)
        self.funcion_objetivo.append(0)
        self.crear_matriz_final()

    def crear_matriz_final(self):
        matriz_final = [self.funcion_objetivo] + self.restricciones
        self.matriz_final_np = np.array(matriz_final, dtype=float)
        self.matrices_resultado.append(self.matriz_final_np.copy())  # Guardar la matriz inicial

    def resolver(self):
        iteration = 1
        while np.any(self.matriz_final_np[1:, -1] < 0):
           
            iteration += 1

            ultima_columna = self.matriz_final_np[1:, -1]
            fila_pivote = np.argmin(ultima_columna) + 1
           

            ratios = []
            for j in range(len(self.funcion_objetivo) - 1):
                if self.matriz_final_np[fila_pivote][j] != 0 and self.matriz_final_np[fila_pivote][j] != -1 and self.matriz_final_np[fila_pivote][j] != 1:
                    ratio = abs(self.matriz_final_np[0][j] / self.matriz_final_np[fila_pivote][j])
                    if self.matriz_final_np[0][j] != 0:
                        ratios.append((ratio, j))

            if not ratios:
                print("No hay soluciones factibles.")
                break

            columna_pivote = min(ratios)[1]
            

            valor_pivote = self.matriz_final_np[fila_pivote, columna_pivote]
            

            if valor_pivote != 1:
                self.matriz_final_np[fila_pivote] /= valor_pivote

            

            for i in range(len(self.matriz_final_np)):
                if i != fila_pivote:
                    fila_factor = self.matriz_final_np[i, columna_pivote]
                    self.matriz_final_np[i] -= fila_factor * self.matriz_final_np[fila_pivote]

            self.matrices_resultado.append(self.matriz_final_np.copy())  # Guardar matriz después de Gauss-Jordan

            
        
        
        
        return self.matrices_resultado
    


def main():
    restricciones = [['10', '0', '100'], ['100', '200', '8000'], ['250', '300', '15000']]
    signos = ['>=', '>=', '<=']
    funcion_objetivo = ['500', '600']
    tipo = "minimizar"

    simplex = Simplex(restricciones, signos, funcion_objetivo, tipo)
    simplex.preparar_datos()
    matrices_resultado = simplex.resolver()

    print(matrices_resultado)
if __name__ == "__main__":
    main()




