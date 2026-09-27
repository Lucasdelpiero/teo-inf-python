from math import log2
import math
import random

TOLERANCIA = 0.001  

################################################### UNIDAD 2 ######################################################################

############# Funciones para mensajes y listas de alfabeto y probabilidad, obtener entropia  ######################################

#Devuelve una lista con la cantidad de bits necesarios para representar cada simbolo
def get_lista_bits_necesarios(listaProb: list[float]):
    nuevaLista = []
    for prob in listaProb:
        nuevaLista.append(log2(1/prob )) 
    return nuevaLista

# Entropia de una lista de probabilidades
def get_entropia_lista_prob(listaProb: list[float]):
    total = 0

    for prob in listaProb:
        total += prob * log2(1/prob)
    return total

# Entropia de un numero si su prob es equiprobable
def get_entropia_equiprob(num: int): # ej: dado de 6, es como si hubiera 6 elementos de 1/6 de prob
    return log2(num)


# Crea listas de alfabeto y probabilidades con caracteres de mensajes
def get_listas_alf_prob(mensaje: str):  # ej: "casa"
    listaAlf = [] 
    listaProb = []

    for letra in mensaje:
        if letra not in listaAlf:
            listaAlf.append(letra)

    for letra in listaAlf:
        listaProb.append(mensaje.count(letra)/len(mensaje))

    return [listaAlf, listaProb] # listas = crearListasAlfProb(mensaje)  ;  listaAlf = listas[0] ;    listaProb = listas[1]

# Obtiene lista alfabeto de una LISTA
def get_lista_alf_lista(lista: list[str]): # [ "001", "01", "012"]
    listaAlf = []
    for mensaje in lista:
        for letra in mensaje:
            if letra not in listaAlf:
                listaAlf.append(letra)
    return listaAlf # ["0", "1", "2"]

# Funcion auxiliar de genPalabra
# Segun el numero ingresado devuelve la pos del elemento segun su probabilidad acumulada
def get_num(n: int, acum):
    for i in range(len(acum)):
        if n < acum[i]:
            return i

# Genera palabra ALEATORIA de largo N  
def gen_palabra(n: int, listaAlf: list[str], listaProb: list[float]):
    palabra = ""
    listaAcum = []
    # Genera lista con probabilidad acumulada de alfabeto
    for i in range(len(listaAlf)):
        if i == 0: 
            listaAcum.append(listaProb[i])
        else:
            listaAcum.append(listaProb[i] + listaAcum[i - 1])
    print(listaAcum)

    # genera la palabra segun un numero aleatorio y lista acumulada
    for i in range(n):
        palabra += listaAlf[get_num(random.random(), listaAcum)]

    return palabra

# Si no tiene memoria, todos los valores de una fila deben ser similares (dentro de la tolerancia)
# Si tiene memoria, 
def tiene_memoria(matriz: list[list], tolerancia: float):
    n = len(matriz)

    for i in range(n):
        menor = mayor = matriz[i][0]
        for j in range(n):
            valor = matriz[i][j]
            if (valor < menor):
                menor = valor
            if (valor > mayor):
                mayor = valor
        if (mayor - menor > tolerancia):
            return True    
    return False


################################################### VECTORES Y MATRICES ###########################################################

#### Con un mensaje obtener matriz de transicion, obtener matriz transicion, vector estacionario y usando ambos, la entropia  #####

# Sigue unidad 2

# Matriz transicion obtenida de un mensaje
def get_alfabeto_matriz_transicion(mensaje: str):
    listaMensaje = list(mensaje)
    alfabeto = list(dict.fromkeys(mensaje)) #diccionario conserva orden al desarmar mensaje
    n = len(alfabeto)

    matrizProb = [[0] * n for _ in range(n)] # Inicializo matriz en cero
    totalCol = [0] * n # veces que una letra aparece en la columna

    # Recorre lista mensaje, toma el caracter anterior y el actual y suma 1 al valor total
    # "ABC" con lista "[A,B,C]" -> Si ant=A y act=B en matriz[1][0] se suma 1
    for i in range(1,len(listaMensaje)): 
        ant = listaMensaje[i - 1]
        act = listaMensaje[i]
        posAnt= alfabeto.index(ant)
        posAct= alfabeto.index(act)
        matrizProb[posAct][posAnt] += 1 # importante el orden de ant y act en fila y col 
        totalCol[posAnt] +=1

    # Divide cada columna por el total de veces que aparece (menos la primera letra)
    for j in range(n):
        for i in range(n):
            matrizProb[i][j] /= totalCol[j]
  
    return alfabeto, matrizProb


# Vector estacionario asumiendo inicialmente que son equiprobables
def get_vector_estacionario(matriz: list[list], tolerancia: float):
    n = len(matriz)
    vectorEstacionario : list = [1/n] * n  # Asumo equiprobable
    nuevoVectorEstacinario : list = [0] * n
    sigue = True
    while sigue:
        sigue = False
        nuevoVectorEstacinario = mult_matriz_vec(matriz, vectorEstacionario)
        for i in range(n):
            if(vectorEstacionario[i] - nuevoVectorEstacinario[i] > tolerancia): 
                sigue = True
                break
        vectorEstacionario = nuevoVectorEstacinario
        
    return  vectorEstacionario

# Auxiliar para multiplicar matrices para obtener el estacionario
def mult_matriz_vec(matriz: list[list], vector: list[float]):
    n = len(matriz)
    nuevoValor : list = [0] * n
    for i in range(n):
        for j in range(n):
            nuevoValor[i] += matriz[i][j] * vector[j]
    return nuevoValor

# Entropia obtenida usando matriz y estacionario
def get_entropia_matriz(matriz: list[list], estacionario: list[float]):
    n = len(estacionario)
    total = 0
    for i in range(n):
        for j in range(n):
            if (matriz[i][j] != 0):
                total += estacionario[i] * matriz[i][j] * log2(1/matriz[i][j])
    return total

####################################################### UNIDAD 3 ##################################################################

# Se usa para inecuacion de kraft, si:    SUMATORIA <= 1 es condificion suficiente para la existencia de 
# AL MENOS 1 codigo INSTANTANEO de tal longitud
# Por inecuacion MacMillan si es > 1 entonces no se puede definir un codigo UNIVOCO ni INSTANTANEO
def get_sumatoria_kraft(listaPalabras: list[str]):
    alfabeto = get_lista_alf_lista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo
    total = 0
    for palabra in listaPalabras:
        li = len(palabra)       # li = largo de la palabra especifica
        total += r **  (-li)
    return total

# Funcion auxiliar para obtener el R (cant de simbolos de alfabeto codigo)
def get_r(listaPalabras: list[str]):
    alfabeto = get_lista_alf_lista(listaPalabras)
    r = len(alfabeto)
    return r

# Largo PROMEDIO de codigo usando su prob y largo de palabras
def get_longitud_media_codigo(listaProb: list[float], listaPalabras: list[str]):
    total = 0
    n = len(listaPalabras)
    for i in range(n):
        prob = listaProb[i]
        largo = len(listaPalabras[i])
        total += prob * largo
    return total

# Obtiene la entropia considerando PROB y LARGO de cada palabra codigo
def get_entropia_ponderada_largo(listaProb: list[float], listaPalabras: list[str]):
    total = 0
    n = len(listaPalabras)
    alfabeto = get_lista_alf_lista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo

    for i in range(n):
        prob = listaProb[i]
        total += prob * math.log(1/prob, r)
    return total


# Booleano que devuelve si un codigo es compacto usando su lista de prob y el largo de cada palabra codigo
def es_compacto(listaProb: list[float], listaCod: list[str]):
    compacto = True
    n = len(listaCod)
    if not es_univoco(listaCod):
        return False

    for i in range(n):
        r = get_r(listaCod)
        informacion = math.ceil(get_informacion(r, listaProb[i]))
        largo = len(listaCod[i])

        if (largo > informacion):
            compacto = False
    
    return compacto

# Funcion auxiliar 
def get_informacion(r: int, prob: float):
    return math.log(1/prob, r)

def tiene_prefijo(listaCod: list[str]):
    for cod in listaCod:
        if listaCod.index(cod) != -1:
            return True
    return False

def es_prefijo(corta, larga):
    return len(corta) < len(larga) and larga[: len(corta)] == corta

def calcular_restos_sardinas_patterson(conjuntoA, conjuntoB):
    resultados = set()
    for a in conjuntoA:
        for b in conjuntoB:
            if es_prefijo(a, b):
                resultados.add(b[len(a) :])
            elif es_prefijo(b, a):
                resultados.add(a[len(b) :])
    return resultados


def es_univoco(palabras):
    if not es_no_singular(palabras):
        return False

    c = set(palabras)
    actual = calcular_restos_sardinas_patterson(c, c)
    vistos = [actual]

    while len(actual) > 0:
        if actual & c:
            return False
        nuevo = calcular_restos_sardinas_patterson(actual, c)
        if len(nuevo) == 0:
            return True
        if nuevo in vistos:
            return True
        vistos.append(nuevo)
        actual = nuevo
    return True

def comparar_codigos(codA , codB):
    prefijo = False
    sobrante = ""
    codA = list(codA)
    codB = list(codB)
    if (len(codA) > len(codB)):
        if (codA[:len(codB)] == codB):
            prefijo = True
            sobrante = "".join(codA[len(codB):]) # devuelve los valores de los sobrantes de la lista y se hace un join
    else:
        if (codB[:len(codA)] == codA):
            prefijo = True
            sobrante = "".join(codB[len(codA):])  # devuelve los valores de los sobrantes de la lista y se hace un join
    return sobrante , prefijo


def es_no_singular(lista):
    val = True
    i = 0
    while i < len(lista) and val:
        j = 0
        while (j < len(lista) and val):
            if (j != i):
                if (lista[j] == lista[i]):
                    val = False
            j += 1
        i += 1
    return val

def es_instantaneo(lista):
    val = True
    i = 0
    S = lista.copy()
    while (i < len(lista) and val):
        j = 0
        while (j < len(lista) and val):
            if (i != j):
                sobrante , prefijo = comparar_codigos(S[i] , S[j])
                if (prefijo):
                    val = False
            j += 1
        i += 1
    return val


# Genera 2 listas de extension de orden n, una con las palabras y otra con las probabilidades
def get_lista_extension_n(alfabeto, probabilidades, N):
    extensiones = []
    probabilidades_ext = []
    M = len(alfabeto)
    for i in range(M ** N):
        numero = i
        nuevas_extensiones = []
        nuevas_probabilidades = 1
        for k in range(N):                         # Cada valor de 0 a (M elevado a N) -1 Se le asigna una combinacion unica
            posicion = numero % M        
            nuevas_extensiones.insert(0,alfabeto[posicion])
            nuevas_probabilidades *= probabilidades[posicion]
            numero = numero // M # devuelve el cociente menor en entero ej 7 // 2 = 3
        extensiones.append("".join(nuevas_extensiones))
        probabilidades_ext.append(nuevas_probabilidades)
    return extensiones, probabilidades_ext  # ["AB", "AC", "BC"...]   [0.333, 0.222, 0.125, ...]

# Crear funcion de clasificar
def clasificar(listaCod : list[str], listaProb: list[float]):
    esUnivoco = es_univoco(listaCod)
    esNoSingular = es_no_singular(listaCod)
    esInstantaneo = es_instantaneo(listaCod)
    print(f"Clasificacion de codigo: {'  '.join(listaCod)}")
    if esInstantaneo:
        print("Instantaneo")
    else:
        if esUnivoco:
            print("Univoco")
        else:
            if esNoSingular:
                print("No singular")
            else:
                print("Bloque")
    esCompacto = es_compacto(listaProb, listaCod)     
    if (esInstantaneo or esUnivoco) and esCompacto:
        print("Es compacto")
    else:
        print("No es compacto")

# Genera 2 listas de extension de orden n, una con las palabras y otra con las probabilidades
def get_lista_extension_n(alfabeto, probabilidades, N):
    extensiones = []
    probabilidades_ext = []
    M = len(alfabeto)
    for i in range(M ** N):
        numero = i
        nuevas_extensiones = []
        nuevas_probabilidades = 1
        for k in range(N):                         # Cada valor de 0 a (M elevado a N) -1 Se le asigna una combinacion unica
            posicion = numero % M        
            nuevas_extensiones.insert(0,alfabeto[posicion])
            nuevas_probabilidades *= probabilidades[posicion]
            numero = numero // M # devuelve el cociente menor en entero ej 7 // 2 = 3
        extensiones.append("".join(nuevas_extensiones))
        probabilidades_ext.append(nuevas_probabilidades)
    return extensiones, probabilidades_ext  # ["AB", "AC", "BC"...]   [0.333, 0.222, 0.125, ...]

# Imprime matriz de prob en una cuadricula espaciada equitativamente, con lista de palabras opcionales
def imprimir_matriz(matrizProb : list[list[float]], listaPalabras : list[str] = []):
    print("{pal:^10}".format( pal = ""), end = "")
    n = len(matrizProb)
    if len(listaPalabras) == n:
        for i in range(n):
            print("{pal:^10}".format(pal = listaPalabras[i]), end = "")
    else:
        print("No se imprimen palabras en cuadricula por error de tamanio")
    
    print("")
    for i in range(n):
        for j in range(n):
            if j == 0:
                    if len(listaPalabras) == n:
                        print("{pal:^10}".format(pal = listaPalabras[i]), end = "")
            print("{prob:^10.3f}".format(prob = matrizProb[i][j]), end = "")
        print("")

# Imprime lista de prob con lista de palabras opcional
def imprimir_lista(listaProb : list[float], listaPalabras : list[str] = []):
    n = len(listaProb)
    if len(listaPalabras) == n:
        print("{pal:>10}".format(pal = "PALABRA"), end = "")
        for i in range(n):
            print("{pal:^10}".format(pal = listaPalabras[i]), end = "")
        print("")
    else:
        print("No se imprimen palabras en cuadricula por error de tamanio")
    
    print("{pal:>10}".format(pal = "PROB"), end = "")
    for i in range(n):
        print("{prob:^10.3f}".format(prob = listaProb[i]), end = "")
    print("")

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

