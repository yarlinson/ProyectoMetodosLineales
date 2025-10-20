from django.shortcuts import render, redirect
from django.http import HttpResponse
from metodos.desarrolloMetodos.metodoSimplex import *
from metodos.desarrolloMetodos.metodoDual import *
from metodos.desarrolloMetodos.MetodoGranM import *
import os
from django.http import FileResponse, Http404
from django.conf import settings

# Create your views here.

def descargar_archivo_rar(request):
    file_path = os.path.join(os.path.dirname(__file__),'desarrolloMetodos', 'MetodoGraficoEjecutable.rar')  # Ruta al archivo .rar
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='archivo.rar')
    else:
        raise Http404("Archivo no encontrado")

def descargar_archivo(request):
    file_path = os.path.join(os.path.dirname(__file__), 'desarrolloMetodos', 'MetodoGrafico.py')  # Ruta al archivo en la misma carpeta
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='MetodoGrafico.py')
    else:
        raise Http404("Archivo no encontrado")

def index(request):
    return render(request, 'index.html')

def metodogranm(request):
    displayTablas = "none"
    if request.method == 'GET':
        display = "none"
        displayTablas = "none"
        
        return render(request, 'metodogranm.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        display = "block"
        
        if Action == "generarModelo":   
            try:
                cant_restricciones = int(request.POST["restricciones"])
                cant_variables = int(request.POST["variables"])
                tipo = request.POST["tipo"]
                
                cantRestricciones = range(cant_restricciones)
                cantRestriccionesDisminuido = range(cant_restricciones-1)
                cantVa = range(cant_variables-1)
                cantVariables = range(cant_variables)
                
                return render(request, 'metodogranm.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'ocularTablas': displayTablas,
                    'tipo': tipo
                })
            except (ValueError, KeyError) as e:
                return render(request, 'metodogranm.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })
                
        if Action == "Desarrollar":
            try:
                # Obtener datos del POST
                variables_count = int(request.POST.get('variables_count', 0))
                restricciones_count = int(request.POST.get('restricciones_count', 0))
                tipo = request.POST.get('tipo', 'maximizar')
                
                cantVariables = range(variables_count)
                cantRestricciones = range(restricciones_count)
                cantRestriccionesDisminuido = range(restricciones_count-1)
                
                # Recopilar datos de la función objetivo
                datosDelfuncionObjetivo = []
                for i in cantVariables:
                    dato = request.POST.get(f'variablesFuncion_{i}')
                    if dato is None or dato == '':
                        raise ValueError(f"Falta coeficiente para X{i}")
                    datosDelfuncionObjetivo.append(dato)
                
                # Recopilar datos de restricciones
                datosRestricciones = []
                retriccionesIndividuales = []
                signos = []
                
                for j in cantRestricciones:
                    restriccion = []
                    for i in cantVariables:
                        dato = request.POST.get(f'variables_{j}_{i}')
                        if dato is None or dato == '':
                            raise ValueError(f"Falta coeficiente para X{i} en restricción {j+1}")
                        restriccion.append(dato)
                        datosRestricciones.append(dato)
                    
                    # Agregar término independiente
                    datoR = request.POST.get(f'variablesR_{j}')
                    if datoR is None or datoR == '':
                        raise ValueError(f"Falta término independiente en restricción {j+1}")
                    restriccion.append(datoR)
                    datosRestricciones.append(datoR)
                    
                    # Obtener signo
                    signo = request.POST.get(f'signo{j}')
                    if signo is None:
                        raise ValueError(f"Falta signo para restricción {j+1}")
                    signos.append(signo)
                    
                    retriccionesIndividuales.append(restriccion)
                
                # Procesar resultados
                displayTablas = "block"
                resultados = simplex_gran_m(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
                nuevaFuncionZ = list(zip(datosDelfuncionObjetivo, cantVariables))
                
                return render(request, 'metodogranm.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'fucionObjetivo': datosDelfuncionObjetivo,
                    'datosDelModelo': datosRestricciones,
                    'datosDerestricciones': datosRestricciones,
                    'retriccionesIndividuales': retriccionesIndividuales,
                    'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                    'ocularTablas': displayTablas,
                    'nuevaFuncionZ': nuevaFuncionZ,
                    'resultado': resultados,
                    'tipo': tipo
                })
                
            except (ValueError, KeyError) as e:
                return render(request, 'metodogranm.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })

def metododosfases(request):
    displayTablas = "none"
    if request.method == 'GET':
        display = "none"
        displayTablas = "none"
        
        return render(request, 'metododosfases.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        display = "block"
        
        if Action == "generarModelo":   
            try:
                cant_restricciones = int(request.POST["restricciones"])
                cant_variables = int(request.POST["variables"])
                tipo = request.POST["tipo"]
                
                cantRestricciones = range(cant_restricciones)
                cantRestriccionesDisminuido = range(cant_restricciones-1)
                cantVa = range(cant_variables-1)
                cantVariables = range(cant_variables)
                
                return render(request, 'metododosfases.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'ocularTablas': displayTablas,
                    'tipo': tipo
                })
            except (ValueError, KeyError) as e:
                return render(request, 'metododosfases.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })
                
        if Action == "Desarrollar":
            try:
                # Obtener datos del POST
                variables_count = int(request.POST.get('variables_count', 0))
                restricciones_count = int(request.POST.get('restricciones_count', 0))
                tipo = request.POST.get('tipo', 'maximizar')
                
                cantVariables = range(variables_count)
                cantRestricciones = range(restricciones_count)
                cantRestriccionesDisminuido = range(restricciones_count-1)
                
                # Recopilar datos de la función objetivo
                datosDelfuncionObjetivo = []
                for i in cantVariables:
                    dato = request.POST.get(f'variablesFuncion_{i}')
                    if dato is None or dato == '':
                        raise ValueError(f"Falta coeficiente para X{i}")
                    datosDelfuncionObjetivo.append(dato)
                
                # Recopilar datos de restricciones
                datosRestricciones = []
                retriccionesIndividuales = []
                signos = []
                
                for j in cantRestricciones:
                    restriccion = []
                    for i in cantVariables:
                        dato = request.POST.get(f'variables_{j}_{i}')
                        if dato is None or dato == '':
                            raise ValueError(f"Falta coeficiente para X{i} en restricción {j+1}")
                        restriccion.append(dato)
                        datosRestricciones.append(dato)
                    
                    # Agregar término independiente
                    datoR = request.POST.get(f'variablesR_{j}')
                    if datoR is None or datoR == '':
                        raise ValueError(f"Falta término independiente en restricción {j+1}")
                    restriccion.append(datoR)
                    datosRestricciones.append(datoR)
                    
                    # Obtener signo
                    signo = request.POST.get(f'signo{j}')
                    if signo is None:
                        raise ValueError(f"Falta signo para restricción {j+1}")
                    signos.append(signo)
                    
                    retriccionesIndividuales.append(restriccion)
                
                # Procesar resultados
                displayTablas = "block"
                status, valor_optimo, resultados = two_phase_simplex(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
                nuevaFuncionZ = list(zip(datosDelfuncionObjetivo, cantVariables))
                
                return render(request, 'metododosfases.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'fucionObjetivo': datosDelfuncionObjetivo,
                    'datosDelModelo': datosRestricciones,
                    'datosDerestricciones': datosRestricciones,
                    'retriccionesIndividuales': retriccionesIndividuales,
                    'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                    'ocularTablas': displayTablas,
                    'nuevaFuncionZ': nuevaFuncionZ,
                    'resultado': resultados,
                    'Zoptimo': valor_optimo,
                    'tipo': tipo
                })
                
            except (ValueError, KeyError) as e:
                return render(request, 'metododosfases.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })


def metodografico(request):
    return render(request, 'metodografico.html')

def metododual(request):
    displayTablas = "none"
    if request.method == 'GET':
        display = "none"
        displayTablas = "none"
        
        return render(request, 'metododual.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        display = "block"
        
        if Action == "generarModelo":   
            try:
                cant_restricciones = int(request.POST["restricciones"])
                cant_variables = int(request.POST["variables"])
                tipo = request.POST["tipo"]
                
                cantRestricciones = range(cant_restricciones)
                cantRestriccionesDisminuido = range(cant_restricciones-1)
                cantVa = range(cant_variables-1)
                cantVariables = range(cant_variables)
                
                return render(request, 'metododual.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'ocularTablas': displayTablas,
                    'tipo': tipo
                })
            except (ValueError, KeyError) as e:
                return render(request, 'metododual.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })
                
        if Action == "Desarrollar":
            try:
                # Obtener datos del POST
                variables_count = int(request.POST.get('variables_count', 0))
                restricciones_count = int(request.POST.get('restricciones_count', 0))
                tipo = request.POST.get('tipo', 'minimizar')
                
                cantVariables = range(variables_count)
                cantRestricciones = range(restricciones_count)
                cantRestriccionesDisminuido = range(restricciones_count-1)
                
                # Recopilar datos de la función objetivo
                datosDelfuncionObjetivo = []
                for i in cantVariables:
                    dato = request.POST.get(f'variablesFuncion_{i}')
                    if dato is None or dato == '':
                        raise ValueError(f"Falta coeficiente para X{i}")
                    datosDelfuncionObjetivo.append(dato)
                
                # Recopilar datos de restricciones
                datosRestricciones = []
                retriccionesIndividuales = []
                signos = []
                
                for j in cantRestricciones:
                    restriccion = []
                    for i in cantVariables:
                        dato = request.POST.get(f'variables_{j}_{i}')
                        if dato is None or dato == '':
                            raise ValueError(f"Falta coeficiente para X{i} en restricción {j+1}")
                        restriccion.append(dato)
                        datosRestricciones.append(dato)
                    
                    # Agregar término independiente
                    datoR = request.POST.get(f'variablesR_{j}')
                    if datoR is None or datoR == '':
                        raise ValueError(f"Falta término independiente en restricción {j+1}")
                    restriccion.append(datoR)
                    datosRestricciones.append(datoR)
                    
                    # Obtener signo
                    signo = request.POST.get(f'signo{j}')
                    if signo is None:
                        raise ValueError(f"Falta signo para restricción {j+1}")
                    signos.append(signo)
                    
                    retriccionesIndividuales.append(restriccion)
                
                # Procesar resultados
                displayTablas = "block"
                resultados = simplex_dual_pulp(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
                
                simplex = Simplex(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
                simplex.preparar_datos()
                tablasDeDual = simplex.resolver()
                
                nuevaFuncionZ = list(zip(datosDelfuncionObjetivo, cantVariables))
                
                return render(request, 'metododual.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'fucionObjetivo': datosDelfuncionObjetivo,
                    'datosDelModelo': datosRestricciones,
                    'datosDerestricciones': datosRestricciones,
                    'retriccionesIndividuales': retriccionesIndividuales,
                    'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                    'ocularTablas': displayTablas,
                    "tablas": tablasDeDual,
                    'nuevaFuncionZ': nuevaFuncionZ,
                    'resultado': resultados,
                    'tipo': tipo
                })
                
            except (ValueError, KeyError) as e:
                return render(request, 'metododual.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })
        
              

def metodosimplex(request):
    displayTablas = "none"
    if request.method == 'GET':
        display = "none"
        displayTablas = "none"
        
        return render(request, 'metodosimplex.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        display = "block"
        
        if Action == "generarModelo":   
            try:
                cant_restricciones = int(request.POST["restricciones"])
                cant_variables = int(request.POST["variables"])
                tipo = request.POST.get("tipo", "maximizar")
                
                cantRestricciones = range(cant_restricciones)
                cantRestriccionesDisminuido = range(cant_restricciones-1)
                cantVa = range(cant_variables-1)
                cantVariables = range(cant_variables)
                
                return render(request, 'metodosimplex.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'ocularTablas': displayTablas,
                    'tipo': tipo
                })
            except (ValueError, KeyError) as e:
                return render(request, 'metodosimplex.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })
                
        if Action == "Desarrollar":
            try:
                # Obtener datos del POST
                variables_count = int(request.POST.get('variables_count', 0))
                restricciones_count = int(request.POST.get('restricciones_count', 0))
                tipo = request.POST.get('tipo', 'maximizar')
                
                cantVariables = range(variables_count)
                cantRestricciones = range(restricciones_count)
                cantRestriccionesDisminuido = range(restricciones_count-1)
                canVari = variables_count
                
                # Recopilar datos de la función objetivo
                datosDelfuncionObjetivo = []
                for i in cantVariables:
                    dato = request.POST.get(f'variablesFuncion_{i}')
                    if dato is None or dato == '':
                        raise ValueError(f"Falta coeficiente para X{i}")
                    datosDelfuncionObjetivo.append(dato)
                
                # Recopilar datos de restricciones
                datosRestricciones = []
                retriccionesIndividuales = []
                
                for j in cantRestricciones:
                    restriccion = []
                    for i in cantVariables:
                        dato = request.POST.get(f'variables_{j}_{i}')
                        if dato is None or dato == '':
                            raise ValueError(f"Falta coeficiente para X{i} en restricción {j+1}")
                        restriccion.append(dato)
                        datosRestricciones.append(dato)
                    
                    # Agregar término independiente
                    datoR = request.POST.get(f'variablesR_{j}')
                    if datoR is None or datoR == '':
                        raise ValueError(f"Falta término independiente en restricción {j+1}")
                    restriccion.append(datoR)
                    datosRestricciones.append(datoR)
                    
                    retriccionesIndividuales.append(restriccion)
                
                # Procesar resultados
                displayTablas = "block"
                metodo = MetodoSimplex()
                tablas = metodo.resolver_simplex(retriccionesIndividuales, datosDelfuncionObjetivo)
                resultados = resolver_problema_optimizacion(canVari, datosDelfuncionObjetivo, retriccionesIndividuales)
                
                nuevaFuncionZ = list(zip(datosDelfuncionObjetivo, cantVariables))
                
                # Calcular Z óptimo
                a_numeros = [float(valor) for valor in datosDelfuncionObjetivo]
                Zoptimo = 0
                for i, valor in enumerate(a_numeros):
                    clave = f'X{i+1}'
                    Zoptimo += valor * resultados.get(clave, 0)
                
                return render(request, 'metodosimplex.html', {
                    'cantVariables': cantVariables,
                    'cantRestricciones': cantRestricciones, 
                    'ocultar': display,
                    'fucionObjetivo': datosDelfuncionObjetivo,
                    'datosDelModelo': datosRestricciones,
                    'datosDerestricciones': datosRestricciones,
                    'retriccionesIndividuales': retriccionesIndividuales,
                    'tablas': tablas,
                    'resultados': resultados,
                    'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                    'ocularTablas': displayTablas,
                    'nuevaFuncionZ': nuevaFuncionZ,
                    'Zoptimo': Zoptimo,
                    'tipo': tipo
                })
                
            except (ValueError, KeyError) as e:
                return render(request, 'metodosimplex.html', {
                    'ocultar': "none",
                    'ocularTablas': "none",
                    'error': f"Error en los datos: {str(e)}"
                })
        
        
    
