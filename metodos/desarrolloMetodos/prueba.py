# Definir variables con N elementos
a = ['10', '20', '30']
b = {'X1': 15.0, 'X2': 35.0, 'X3': 25.0}

# Convertir los elementos de 'a' a números
a_numeros = [int(valor) for valor in a]

# Inicializar el resultado
resultado = 0

# Iterar a través de los elementos y realizar las multiplicaciones y sumas
for i, valor in enumerate(a_numeros):
    clave = f'X{i+1}'
    resultado += valor * b.get(clave, 0)

print(resultado)






















