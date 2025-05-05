import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import re
from tkinter import Entry, Label, Button, Radiobutton, StringVar
from tkinter import *
from os import remove
from PIL import Image, ImageTk

vertices_labels = []  # Lista para almacenar los labels de los vértices
root = Tk()
root.title("Programación Lineal")
root.geometry("1100x600")

canvas = Canvas(root, width=550, height=500)
canvas.pack(side=LEFT)


def generar_restricciones():
    global restriccion_entries, restriccion_labels, calcular_btn
    global num_restricciones_entry

    num_restricciones = int(num_restricciones_entry.get())
    # print(num_restricciones)

    for widget in canvas.winfo_children():
        widget.destroy()

    restriccion_entries = []
    restriccion_labels = []
    if num_restricciones > 5:
        num_restricciones = 5

    for i in range(num_restricciones):
        restriccion_label = Label(root, text=f"Restriccion {i +1}: ")
        restriccion_label.pack()
        restriccion_entry = Entry(root)
        restriccion_entry.pack()
        restriccion_labels.append(restriccion_label)
        restriccion_entries.append(restriccion_entry)

    generar_restricciones_btn.config(state="disabled")
    num_restricciones_entry.config(state="disabled")
    # boton de la función calcular_valor_optimo
    calcular_btn = Button(root, text="Calcular", command=calcular_solucion_optima)
    calcular_btn.pack(side=tk.TOP, pady=20)


def calcular_valor_optimo(vertices):
    global vertices_labels  # Usa la lista global para almacenar los labels

    # Borra los labels anteriores
    for label in vertices_labels:
        label.destroy()
    vertices_labels.clear()  # Limpia la lista para los nuevos labels

    optimize = maximizar_minimizar_var.get()
    valor_optimo = None
    solucion_optima = None

    funcion_objetivo_str = funcion_objetivo_entry.get()
    patron = r"(\d+)([a-zA-Z])"
    funcion_objetivo = re.sub(patron, r"\1*\2", funcion_objetivo_str)

    evaluacion_vertices_title = tk.StringVar()
    evaluacion_vertices_title_label = Label(
        root, textvariable=evaluacion_vertices_title
    )
    evaluacion_vertices_title_label.pack()
    evaluacion_vertices_title.set(f"Vertices : Evaluación")

    # Asegúrate de agregar este label a la lista para poder eliminarlo luego
    vertices_labels.append(evaluacion_vertices_title_label)

    for punto in vertices:
        x, y = punto
        resultado = eval(funcion_objetivo)
        evaluacion_vertices = tk.StringVar()
        evaluacion_vertices_label = Label(root, textvariable=evaluacion_vertices)
        evaluacion_vertices_label.pack()
        evaluacion_vertices.set(f"({x}, {y}) : {resultado}")

        # Añade cada nuevo label a la lista
        vertices_labels.append(evaluacion_vertices_label)

        if (
            valor_optimo is None
            or (optimize == "max" and resultado > valor_optimo)
            or (optimize == "min" and resultado < valor_optimo)
        ):
            valor_optimo = resultado
            solucion_optima = (x, y)

    if solucion_optima is not None:
        x_optimo, y_optimo = solucion_optima
        x_optimo_redondeado = round(
            x_optimo, 2
        )  # Cambia el número de decimales según tus necesidades
        y_optimo_redondeado = round(
            y_optimo, 2
        )  # Cambia el número de decimales según tus necesidades
        valor_optimo_redondeado = round(
            valor_optimo, 2
        )  # Cambia el número de decimales según tus necesidades
        resultado_text.set(
            f"Solución óptima en ({x_optimo_redondeado}, {y_optimo_redondeado}) con valor {valor_optimo_redondeado}"
        )
    else:
        resultado_text.set("No se encontró una solución óptima")


def encontrar_puntos_interseccion(restricciones):
    puntos_interseccion = []
    origen=ajustar_punto_origen(ecuaciones)
    print(origen)
    puntos_interseccion.append(origen)
    # Encuentra puntos de intersección entre pares de líneas
    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            A1, B1, C1 = restricciones[i]
            A2, B2, C2 = restricciones[j]
            determinant = A1 * B2 - A2 * B1
            if determinant != 0:  # Asegura que no son líneas paralelas
                x_intersection = (C1 * B2 - C2 * B1) / determinant
                y_intersection = (A1 * C2 - A2 * C1) / determinant
                if 0 <= x_intersection <= 1000 and 0 <= y_intersection <= 1000:
                    puntos_interseccion.append((x_intersection, y_intersection))

    # Incluye los puntos de intersección con los ejes, evitando divisiones por cero o lógica incorrecta
    for A, B, C in restricciones:
        if A != 0:  # Punto donde la línea intersecta el eje x (y=0)
            x_intersection = C / A
            if origen[0] <= x_intersection <= 1000:
                puntos_interseccion.append((x_intersection, 0))
        if B != 0:  # Punto donde la línea intersecta el eje y (x=0)
            y_intersection = C / B
            if origen[1] <= y_intersection <= 1000:
                puntos_interseccion.append((0, y_intersection))

    # Eliminar duplicados
    puntos_interseccion = list(set(puntos_interseccion))

    return puntos_interseccion

def ajustar_punto_origen(ecuaciones):
    # Inicializar el punto de origen a (0, 0)
    x_origen = 0
    y_origen = 0

    for A, B, C in ecuaciones:
        if B == 0 and A < 0:  # x >= C
            x_origen = max(x_origen, C)
        elif A == 0 and B < 0:  # y >= C
            y_origen = max(y_origen, C)

    return (x_origen, y_origen)


# Función para generar los vértices de la región acotada
def generar_vertices(puntos_interseccion):
    vertices = set()
    for punto in puntos_interseccion:
        es_vertice = True
        for restriccion in ecuaciones:
            A, B, C = restriccion
            
            resultado = A * punto[0] + B * punto[1] - C
            if resultado > 0:
                es_vertice = False
                break
        if es_vertice:
            vertices.add(punto)
        
    return list(vertices)

# Función para graficar la región acotada
def graficar_region_acotada(vertices):

    # organizar
    vertices_organizados = sorted(vertices, key=lambda x: (x[0], x[1]))
    x_vertices, y_vertices = zip(*vertices_organizados)
    plt.fill(x_vertices, y_vertices, alpha=0.2, color="blue", label="Región factible")
    # print(vertices)
    # print(vertices_organizados)


# Función para graficar las restricciones
def graficar_restricciones():

    for i in range(len(ecuaciones)):
        ec_label = restriccion_entries[i].get()
        A, B, C = ecuaciones[i]
        if B == 0:
            m = C / A
            plt.axvline(m, linestyle="-")

        elif A == 0:
            m = C / B
            plt.axhline(m, linestyle="-")

        else:
            x = np.linspace(0, 1000)
            y = (C - (A * x)) / B
            plt.plot(x, y, label=ec_label)


# Función principal para calcular la solución óptima
def calcular_solucion_optima():
    global ecuaciones
    ecuaciones = []

    # remove('grafico.png')
    num_restricciones = int(num_restricciones_entry.get())

    for i in range(num_restricciones):
        ec_str = restriccion_entries[i].get()
        parts = ec_str.split()
        A, B, C, op = None, None, None, None
        for part in parts:
            part = part.strip()
            if "x" in part:
                if "x" == part:
                    A = 1
                elif "-x" == part:
                    A = -1
                else:
                    A = float(part.replace("x", ""))
            elif "y" in part:
                if "y" == part:
                    B = 1
                elif "-y" == part:
                    B = -1
                else:
                    B = float(part.replace("y", ""))
            elif ">=" in part:
                op = ">="
            elif "<=" in part:
                op = "<="
            elif op is not None:
                C = float(part)

            # Si no se especifica x o y, se considera el coeficiente como cero
            if A is None:
                A = 0
            if B is None:
                B = 0

        if A is not None and B is not None and C is not None and op is not None:
            if op == ">=":
                C = -C
                A = -A
                B = -B
            ecuaciones.append([A, B, C])
        else:
            resultado_text.set(
                f"Error en la entrada de la restricción {i + 1}. Asegúrese de usar el formato 'AX + By <= C'."
            )
            return

    puntos_interseccion = encontrar_puntos_interseccion(ecuaciones)

    print(puntos_interseccion)
    print(generar_vertices(puntos_interseccion))      


    vertices = generar_vertices(puntos_interseccion)
    max_x = max(vertices, key=lambda punto: punto[0])
    max_y = max(vertices, key=lambda punto: punto[1])
    x_axis = max(max_x) + (max(max_x)) * 0.05
    y_axis = max(max_y) + (max(max_y)) * 0.05
    plt.clf()
    graficar_region_acotada(vertices)
    graficar_restricciones()

    plt.xlim(0, x_axis)
    plt.ylim(0, y_axis)
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.grid(True, linewidth=0.5, linestyle="--")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Programación lineal - Método gráfico")

    calcular_valor_optimo(vertices)

    plt.legend()
    plt.savefig("grafico.png")
    image = Image.open("grafico.png")
    photo = ImageTk.PhotoImage(image)

    # Utiliza el objeto PhotoImage de Tkinter para mostrar la imagen en el lienzo
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    canvas.config(width=image.width, height=image.height)
    canvas.image = photo  # Mantén una referencia al objeto PhotoImage para evitar que sea eliminado por el recolector de basura


# Función para finalizar el programa
def finalizar_programa():
    root.destroy()


funcion_objetivo_label = Label(root, text="Función objetivo: ")
funcion_objetivo_label.pack()
funcion_objetivo_entry = Entry(root)
funcion_objetivo_entry.pack()
funcion_objetivo_entry.config(width=12, justify="center", font=16)

maximizar_minimizar_var = StringVar()
maximizar_minimizar_var.set("max")  # Determinado
maximizar_minimizar_lbl = Label(root, text="¿Que desea hacer con la función objetivo?")
maximizar_minimizar_lbl.pack()
maximizar_minimizar_radio_max = Radiobutton(
    root, text="Maximizar", variable=maximizar_minimizar_var, value="max"
)
maximizar_minimizar_radio_min = Radiobutton(
    root, text="Minimizar", variable=maximizar_minimizar_var, value="min"
)
maximizar_minimizar_radio_max.pack()
maximizar_minimizar_radio_min.pack()

# Etiquetas y campos de entrada de parámetros
num_restricciones_label = Label(
    root, text="Indica el numero de restricciones (max 5): "
)
num_restricciones_label.pack()
num_restricciones_entry = Entry(root)
num_restricciones_entry.pack()
num_restricciones_entry.config(width=12, justify="center", font=16)

# Generar campos de restricciones
generar_restricciones_btn = Button(
    root, text="Generar campos de restricciones", command=generar_restricciones
)
generar_restricciones_btn.pack(side=TOP, pady=10)
finalizar_btn = Button(root, text="Finalizar", command=finalizar_programa)
finalizar_btn.pack(side=tk.TOP, pady=10)

# valor optimo y evaluacion de los vertices
resultado_text = tk.StringVar()
resultado_label = Label(root, textvariable=resultado_text)
resultado_label.pack()


root.mainloop()
