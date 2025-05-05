from django.shortcuts import render, redirect
from django.http import HttpResponse
from metodos.desarrolloMetodos.metodoSimplex import *
from metodos.desarrolloMetodos.metodoDual import *
from metodos.desarrolloMetodos.MetodoGranM import *
import os
from django.http import FileResponse, Http404
from django.conf import settings

# Create your views here.

cantRestricciones = []
cantVariables = []
cantVa = []
cantRestriccionesDisminuido = []
canVari = []
tipo = []

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
    global cantRestricciones, cantVariables, cantVa, cantRestriccionesDisminuido, canVari, tipo
    displayTablas= "none"
    if request.method == 'GET':
        display = "none"
        displayTablas= "none"
        
        return render(request, 'metodogranm.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        datosDelModelo = []
        datosDelfuncionObjetivo = []
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        datosDelfuncionObjetivo=[]
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        retriccionesIndividuales=[]
        signos=[]
        coeficiente=[]
        print(Action)
        display = "block"
        
        if Action == "generarModelo":   
            cantRestricciones = range(int(request.POST["restricciones"]))
            cantRestriccionesDisminuido = range(int(request.POST["restricciones"])-1)
            cantVa = range(int(request.POST["variables"])-1)
            cantVariables = range(int(request.POST["variables"]))
            tipo = request.POST["tipo"]
            print(tipo)
            
            return render(request, 'metodogranm.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'ocularTablas': displayTablas
            })
        if Action == "Desarrollar":
            displayTablas = "block"
            print(cantRestricciones)
            print(cantVariables)
            canVari = max(cantVariables)+1
            for i in cantVariables:
                dato= request.POST.get(f'variablesFuncion_{i}')
                print(dato)
                datosDelModelo.append(dato)
                datosDelfuncionObjetivo.append(dato)
            for j in cantRestricciones:
                for i in cantVariables:
                    dato = request.POST.get(f'variables_{j}_{i}')
                    datosDelModelo.append(dato)
                    datosRestricciones.append(dato)       
                dato = request.POST.get(f'variablesR_{j}')
                print(dato)
                datosDelModelo.append(dato)
                datosRestriccionesFinales.append(dato)
                datosRestricciones.append(dato)
            for i in cantRestricciones:
                datoSigno= request.POST.get(f'signo{i}')
                signos.append(datoSigno)
            
        
            n= len(datosDelfuncionObjetivo)+1
            print(datosRestricciones)
            for i in range(0, len(datosRestricciones), max(cantVariables)+2):
                print(datosRestricciones[i:i+n])
                retriccionesIndividuales.append(datosRestricciones[i:i+n])
                
            print(retriccionesIndividuales)   
            print(signos) 
            print(datosDelfuncionObjetivo)
            print(tipo)
       
            resultados = simplex_gran_m(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
            
            
            nuevaFuncionZ=list(zip(datosDelfuncionObjetivo,cantVariables))
            print("Datos combinados:", nuevaFuncionZ)
                       
            return render(request, 'metodogranm.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'fucionObjetivo':datosDelfuncionObjetivo ,
                'datosDelModelo': datosDelModelo,
                'datosDerestricciones': datosRestricciones,
                'retriccionesIndividuales':retriccionesIndividuales,
                'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                'ocularTablas': displayTablas,
                'nuevaFuncionZ': nuevaFuncionZ,
                'resultado': resultados
            })

def metododosfases(request):
    global cantRestricciones, cantVariables, cantVa, cantRestriccionesDisminuido, canVari, tipo
    displayTablas= "none"
    if request.method == 'GET':
        display = "none"
        displayTablas= "none"
        
        return render(request, 'metododosfases.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        datosDelModelo = []
        datosDelfuncionObjetivo = []
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        datosDelfuncionObjetivo=[]
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        retriccionesIndividuales=[]
        signos=[]
        coeficiente=[]
        print(Action)
        display = "block"
        
        if Action == "generarModelo":   
            cantRestricciones = range(int(request.POST["restricciones"]))
            cantRestriccionesDisminuido = range(int(request.POST["restricciones"])-1)
            cantVa = range(int(request.POST["variables"])-1)
            cantVariables = range(int(request.POST["variables"]))
            tipo = request.POST["tipo"]
            print(tipo)
            
            return render(request, 'metododosfases.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'ocularTablas': displayTablas
            })
        if Action == "Desarrollar":
            displayTablas = "block"
            print(cantRestricciones)
            print(cantVariables)
            canVari = max(cantVariables)+1
            for i in cantVariables:
                dato= request.POST.get(f'variablesFuncion_{i}')
                print(dato)
                datosDelModelo.append(dato)
                datosDelfuncionObjetivo.append(dato)
            for j in cantRestricciones:
                for i in cantVariables:
                    dato = request.POST.get(f'variables_{j}_{i}')
                    datosDelModelo.append(dato)
                    datosRestricciones.append(dato)       
                dato = request.POST.get(f'variablesR_{j}')
                print(dato)
                datosDelModelo.append(dato)
                datosRestriccionesFinales.append(dato)
                datosRestricciones.append(dato)
            for i in cantRestricciones:
                datoSigno= request.POST.get(f'signo{i}')
                signos.append(datoSigno)
            
        
            n= len(datosDelfuncionObjetivo)+1
            print(datosRestricciones)
            for i in range(0, len(datosRestricciones), max(cantVariables)+2):
                print(datosRestricciones[i:i+n])
                retriccionesIndividuales.append(datosRestricciones[i:i+n])
                
            print(retriccionesIndividuales)   
            print(signos) 
            print(datosDelfuncionObjetivo)
            print(tipo)
       
            status, valor_optimo, resultados = two_phase_simplex(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
            
            
            nuevaFuncionZ=list(zip(datosDelfuncionObjetivo,cantVariables))
            print("Datos combinados:", nuevaFuncionZ)
                       
            return render(request, 'metododosfases.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'fucionObjetivo':datosDelfuncionObjetivo ,
                'datosDelModelo': datosDelModelo,
                'datosDerestricciones': datosRestricciones,
                'retriccionesIndividuales':retriccionesIndividuales,
                'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                'ocularTablas': displayTablas,
                'nuevaFuncionZ': nuevaFuncionZ,
                'resultado': resultados,
                'Zoptimo': valor_optimo
            })


def metodografico(request):
    return render(request, 'metodografico.html')

def metododual(request):
    global cantRestricciones, cantVariables, cantVa, cantRestriccionesDisminuido, canVari
    displayTablas= "none"
    if request.method == 'GET':
        display = "none"
        displayTablas= "none"
        
        return render(request, 'metododual.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        datosDelModelo = []
        datosDelfuncionObjetivo = []
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        datosDelfuncionObjetivo=[]
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        retriccionesIndividuales=[]
        signos=[]
        coeficiente=[]
        print(Action)
        display = "block"
        
        if Action == "generarModelo":   
            cantRestricciones = range(int(request.POST["restricciones"]))
            cantRestriccionesDisminuido = range(int(request.POST["restricciones"])-1)
            cantVa = range(int(request.POST["variables"])-1)
            cantVariables = range(int(request.POST["variables"]))
            
            print(cantRestricciones)
            print(cantVariables)
           
            return render(request, 'metododual.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'ocularTablas': displayTablas
            })
            
        if Action == "Desarrollar":
            displayTablas = "block"
            print(cantRestricciones)
            print(cantVariables)
            canVari = max(cantVariables)+1
            for i in cantVariables:
                dato= request.POST.get(f'variablesFuncion_{i}')
                print(dato)
                datosDelModelo.append(dato)
                datosDelfuncionObjetivo.append(dato)
            for j in cantRestricciones:
                for i in cantVariables:
                    dato = request.POST.get(f'variables_{j}_{i}')
                    datosDelModelo.append(dato)
                    datosRestricciones.append(dato)       
                dato = request.POST.get(f'variablesR_{j}')
                print(dato)
                datosDelModelo.append(dato)
                datosRestriccionesFinales.append(dato)
                datosRestricciones.append(dato)
            for i in cantRestricciones:
                datoSigno= request.POST.get(f'signo{i}')
                signos.append(datoSigno)
            
        
            print(max(cantVariables)+2)
            print(len(datosRestricciones))
            n= len(datosDelfuncionObjetivo)+1
            print(datosRestricciones)
            for i in range(0, len(datosRestricciones), max(cantVariables)+2):
                print(datosRestricciones[i:i+n])
                retriccionesIndividuales.append(datosRestricciones[i:i+n])
                
            print(retriccionesIndividuales)   
            print(signos) 
            print(datosDelfuncionObjetivo)
       
            tipo = "minimizar"
            resultados = simplex_dual_pulp(retriccionesIndividuales, signos, datosDelfuncionObjetivo, tipo)
            print(resultados)
            
            simplex = Simplex(retriccionesIndividuales, signos, datosDelfuncionObjetivo, "minimizar")
            simplex.preparar_datos()
            tablasDeDual = simplex.resolver()
            print(tablasDeDual)
            
            nuevaFuncionZ=list(zip(datosDelfuncionObjetivo,cantVariables))
            print("Datos combinados:", nuevaFuncionZ)
            
        
            
            
            return render(request, 'metododual.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'fucionObjetivo':datosDelfuncionObjetivo ,
                'datosDelModelo': datosDelModelo,
                'datosDerestricciones': datosRestricciones,
                'retriccionesIndividuales':retriccionesIndividuales,
                'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                'ocularTablas': displayTablas,
                "tablas": tablasDeDual,
                'nuevaFuncionZ': nuevaFuncionZ,
                'resultado': resultados
            })
        
              

def metodosimplex(request):
    global cantRestricciones, cantVariables, cantVa, cantRestriccionesDisminuido, canVari
    displayTablas= "none"
    if request.method == 'GET':
        display = "none"
        displayTablas= "none"
        
        return render(request, 'metodosimplex.html', {
            'ocultar': display,
            'ocularTablas': displayTablas
        })
    else:
        Action = request.POST.get('action')
        datosDelModelo = []
        datosDelfuncionObjetivo = []
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        datosDelfuncionObjetivo=[]
        datosRestricciones=[]
        datosRestriccionesFinales=[]
        retriccionesIndividuales=[]
        print(Action)
        display = "block"
        
        if Action == "generarModelo":   
            cantRestricciones = range(int(request.POST["restricciones"]))
            cantRestriccionesDisminuido = range(int(request.POST["restricciones"])-1)
            cantVa = range(int(request.POST["variables"])-1)
            cantVariables = range(int(request.POST["variables"]))
            
            print(cantRestricciones)
            print(cantVariables)
           
            return render(request, 'metodosimplex.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'ocularTablas': displayTablas
            })
            
        if Action == "Desarrollar":
            displayTablas = "block"
            print(cantRestricciones)
            print(cantVariables)
            canVari = max(cantVariables)+1
            for i in cantVariables:
                dato= request.POST.get(f'variablesFuncion_{i}')
                print(dato)
                datosDelModelo.append(dato)
                datosDelfuncionObjetivo.append(dato)
        
            
            for j in cantRestricciones:
                for i in cantVariables:
                    dato = request.POST.get(f'variables_{j}_{i}')
                    datosDelModelo.append(dato)
                    datosRestricciones.append(dato)
                       
                dato = request.POST.get(f'variablesR_{j}')
                print(dato)
                datosDelModelo.append(dato)
                datosRestriccionesFinales.append(dato)
                datosRestricciones.append(dato)
            
            print(max(cantVariables)+2)
            print(len(datosRestricciones))
            n= len(datosDelfuncionObjetivo)+1
            print(datosRestricciones)
            for i in range(0, len(datosRestricciones), max(cantVariables)+2):
                print(datosRestricciones[i:i+n])
                retriccionesIndividuales.append(datosRestricciones[i:i+n])
                
            print(retriccionesIndividuales)    
            print(datosDelfuncionObjetivo)
            print(canVari)
            metodo = MetodoSimplex()
            tablas = metodo.resolver_simplex(retriccionesIndividuales, datosDelfuncionObjetivo)
            resultados = resolver_problema_optimizacion(canVari,datosDelfuncionObjetivo,retriccionesIndividuales)
            print(tablas)
            print(type(resultados))
            print(resultados)
            print(cantRestriccionesDisminuido)
            nuevaFuncionZ=list(zip(datosDelfuncionObjetivo,cantVariables))
            # Convertir los elementos de 'a' a números
            a_numeros = [int(valor) for valor in datosDelfuncionObjetivo]

            # Inicializar el resultado
            Zoptimo = 0

            # Iterar a través de los elementos y realizar las multiplicaciones y sumas
            for i, valor in enumerate(a_numeros):
                clave = f'X{i+1}'
                Zoptimo += valor * resultados.get(clave, 0)

            print(Zoptimo)    

            
            print("Datos combinados:", nuevaFuncionZ)
            return render(request, 'metodosimplex.html', {
                'cantVariables': cantVariables,
                'cantRestricciones': cantRestricciones, 
                'ocultar': display,
                'fucionObjetivo':datosDelfuncionObjetivo ,
                'datosDelModelo': datosDelModelo,
                'datosDerestricciones': datosRestricciones,
                'retriccionesIndividuales':retriccionesIndividuales,
                'tablas': tablas,
                'resultados': resultados,
                'cantRestriccionesDisminuidas': cantRestriccionesDisminuido,
                'ocularTablas': displayTablas,
                'nuevaFuncionZ': nuevaFuncionZ,
                'Zoptimo': Zoptimo
            })
        
        
    
