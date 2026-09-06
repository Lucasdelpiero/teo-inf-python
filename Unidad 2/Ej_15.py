import random

mensaje = ".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."
#mensaje = "+-/+/-//-/*-/**-*---////-+--*+*/-----/--+/++--*/-+"
#mensaje = "]]]([[]))([(])]([]([([([)([([([[([))][([([[([)([(]"
#mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"

# a
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
    for i in range(n):
        for j in range(n):
            matriz[i][j] /= totalCol[i]
  
    return alfabeto, matriz

# b
def simularMensaje(alfabeto: list, matriz: list[list], largo: int):
    rand = random.random()
    n = len(matriz)
    acum = [[0] * n for _ in range(n)] # Matriz prob acumuladas
    for i in range(n):
        total = 0
        for j in range(n):
            total += matriz[i][j]
            acum[i][j] = total

    listaPalabra : list = [alfabeto[random.randint(0,3)]] # Primera letra de palabra
    for i in range(1, largo):   
        letraAnt = listaPalabra[i - 1] # Segun la letra anterior usa su columna para elegir la sig letra
        letraAntPos = alfabeto.index(letraAnt)  # Para ver que columna de la matriz acumulada recorre
        rand = random.random()
        j = 0
        while rand > acum[letraAntPos][j] and j < n:
            j += 1
        listaPalabra.append(alfabeto[j])
    palabra = "".join(listaPalabra)

    return palabra

#c
# Si no tiene memoria, todos los valores de una columna deben ser similares (dentro de la tolerancia)
# Si tiene memoria, 
def tieneMemoria(matriz: list[list], tolerancia: float):
    n = len(matriz)
    tiene = False
    for j in range(1,n):
        valor = matriz[0][j] # Compara primer valor de col con el resto
        for i in range(n):
            actual = abs(valor - matriz[i][j])
            if (actual) > tolerancia:
                return True

    return tiene

alfabeto, matriz = obtenerAlfabetoMatrizTransicion(mensaje) #a
print("alfabeto: " + str(alfabeto))
print("Matriz transicion:")
print(matriz)
nuevoMensaje = simularMensaje(alfabeto, matriz, 45) #b
print("Mensaje simulado: " + nuevoMensaje)
if tieneMemoria(matriz, 0.05): # c
    print("Tiene memoria")
else:
    print("No tiene memoria")
