from math import log2 

mensaje = ".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."
def obtenerAlfabetoMatrizTransicion(mensaje: String):
    listaMensaje = list(mensaje)
    alfabeto = list(dict.fromkeys(mensaje)) #diccionario conserva orden al desarmar mensaje
    n = len(alfabeto)

    matriz = [[0] * n for _ in range(n)] # Inicializo matriz en cero
    totalCol = [0] * n # veces que una letra aparece en la columna

    # Recorre lista mensaje, toma el caracter anterior y el actual y suma 1 al valor total
    # "ABC" con lista "[A,B,C]" -> Si ant=A y act=B en matriz[1][0] se suma 1
    for i in range(1,len(listaMensaje)): 
        ant = listaMensaje[i - 1]
        act = listaMensaje[i]
        posAnt= alfabeto.index(ant)
        posAct= alfabeto.index(act)
        matriz[posAnt][posAct] += 1 # importante el orden de ant y act en fila y col 
        totalCol[posAct] +=1
    # Divide cada columna por el total de veces que aparece (menos la primera letra)
    #print(matriz)
    for i in range(n):
        for j in range(n):
            matriz[i][j] /= totalCol[i]
    return alfabeto, matriz

def obtenerEstacionario(matriz: list[list]):
    n = len(matriz)
    tolerancia = 0.05
    vectorEstacionario : list = [1/n] * n  # Asumo equiprobable
    nuevoVectorEstacinario : list = [0] * n
    sigue = True
    while sigue:
        sigue = False
        nuevoVectorEstacinario = multMatrizVec(matriz, vectorEstacionario)
        for i in range(n):
            if(vectorEstacionario[i] - nuevoVectorEstacinario[i] > tolerancia): 
                sigue = True
                break
        vectorEstacionario = nuevoVectorEstacinario
        
    return  vectorEstacionario

def multMatrizVec(matriz, vector):
    n = len(matriz)
    nuevoValor : list = [0] * n
    for j in range(n):
        for i in range(n):
            nuevoValor[j] += vector[i] * matriz[i][j]
    return nuevoValor

def obtenerEntropia(matriz: list[list], estacionario: list):
    n = len(estacionario)
    total = 0
    for i in range(n):
        for j in range(n):
            if (matriz[i][j] != 0):
                total += estacionario[i] * matriz[i][j] * log2(1/matriz[i][j])
    return total

alfabeto, matriz = obtenerAlfabetoMatrizTransicion(mensaje) 
estacionario = obtenerEstacionario(matriz)
print(estacionario)
entropia = obtenerEntropia(matriz, estacionario)
print("Entropia: " + str(entropia))