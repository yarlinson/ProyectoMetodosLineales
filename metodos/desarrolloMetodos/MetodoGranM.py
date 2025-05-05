from pulp import *

def simplex_gran_m(restricciones, signos, funcion_objetivo, tipo):
    # Crear un problema de optimización de PuLP
    problema = LpProblem("Simplex_Gran_M", LpMinimize if tipo == "minimizar" else LpMaximize)
    
    # Definir las variables de decisión
    variables = [LpVariable(f"x{i}", lowBound=0) for i in range(len(funcion_objetivo))]
    
    # Agregar las restricciones al problema
    for i, restriccion in enumerate(restricciones):
        expresion = lpSum(float(restriccion[j]) * variables[j] for j in range(len(funcion_objetivo)))
        if signos[i] == "<=":
            problema += expresion <= float(restriccion[-1])
        elif signos[i] == ">=":
            problema += expresion >= float(restriccion[-1])
        elif signos[i] == "=":
            problema += expresion == float(restriccion[-1])
    
    # Agregar la función objetivo al problema
    objetivo = lpSum(float(funcion_objetivo[i]) * variables[i] for i in range(len(funcion_objetivo)))
    problema += objetivo
    
    # Resolver el problema
    problema.solve()
    
    # Crear un diccionario para almacenar los resultados
    resultados = {}
    
    # Almacenar el estado de la solución
    resultados["estado"] = LpStatus[problema.status]
    
    # Almacenar las variables y sus valores óptimos
    for v in problema.variables():
        resultados[v.name] = v.varValue
    
    # Almacenar el valor óptimo de la función objetivo
    resultados["valor_optimo"] = value(problema.objective)
    
    # Devolver los resultados
    return resultados

# Datos de entrada
#restricciones = [['2', '1', '90'], ['1', '1', '50'], ['1', '0', '10']]
#signos = ['<=', '>=', '<=']
#funcion_objetivo = ['1.5', '2.5']
#tipo = "minimizar"

# Resolver el problema utilizando el método Simplex Gran M
#resultados = simplex_gran_m(restricciones, signos, funcion_objetivo, tipo)
#print(resultados)
