from pulp import *

def two_phase_simplex(restricciones, signos, funcion_objetivo, tipo):
    # Crear un problema de optimización
    prob = LpProblem("Simplex Dos Fases", LpMaximize if tipo == "maximizar" else LpMinimize)

    # Variables de decisión
    variables = LpVariable.dicts("x", range(len(funcion_objetivo)))

    # Variables de holgura para la segunda fase (si es necesario)
    slack_vars = LpVariable.dicts("s", range(len(restricciones)), lowBound=0)

    # Función objetivo
    prob += lpSum([int(funcion_objetivo[i]) * variables[i] for i in range(len(funcion_objetivo))])

    # Restricciones de igualdad
    for i in range(len(restricciones)):
        constraint = lpSum([int(restricciones[i][j]) * variables[j] for j in range(len(funcion_objetivo))])
        if signos[i] == "=":
            prob += constraint == int(restricciones[i][-1])
        elif signos[i] == "<=":
            prob += constraint <= int(restricciones[i][-1])
        elif signos[i] == ">=":
            prob += constraint >= int(restricciones[i][-1])

    # Resolver el problema de la primera fase para encontrar una solución básica factible
    prob.solve()

    # Si la solución no es factible, resolver el problema de la segunda fase
    if LpStatus[prob.status] != "Optimal":
        # Crear un nuevo problema de optimización para la segunda fase
        prob2 = LpProblem("Simplex Dos Fases - Segunda Fase", LpMaximize if tipo == "maximizar" else LpMinimize)

        # Función objetivo para la segunda fase
        if tipo == "maximizar":
            prob2 += lpSum([int(restricciones[i][-1]) * slack_vars[i] for i in range(len(restricciones))])
        else:
            prob2 += lpSum([int(restricciones[i][-1]) * slack_vars[i] for i in range(len(restricciones))])

        # Restricciones de igualdad para la segunda fase
        for i in range(len(restricciones)):
            constraint = lpSum([int(restricciones[i][j]) * variables[j] for j in range(len(funcion_objetivo))])
            prob2 += constraint + slack_vars[i] == int(restricciones[i][-1])

        # Resolver el problema de la segunda fase
        prob2.solve()

        # Recolectar resultados de la segunda fase
        status2 = LpStatus[prob2.status]
        valor_optimo2 = value(prob2.objective)
        resultados2 = {v.name: v.varValue for v in prob2.variables()}
        
        return status2, valor_optimo2, resultados2
    else:
        # Recolectar resultados de la primera fase si la solución es factible
        status = LpStatus[prob.status]
        valor_optimo = value(prob.objective)
        resultados = {v.name: v.varValue for v in prob.variables()}
        
        return status, valor_optimo, resultados

# Ejemplo de uso

#restricciones = [['2', '0', '12'], ['1', '1', '8'], ['0', '1', '8']]
#signos = ['=', '>=', '<=']
#funcion_objetivo = ['5', '8']
#tipo = "maximizar"  # Cambiar a "minimizar" para problemas de minimización

#status, valor_optimo, resultados = two_phase_simplex(restricciones, signos, funcion_objetivo, tipo)
#print("Estado:", status)
#print("Valor óptimo:", valor_optimo)
#print("Resultados:")
#for var, val in resultados.items():
#    print(var, "=", val)



