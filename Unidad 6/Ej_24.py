from math import log2
from math import log
from math import exp
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

def get_entropia_tamanio_r(listaProb: list[float], tamanioAlfabeto: int):
    total = 0
    for prob in listaProb:
        total += prob * log(1/prob, tamanioAlfabeto)
    return total

# Entropia de un numero si su prob es equiprobable
def get_entropia_equiprob(num: int): # ej: dado de 6, es como si hubiera 6 elementos de 1/6 de prob
    return log2(num)


# Crea listas de alfabeto y probabilidades con caracteres de mensajes
def get_listas_alf_prob(mensaje: str):  # ej: "casa"
    listaAlf = [] 
    listaProb = []

    listaAlf = sorted(set(mensaje)) # Asi siempre aparecen ordenadas

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
    return probabilidades_ext, extensiones  # ["AB", "AC", "BC"...]   [0.333, 0.222, 0.125, ...]

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
    return probabilidades_ext, extensiones   # ["AB", "AC", "BC"...]   [0.333, 0.222, 0.125, ...]

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

####################################################### UNIDAD 4 ##################################################################

# Cuando la longitud de orden n del codigo esta entre la entropia de la fuente y la entropia de la fuente
# Si H <= Ln/N <= H + 1
def primer_teorema_shanon(listaProb : list[float], listaCodOrdenN: list[str], N: int):
    longitudMedia = get_longitud_media_codigo(listaProb, listaCodOrdenN) 
    print("longitud: " + str(longitudMedia))
    r = get_r(listaCodOrdenN)
    entropia =  get_entropia_tamanio_r(listaProb, r) 
    print("entropia: " + str(entropia/ N))
    valor = (entropia / N <= longitudMedia / N and longitudMedia / N < entropia / N + 1 / N)
    return valor

def ordenar_por_probabilidad(listaProb: list[float],
                             listaCod: list[str]) -> tuple[list[float], list[str]]:
    pares = list(zip(listaProb, listaCod))
    pares.sort(key=lambda par: par[0], reverse=True)

    listaProbOrdenada = [par[0] for par in pares]
    listaCodOrdenada = [par[1] for par in pares]

    return listaProbOrdenada, listaCodOrdenada

# Dada una funcion de base r se calcula su rendimiento y redundancia, devolviendo ambas
def calcula_rendimiento_redundancia(listaProb: list[float], listaCod: list[str]):
    r = get_r(listaCod)
    entropia = get_entropia_tamanio_r(listaProb, r)
    longitud = get_longitud_media_codigo(listaProb, listaCod)
    
    rendimiento  = entropia / longitud
    redundancia = 1 - rendimiento

    return rendimiento, redundancia

def distancia_palabras_hamming(cod1: str, cod2: str) -> int:
    distancia = 0
    for i in range(len(cod1)):
        if cod1[i] != cod2[i]:
            distancia += 1

    return distancia

def get_min_distancia_deteccion_correccion_hamming(listaCod: list[str]) -> tuple[int, int, int]:
    distanciaMin : int = 99999
    n = len(listaCod)
    for i in range(n):
        for j in range(n):
            if(i != j):
                distancia = distancia_palabras_hamming(listaCod[i], listaCod[j])
                if distancia < distanciaMin:
                    distanciaMin = distancia
    deteccion : int = distanciaMin - 1
    correccion : int = math.floor(( (distanciaMin - 1) / 2 ))
    return distanciaMin, deteccion, correccion

def imprimir_hamming(listas: tuple[int, int, int]):
    print("Distancia: " + str(listas[0]))
    print("Detecta: " + str(listas[1]))
    print("Corrige: " + str(listas[2]))

# Cuenta la cantidad de "1" en un string de binarios y devuelve si tiene cantidad par o no
def tiene_paridad_par(bin: str):
    cantUnos = 0
    for bit in bin:
        if bit == "1":
            cantUnos += 1
    return (cantUnos % 2) == 0

# Convierte un caracter en un binario con el ultimo bit como bit de paridad
def get_caracter_a_binario(car: str):
    binario = bin(ord(car))[2:]
    if tiene_paridad_par(binario):
        binario += "0"
    else:
        binario += "1"
    return binario


####################################################### UNIDAD 6 ##################################################################

def get_matriz_canal(entrada: str, salida: str):
    alfabeto_entrada = sorted(set(entrada))
    alfabeto_salida = sorted(set(salida))

    N = len(alfabeto_entrada)
    M = len(alfabeto_salida)
    matriz = [[0 for _ in range(M)] for _ in range(N)]

    for i in range(len(entrada)):
        simbolo_entrada = entrada[i]
        simbolo_salida = salida[i]

        indice_entrada = alfabeto_entrada.index(simbolo_entrada)
        indice_salida = alfabeto_salida.index(simbolo_salida)

        matriz[indice_entrada][indice_salida] +=  1

    for i in range(len(alfabeto_entrada)):
        for j in range(len(alfabeto_salida)):
            entrada_apariciones = (list(entrada)).count(alfabeto_entrada[i])
            matriz[i][j] /= entrada_apariciones

    return matriz


# Usa las prob a priori y matriz transicion del canal/prob condicional y devuelve una lista con las prob de salida
def get_lista_probabilidades_salida(prob_a_priori : list[float], matriz_transicion_canal: list[list[float]]):
    lista_salida : list[float] = []
    r = len(prob_a_priori)
    m = len(matriz_transicion_canal[0])
    for j in range(m):
        lista_salida.append(0)
        for i in range(r):
            lista_salida[j] += prob_a_priori[i] * matriz_transicion_canal[i][j]
    return lista_salida


# Usa las prob a priori y matriz transicion canal para obtener la matriz prob a priori
def get_matriz_probabilidades_a_posteriori(prob_a_priori : list[float], matriz_transicion_canal: list[list[float]]):
    r = len(prob_a_priori)
    m = len(matriz_transicion_canal[0])

    # Denominador: denominadores[j] = suma sobre k de P(b_j|a_k) * P(a_k)
    denominadores = []
    for j in range(m):
        suma = 0
        for k in range(r):
            suma += matriz_transicion_canal[k][j] * prob_a_priori[k]
        denominadores.append(suma)

    # Teorema de Bayes
    matriz_prob_posteriori = []
    for i in range(r):
        fila = []
        for j in range(m):
            fila.append(matriz_transicion_canal[i][j] * prob_a_priori[i] / denominadores[j])
        matriz_prob_posteriori.append(fila)

    return matriz_prob_posteriori

# Prob simultaneo
# Prob conjunta: P(a,b) = P(ai/bj).P(bj) = P(bj/ai).P(ai)
def get_matriz_prob_conjunta(prob_a_priori : list[float], matriz_transicion_canal: list[list[float]]):
    """
    prob_a_priori:   lista de largo r, p_a[i] = P(a_i)
    matriz_transicion_canal: matriz (r x m), canal[i][j] = P(b_j | a_i)
    Devuelve: matriz (r x m), resultado[i][j] = P(a_i, b_j)
    """
    r = len(prob_a_priori)
    m = len(matriz_transicion_canal[0])

    matriz_prob_conjunta = []
    for i in range(r):
        fila = []
        for j in range(m):
            fila.append(matriz_transicion_canal[i][j] * prob_a_priori[i])
        matriz_prob_conjunta.append(fila)

    return matriz_prob_conjunta

# Representa el numero medio de bits necesarios para definir la entrada tras la recepcion y lectura del simbolo bj
def get_entropia_a_posteriori(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    """
    Devuelve la lista [H(A|b_1), H(A|b_2), ...] en bits.
 
    prob_a_priori: lista con P(a_i).
    matriz_transicion_canal: una fila por cada a_i, con P(b_j | a_i).
    """
    n_a = len(prob_a_priori)
    n_b = len(matriz_transicion_canal[0])
    entropias = []
 
    for j in range(n_b):
        # Conjunta P(a_i, b_j) y marginal P(b_j)
        conjunta = [prob_a_priori[i] * matriz_transicion_canal[i][j] for i in range(n_a)]
        prob_b = sum(conjunta)
 
        # Posterior P(a_i | b_j) y su entropía
        posterior = [c / prob_b for c in conjunta]
        entropias.append(-sum(p * log2(p) for p in posterior if p > 0))
 
    return entropias

# Entropia de salida H(B): entropia de la distribucion de probabilidades de salida
def get_entropia_salida(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    prob_b = get_lista_probabilidades_salida(prob_a_priori, matriz_transicion_canal)
    return get_entropia_lista_prob(prob_b)

# Mide la informacion que queda en A despues de observar B, repesenta la perdida de informacion sobre A causada por el canal
# H(A/B)
def get_ruido(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    prob_b = get_lista_probabilidades_salida(prob_a_priori, matriz_transicion_canal)
    h_posteriori = get_entropia_a_posteriori(prob_a_priori, matriz_transicion_canal)
    return sum(pb * h for pb, h in zip(prob_b, h_posteriori))

# Incertidumbre de la salida conociendo la entrada
# H(B/A)
def get_perdida(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    total = 0
    for i, fila in enumerate(matriz_transicion_canal):
        h_fila = sum(p * log2(1 / p) for p in fila if p > 0)
        total += prob_a_priori[i] * h_fila
    return total

# Es la suma H(A,B) = de H(A) + H(B/A) = H(B) + H(B/A) = H(B,A)
def get_entropia_afin(prob_a_priori, matriz_transicion_canal):
    conjunta = get_matriz_prob_conjunta(prob_a_priori, matriz_transicion_canal)
    return sum(p * log2(1 / p) for fila in conjunta for p in fila if p > 0)


# Informacion mutua: I(A;B) = H(A) - H(A|B)
def get_informacion_mutua(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    return get_entropia_lista_prob(prob_a_priori) - get_ruido(prob_a_priori, matriz_transicion_canal)

# Canal sin ruido: un solo elemento distinto de cero en cada columna
# Si H(A/B) = 0 luego se cumple que I(A,B) = H(A)
def es_canal_sin_ruido(prob: list[float], matriz: list[list[float]]):
    ruido = get_ruido(prob, matriz)
    return ruido == 0

# Canal determinante: un solo elemento distinto de cero en cada fila
# Si H(B/A) = 0 luego se cumple que I(A,B) = H(B)
def es_canal_determinante(prob: list[float], matriz: list[list[float]]):
    perdida = get_perdida(prob, matriz)
    return perdida == 0

# De un canal P y un canal determinante se devuelve un canal reducido
def get_canal_compuesto(canal1: list[list[float]], canal2: list[list[float]]):
    n = len(canal1)
    m = len(canal1[0])
    k = len(canal2[0])

    if len(canal2) != m:
        print("Error no se puede devolver canal reducido")
        return []

    resultado = [[0.0] * k for _ in range(n)]
    for i in range(n):
        for j in range(k):
            for y in range(m):
                resultado[i][j] += canal1[i][y] * canal2[y][j]

    return resultado

def validar_columnas(canal, j1, j2):
    m = len(canal[0])
    if j1 == j2:
        raise ValueError("Los índices de las columnas deben ser distintos.")
    if not (0 <= j1 < m and 0 <= j2 < m):
        raise ValueError(f"Los índices deben estar entre 0 y {m - 1}.")


def es_reduccion_suficiente(canal, j1, j2, tol=1e-9):
    """
    Verifica si las columnas j1 y j2 se pueden combinar (sumar) en una
    reducción suficiente, es decir, sin perder información sobre la entrada.

    Condición: las columnas son proporcionales, o sea que para todo par de
    filas i, l se cumple canal[i][j1] * canal[l][j2] == canal[l][j1] * canal[i][j2].
    Equivale a que P(x|y1) = P(x|y2) para todo x.
    """
    validar_columnas(canal, j1, j2)
    n = len(canal)

    for i in range(n):
        for l in range(i + 1, n):
            if abs(canal[i][j1] * canal[l][j2] - canal[l][j1] * canal[i][j2]) > tol:
                return False
    return True


def canal_determinante(canal, j1, j2):
    """
    Genera la matriz del canal determinante que combina las columnas j1 y j2.

    Es una matriz de m filas (salidas originales) x (m-1) columnas (salidas
    reducidas). La columna combinada queda en la posición min(j1, j2) y la
    otra columna se elimina; el resto conserva su orden.
    Cada fila tiene un único 1 (canal determinístico).
    """
    validar_columnas(canal, j1, j2)
    m = len(canal[0])
    menor, mayor = min(j1, j2), max(j1, j2)

    det = [[0.0] * (m - 1) for _ in range(m)]
    for c in range(m):
        if c == mayor:
            destino = menor
        elif c > mayor:
            destino = c - 1
        else:
            destino = c
        det[c][destino] = 1.0
    return det


def get_reduccion_suficiente(canal, tol=1e-9):
    """
    Reduce el canal lo más posible combinando columnas mientras exista
    algún par que sea una reducción suficiente.

    Devuelve (canal_reducido, determinante_total), donde
    canal_reducido = canal en serie con determinante_total.
    """
    actual = [fila[:] for fila in canal]
    m = len(actual[0])
    det_total = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]

    while True:
        m = len(actual[0])
        combinado = False
        for j1 in range(m):
            for j2 in range(j1 + 1, m):
                if es_reduccion_suficiente(actual, j1, j2, tol):
                    det = canal_determinante(actual, j1, j2)
                    actual = get_canal_compuesto(actual, det)
                    det_total = get_canal_compuesto(det_total, det)
                    combinado = True
                    break
            if combinado:
                break
        if not combinado:
            return actual, det_total


# Valor maximo al cual la informacion puede ser transmitida por un canal
def get_capacidad(canal: list[list[float]], tol=1e-12, max_iter=10000):
    n, m = len(canal), len(canal[0])
    prob_entrada = [1 / n] * n

    for _ in range(max_iter):
        py = [sum(prob_entrada[i] * canal[i][j] for i in range(n)) for j in range(m)]

        # Divergencia D(P(.|x) || p(y)) en nats para cada entrada
        d = []
        for i in range(n):
            s = 0.0
            for j in range(m):
                if canal[i][j] > 0:
                    s += canal[i][j] * log(canal[i][j] / py[j])
            d.append(s)

        nuevo = [prob_entrada[i] * exp(d[i]) for i in range(n)]
        total = sum(nuevo)
        nuevo = [v / total for v in nuevo]

        if max(abs(nuevo[i] - px[i]) for i in range(n)) < tol:
            px = nuevo
            break
        prob_entrada = nuevo

    return get_informacion_mutua_matriz_lista(canal, prob_entrada), prob_entrada


# Variante auxiliar para informacion mutua entre matriz y lista
def get_informacion_mutua_matriz_lista(canal: list[list[float]], prob_entrada: list[float]):
    n, m = len(canal), len(canal[0])
    py = [sum(prob_entrada[i] * canal[i][j] for i in range(n)) for j in range(m)]
    info = 0.0
    for i in range(n):
        for j in range(m):
            if prob_entrada[i] > 0 and canal[i][j] > 0:
                info += prob_entrada[i] * canal[i][j] * log2(canal[i][j] / py[j])
    return info

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

canal3 = [
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5],
    [0.5, 0.2, 0.3],
]
c, prob_entrada = get_capacidad(canal3)
print(c)   # ≈ 0.0995 bits
print(prob_entrada)  # ≈ [1/3, 1/3, 1/3]

ejemplos = {
#    "a" : (prob_a, canal_a),
#    "b" : (prob_b, canal_b),
#    "red": (prob_reducido, canal_reducido)
}

for nombre, (prob, matriz) in ejemplos.items():
    entropia_a_priori = get_entropia_lista_prob(prob)
    entropia_salida = get_entropia_salida(prob, matriz)
    print(nombre)
    #print("a) Entropia a priori y posteriori:")
    #print(f"{'Entropia a priori:':<25}", f"{entropia_a_priori:.4f}")
    #print(f"{'b)Entropia salida:':<25}", f"{entropia_salida:.4f}")
    sin_ruido = es_canal_sin_ruido(prob, matriz)
    determinante = es_canal_determinante(prob, matriz)


    ruido = get_ruido(prob, matriz)
    perdida = get_perdida(prob, matriz)
    print(f"{' Ruido/Equivocacion:':<25}", f"{ruido:.4f}")
    #print(f"{' Perdida:':<25}", f"{perdida:.4f}")
    
    entropia_afin = get_entropia_afin(prob, matriz)
    #print(f"{'e) Entropia afin:':<25}" , f"{entropia_afin:.4f}")

    info_mutua = get_informacion_mutua(prob, matriz)
    print(f"{' Info mutua:':<25}" , f"{info_mutua:.4f}")

