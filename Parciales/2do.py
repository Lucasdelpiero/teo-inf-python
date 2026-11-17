from math import log2
from math import log
from math import exp
import math
import random

TOLERANCIA = 0.001  

################################################### UNIDAD 2 ######################################################################

############# Funciones para mensajes y listas de alfabeto y probabilidad, obtener entropia  ######################################

def get_lista_bits_necesarios(listaProb: list[float]):
    """Devuelve una lista con la cantidad de bits necesarios para representar cada simbolo"""
    nuevaLista = []
    for prob in listaProb:
        nuevaLista.append(log2(1/prob )) 
    return nuevaLista

def get_entropia_lista_prob(listaProb: list[float]):
    """Entropia de una lista de probabilidades"""
    total = 0

    for prob in listaProb:
        total += prob * log2(1/prob)
    return total

def get_entropia_tamanio_r(listaProb: list[float], tamanioAlfabeto: int):
    total = 0
    for prob in listaProb:
        total += prob * log(1/prob, tamanioAlfabeto)
    return total

def get_entropia_equiprob(num: int): # ej: dado de 6, es como si hubiera 6 elementos de 1/6 de prob
    """Entropia de un numero si su prob es equiprobable"""
    return log2(num)


def get_listas_alf_prob(mensaje: str):  # ej: "casa"
    """Crea listas de alfabeto y probabilidades con caracteres de mensajes"""
    listaAlf = [] 
    listaProb = []

    listaAlf = sorted(set(mensaje)) # Asi siempre aparecen ordenadas

    for letra in listaAlf:
        listaProb.append(mensaje.count(letra)/len(mensaje))

        
    return [listaAlf, listaProb] # listas = crearListasAlfProb(mensaje)  ;  listaAlf = listas[0] ;    listaProb = listas[1]

def get_lista_alf_lista(lista: list[str]): # 
    """Obtiene lista alfabeto de una LISTA\n
    EJ: ["001", "01", "012"]"""
    listaAlf = []
    for mensaje in lista:
        for letra in mensaje:
            if letra not in listaAlf:
                listaAlf.append(letra)
    return listaAlf # ["0", "1", "2"]


def get_num(n: int, acum):
    """Funcion auxiliar de genPalabra\n
    Segun el numero ingresado devuelve la pos del elemento segun su probabilidad acumulada"""
    for i in range(len(acum)):
        if n < acum[i]:
            return i

def gen_palabra(n: int, listaAlf: list[str], listaProb: list[float]):
    """Genera palabra ALEATORIA de largo N """
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


def tiene_memoria(matriz: list[list], tolerancia: float = 0.0001):
    """Si no tiene memoria, todos los valores de una fila deben ser similares (dentro de la tolerancia)\n
    Si tiene memoria, estos estaran por fuera de la tolerancia"""
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

def get_alfabeto_matriz_transicion(mensaje: str):
    """Matriz transicion obtenida de un mensaje"""
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


def get_vector_estacionario(matriz: list[list], tolerancia: float):
    """Vector estacionario asumiendo inicialmente que son equiprobables"""
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

def mult_matriz_vec(matriz: list[list], vector: list[float]):
    """Auxiliar para multiplicar matrices para obtener el estacionario"""
    n = len(matriz)
    nuevoValor : list = [0] * n
    for i in range(n):
        for j in range(n):
            nuevoValor[i] += matriz[i][j] * vector[j]
    return nuevoValor

def get_entropia_matriz(matriz: list[list], estacionario: list[float]):
    """Entropia obtenida usando matriz y estacionario"""
    n = len(estacionario)
    total = 0
    for i in range(n):
        for j in range(n):
            if (matriz[i][j] != 0):
                total += estacionario[i] * matriz[i][j] * log2(1/matriz[i][j])
    return total

####################################################### UNIDAD 3 ##################################################################

def get_sumatoria_kraft(listaPalabras: list[str]):
    """Se usa para inecuacion de kraft, si:    SUMATORIA <= 1 es condificion suficiente para la existencia de \n
    AL MENOS 1 codigo INSTANTANEO de tal longitud\n
    Por inecuacion MacMillan si es > 1 entonces no se puede definir un codigo UNIVOCO ni INSTANTANEO"""
    alfabeto = get_lista_alf_lista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo
    total = 0
    for palabra in listaPalabras:
        li = len(palabra)       # li = largo de la palabra especifica
        total += r **  (-li)
    return total

def get_r(listaPalabras: list[str]):
    """Funcion auxiliar para obtener el R (cant de simbolos de alfabeto codigo)"""
    alfabeto = get_lista_alf_lista(listaPalabras)
    r = len(alfabeto)
    return r

def get_longitud_media_codigo(listaProb: list[float], listaPalabras: list[str]):
    """Largo PROMEDIO de codigo usando su prob y largo de palabras"""
    total = 0
    n = len(listaPalabras)
    for i in range(n):
        prob = listaProb[i]
        largo = len(listaPalabras[i])
        total += prob * largo
    return total

def get_entropia_ponderada_largo(listaProb: list[float], listaPalabras: list[str]):
    """Obtiene la entropia considerando PROB y LARGO de cada palabra codigo"""
    total = 0
    n = len(listaPalabras)
    alfabeto = get_lista_alf_lista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo

    for i in range(n):
        prob = listaProb[i]
        total += prob * math.log(1/prob, r)
    return total


def es_compacto(listaProb: list[float], listaCod: list[str]):
    """Booleano que devuelve si un codigo es compacto usando su lista de prob y el largo de cada palabra codigo"""
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
    """Devuelve true si tiene algun prefijo en la lista de palabras"""
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


def get_lista_extension_n(alfabeto, probabilidades, N):
    """Genera 2 listas de extension de orden n, una con las palabras y otra con las probabilidades"""
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

def clasificar(listaCod : list[str], listaProb: list[float]):
    """Crear funcion de clasificar"""
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

def get_lista_extension_n(alfabeto, probabilidades, N):
    """Genera 2 listas de extension de orden n, una con las palabras y otra con las probabilidades"""
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

def imprimir_matriz(matrizProb : list[list[float]], listaPalabras : list[str] = []):
    """Imprime matriz de prob en una cuadricula espaciada equitativamente, con lista de palabras opcionales"""
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

def imprimir_lista(listaProb : list[float], listaPalabras : list[str] = []):
    """Imprime lista de prob con lista de palabras opcional"""
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

def primer_teorema_shanon(listaProb : list[float], listaCodOrdenN: list[str], N: int):
    """Significa que el codigo es suficientemente eficiente/compacto\n
    Cuando la longitud de orden n del codigo esta entre la entropia de la fuente y la entropia de la fuente\n
    Si H <= Ln/N <= H + 1"""
    longitudMedia = get_longitud_media_codigo(listaProb, listaCodOrdenN) 
    r = get_r(listaCodOrdenN)
    entropia =  get_entropia_tamanio_r(listaProb, r) 
    valor = (entropia / N <= longitudMedia / N and longitudMedia / N < entropia / N + 1 / N)
    return valor

def ordenar_por_probabilidad(listaProb: list[float],
                             listaCod: list[str]) -> tuple[list[float], list[str]]:
    pares = list(zip(listaProb, listaCod))
    pares.sort(key=lambda par: par[0], reverse=True)

    listaProbOrdenada = [par[0] for par in pares]
    listaCodOrdenada = [par[1] for par in pares]

    return listaProbOrdenada, listaCodOrdenada

def calcula_rendimiento_redundancia(listaProb: list[float], listaCod: list[str]):
    """Dada una funcion de base r se calcula su rendimiento y redundancia, devolviendo ambas\n
    return rendimiento, redundancia"""
    r = get_r(listaCod)
    entropia = get_entropia_tamanio_r(listaProb, r)
    longitud = get_longitud_media_codigo(listaProb, listaCod)
    
    rendimiento  = entropia / longitud
    redundancia = 1 - rendimiento

    return rendimiento, redundancia

def distancia_palabras_hamming(cod1: str, cod2: str) -> int:
    """Es la cantidad de bits de diferencia entre los codigos para que uno se convierta en el otro"""
    distancia = 0
    for i in range(len(cod1)):
        if cod1[i] != cod2[i]:
            distancia += 1

    return distancia

def get_min_distancia_deteccion_correccion_hamming(listaCod: list[str]) -> tuple[int, int, int]:
    """Indica cual es la distancia minima para que haya un error
       la cant de errores que puede detectar  
       y la cantidad de correcciones que puede hacer
    """
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
    """Se usa para imprimir el resultado de get_min_distancia_deteccion_correccion_hamming"""
    print("Distancia: " + str(listas[0]))
    print("Detecta: " + str(listas[1]))
    print("Corrige: " + str(listas[2]))


def tiene_paridad_par(bin: str):
    """ Cuenta la cantidad de "1" en un string de binarios y devuelve si tiene cantidad par o no """
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


# Ejemplo de uso abajo
def a_bytearray(*bytes_bin: str) -> bytearray:
    """Convierte cadenas de bits ('00100001', ...) a bytearray."""
    return bytearray(int(b, 2) for b in bytes_bin)
 
 # Cada string es una fila de la matriz 
EJEMPLOS = {
    "a": a_bytearray("00100001", "10000111", "10000010", "10100110", "10000010"),
    "b": a_bytearray("00101101", "10011001", "10001010", "10011100", "10000010"),
    "c": a_bytearray("00101010", "10000010", "10011010", "10011111", "10100101"),
    "d": a_bytearray("00010100", "10010000", "10011110", "10011001", "10000010"),
    "e": a_bytearray("00110101", "10011010", "10101011", "10100100", "10000010"),
    "f": a_bytearray("00001001", "10101001", "10100101", "10001011", "10100110"),
    "g": a_bytearray("00011101", "10010011", "10011101", "10001100", "10011111"),
    "h": a_bytearray("00111110", "10000111", "10010000", "10000010", "10101010"),
}

def bits_a_bytearray(bits: str) -> bytearray:
    """Convierte una cadena de unos y ceros en un bytearray (8 bits por byte).
    Ignora espacios y saltos de línea."""
    bits = "".join(bits.split())
    if set(bits) - {"0", "1"}:
        raise ValueError("La cadena solo puede tener 0 y 1 (y espacios)")
    if len(bits) % 8:
        raise ValueError(f"La cantidad de bits ({len(bits)}) no es múltiplo de 8")
    return bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
 

def bits_a_bytearray(bits: str) -> bytearray:
    """Convierte una cadena de unos y ceros en un bytearray (8 bits por byte).
    Ignora espacios y saltos de línea."""
    bits = "".join(bits.split())
    if set(bits) - {"0", "1"}:
        raise ValueError("La cadena solo puede tener 0 y 1 (y espacios)")
    if len(bits) % 8:
        raise ValueError(f"La cantidad de bits ({len(bits)}) no es múltiplo de 8")
    return bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
 
 
def bytes_a_matriz(datos) -> list[list[int]]:
    """bytes -> lista de cadenas binarias -> matriz de enteros (0/1)."""
    cadenas = [format(b, "08b") for b in datos]
    return [[int(c) for c in cadena] for cadena in cadenas]
 
 
def matriz_a_bytes(matriz: list[list[int]]) -> bytearray:
    """Matriz de bits -> lista de cadenas binarias -> bytearray."""
    cadenas = ["".join(str(bit) for bit in fila) for fila in matriz]
    return bytearray(int(cadena, 2) for cadena in cadenas)
 
 
# --------------------------------------------------------------------- paridad
 
def paridad(bits) -> int:
    """Bit que completa paridad par: 1 si hay cantidad impar de unos."""
    return sum(bits) % 2
 
 
def filas_incorrectas(matriz) -> list[int]:
    """Índices de las filas con paridad impar (error de VRC)."""
    return [i for i, fila in enumerate(matriz) if paridad(fila)]
 
 
def columnas_incorrectas(matriz) -> list[int]:
    """Índices de las columnas con paridad impar (error de LRC / cruzada)."""
    return [j for j, columna in enumerate(zip(*matriz)) if paridad(columna)]
 
 
# ---------------------------------------------------------------- codificación
 
def get_string_a_bytearray(texto: str) -> bytearray:
    """Genera el bytearray con el LRC al inicio y cada carácter con su VRC."""
    filas = []
    for c in texto:
        codigo = ord(c)
        if codigo > 127:
            raise ValueError(f"El carácter {c!r} no es ASCII (7 bits)")
        bits = [int(b) for b in format(codigo, "07b")]
        bits.append(paridad(bits))                      # VRC en el bit 0
        filas.append(bits)
 
    # LRC: paridad de cada columna (la última columna, la de los VRC,
    # da la paridad cruzada)
    lrc = [paridad(columna) for columna in zip(*filas)] if filas else [0] * 8
    return matriz_a_bytes([lrc] + filas)
 
 
def verificar(datos: bytearray) -> bool:
    """True si todas las filas y todas las columnas tienen paridad par."""
    matriz = bytes_a_matriz(datos)
    return bool(matriz) and not filas_incorrectas(matriz) and not columnas_incorrectas(matriz)
 
 
# ---------------------------------------------------------------- decodificación
 
def corregir_matriz_mensaje(matriz: list[list[int]]):
    """
    Devuelve la matriz corregida, o None si no se puede corregir.
    Solo se corrige un error de un único bit: la fila con VRC incorrecto y la
    columna con LRC incorrecto se cruzan en el bit erróneo.
    """
    matriz = [fila[:] for fila in matriz]               # copia
    filas_mal = filas_incorrectas(matriz)
    columnas_mal = columnas_incorrectas(matriz)
 
    if not filas_mal and not columnas_mal:
        return matriz                                   # sin errores
    if len(filas_mal) == 1 and len(columnas_mal) == 1:
        matriz[filas_mal[0]][columnas_mal[0]] ^= 1      # invierte el bit erróneo
        return matriz
    return None                                         # no corregible
 
 
def get_bytearray_a_string(datos: bytearray) -> str:
    """Devuelve el mensaje original corregido, o "" si no se pueden corregir los errores."""
    matriz = bytes_a_matriz(datos)
    if not matriz:
        return ""
    matriz = corregir_matriz_mensaje(matriz)
    if matriz is None:
        return ""
 
    # Se descarta la fila del LRC (fila 0) y el bit de paridad (último bit)
    return "".join(chr(int("".join(map(str, fila[:7])), 2)) for fila in matriz[1:])

def corregir_bytearray_devolver_string(datos: bytearray) -> str:
    """Corrige mensaje en bytearray y lo devuelve como string\n
    solo llama a get_bytearray_a_string pero asi quiza es mas facil de encontrar"""
    return get_bytearray_a_string(datos)


def imprimir_bytearray_matriz(datos: bytearray):
    """ Imprime bytearray en forma de matriz """
    for fila in bytes_a_matriz(datos):
        print("  ", "".join(map(str, fila)))

####################################################### UNIDAD 5 ##################################################################

def get_codificacion_huffman(probabilidades: list[float]):
    """Devuelve la lista de códigos binarios de Huffman."""
    n = len(probabilidades)
    if n == 0:
        return []
    if n == 1:
        return ["0"]
 
    codigos = [""] * n
    # Cada nodo es (probabilidad, [índices de símbolos del grupo])
    nodos = [(p, [i]) for i, p in enumerate(probabilidades)]
 
    while len(nodos) > 1:
        # Ordenar por probabilidad creciente: los dos menores quedan al principio
        nodos.sort(key=lambda nodo: nodo[0])
        p1, grupo1 = nodos.pop(0)  # menor probabilidad
        p2, grupo2 = nodos.pop(0)  # siguiente menor
        for i in grupo1:
            codigos[i] = "0" + codigos[i]
        for i in grupo2:
            codigos[i] = "1" + codigos[i]
        nodos.append((p1 + p2, grupo1 + grupo2))
 
    return codigos
 
 
def get_codificacion_shannon_fano(probabilidades: list[float]):
    """Devuelve la lista de códigos binarios de Shannon-Fano."""
    n = len(probabilidades)
    if n == 0:
        return []
    if n == 1:
        return ["0"]
 
    codigos = [""] * n
    # Índices ordenados por probabilidad decreciente
    orden = sorted(range(n), key=lambda i: probabilidades[i], reverse=True)
 
    def dividir(indices):
        if len(indices) <= 1:
            return
        total = sum(probabilidades[i] for i in indices)
        # Punto de corte que minimiza la diferencia entre ambas mitades
        acumulado = 0.0
        mejor_corte, mejor_dif = 1, math.inf
        for corte in range(1, len(indices)):
            acumulado += probabilidades[indices[corte - 1]]
            dif = abs(total - 2 * acumulado)
            if dif < mejor_dif:
                mejor_dif, mejor_corte = dif, corte
        izq, der = indices[:mejor_corte], indices[mejor_corte:]
        for i in izq:
            codigos[i] += "0"
        for i in der:
            codigos[i] += "1"
        dividir(izq)
        dividir(der)
 
    dividir(orden)
    return codigos


def codificar_a_bytearray(alfabeto: list[str], codigos: list[str], mensaje: str):
    """Codifica `mensaje` (escrito con los símbolos de `alfabeto`).
    Los codigos son los que devuelve la codificacion de Huffman o Shannon Fano
    alfabeto: cadena con los símbolos fuente; alfabeto[i] se codifica
              con codigos[i].
    codigos:  lista de cadenas de '0' y '1'.
    Devuelve un bytearray.
    """
    if len(alfabeto) != len(codigos):
        raise ValueError("El alfabeto y la lista de códigos deben tener igual longitud")
 
    tabla = dict(zip(alfabeto, codigos))
    try:
        bits = "".join(tabla[simbolo] for simbolo in mensaje)
    except KeyError as e:
        raise ValueError(f"El símbolo {e.args[0]!r} no pertenece al alfabeto") from None
 
    relleno = (-len(bits)) % 8
    bits += "0" * relleno
 
    resultado = bytearray([relleno])
    for i in range(0, len(bits), 8):
        resultado.append(int(bits[i:i + 8], 2))
    return resultado
 
 
def decodificar_bytearray(alfabeto: str, codigos: str, datos: str):
    """Decodifica una secuencia de bytes generada por `codificar`.
    Los codigos son los que devuelve la codificacion de Huffman o Shannon Fano
    Devuelve el mensaje original como cadena de caracteres.
    """
    if len(alfabeto) != len(codigos):
        raise ValueError("El alfabeto y la lista de códigos deben tener igual longitud")
    if len(datos) == 0:
        raise ValueError("La secuencia de bytes está vacía")
 
    relleno = datos[0]
    bits = "".join(format(byte, "08b") for byte in datos[1:])
    if relleno:
        bits = bits[:-relleno]
 
    tabla = dict(zip(codigos, alfabeto))
    mensaje = []
    actual = ""
    for bit in bits:
        actual += bit
        if actual in tabla:  # al ser un código prefijo, la primera coincidencia es la correcta
            mensaje.append(tabla[actual])
            actual = ""
 
    if actual:
        raise ValueError("La secuencia de bits no corresponde a una codificación válida")
    return "".join(mensaje)

def imprimir_bits_bytearray(datos: bytearray):
    """Imprime el bytearray como secuencia de bits"""
    print("Bits:      ", "".join(format(b, "08b") for b in datos[1:]))


def get_tasa_compresion_bytearray(mensaje: str, codificado: bytearray) -> float:
    """Calcula la tasa de compresión: tamaño original / tamaño comprimido.
    mensaje:    cadena con el mensaje original (se mide en bytes UTF-8, o sea
                1 byte por carácter para texto ASCII).
    codificado: bytearray generado por `codificar_a_bytearray`. El primer byte
                es el de relleno y NO se cuenta en el tamaño comprimido.
    Un valor mayor que 1 indica que hubo compresión.
    """
    datos_comprimidos = len(codificado) - 1  # se descuenta el byte de relleno
    if datos_comprimidos <= 0:
        raise ValueError("La secuencia de bytes está vacía")
    return len(mensaje.encode("utf-8")) / datos_comprimidos


def get_tasa_compresion_str(mensaje: str, codificado: str, redondear_bytes: bool = False) -> float:
    """Calcula la tasa de compresión: tamaño original / tamaño comprimido.
    mensaje:         cadena con el mensaje original (se mide en bytes UTF-8, o sea
                     1 byte por carácter para texto ASCII).
    codificado:      string de bits ('0' y '1') generado por `codificar_a_string`.
    redondear_bytes: si es True, el tamaño comprimido se redondea hacia arriba a
                     bytes completos (como lo haría un archivo real, sin contar relleno).
    Un valor mayor que 1 indica que hubo compresión.
    """
    if len(codificado) == 0:
        raise ValueError("La secuencia codificada está vacía")
    tam_comprimido = len(codificado) / 8
    if redondear_bytes:
        tam_comprimido = math.ceil(tam_comprimido)
    return len(mensaje.encode("utf-8")) / tam_comprimido


def comprimir_rlc(mensaje: str) -> bytearray:
    """Comprime `mensaje` con RLC y devuelve un bytearray."""
    resultado = bytearray()
    i = 0
    while i < len(mensaje):
        caracter = mensaje[i]
        codigo = ord(caracter)
        if codigo > 255:
            raise ValueError(f"El carácter {caracter!r} no entra en un byte")
 
        # Contar repeticiones consecutivas del mismo carácter
        j = i
        while j < len(mensaje) and mensaje[j] == caracter:
            j += 1
        repeticiones = j - i
 
        # Un byte solo guarda hasta 255: se parte la racha si es más larga
        while repeticiones > 0:
            n = min(repeticiones, 255)
            resultado.append(codigo)
            resultado.append(n)
            repeticiones -= n
        i = j
 
    return resultado


def descomprimir_rlc(datos: bytearray) -> str:
    """Operación inversa: recupera el mensaje a partir del bytearray RLC."""
    if len(datos) % 2 != 0:
        raise ValueError("La secuencia debe tener pares de bytes (carácter, cantidad)")
    return "".join(chr(datos[i]) * datos[i + 1] for i in range(0, len(datos), 2))


def get_texto_rlc(datos: bytearray) -> str:
    """Devuelve el bytearray RLC en formato legible, por ejemplo U2O4A3I1E1U4."""
    if len(datos) % 2 != 0:
        raise ValueError("La secuencia debe tener pares de bytes (carácter, cantidad)")
    texto = "".join(chr(datos[i]) + str(datos[i + 1]) for i in range(0, len(datos), 2))
    return texto

def imprimir_lista_bytearray(datos: bytearray):
    """Imprime en numeros enteros los valores del bytearray"""
    print(list(datos))

####################################################### UNIDAD 6 ##################################################################

def get_matriz_canal(entrada: str, salida: str):
    """Devuelve la matriz de transicion de un canal dada tal entrada y salida en palabras"""
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


def get_lista_probabilidades_salida(prob_a_priori : list[float], matriz_transicion_canal: list[list[float]]):
    """Usa las prob a priori y matriz transicion del canal/prob condicional y devuelve una lista con las prob de salida"""
    lista_salida : list[float] = []
    r = len(prob_a_priori)
    m = len(matriz_transicion_canal[0])
    for j in range(m):
        lista_salida.append(0)
        for i in range(r):
            lista_salida[j] += prob_a_priori[i] * matriz_transicion_canal[i][j]
    return lista_salida


def get_matriz_probabilidades_a_posteriori(prob_a_priori : list[float], matriz_transicion_canal: list[list[float]]):
    """Usa las prob a priori y matriz transicion canal para obtener la matriz prob a posteriori"""
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


def get_matriz_prob_conjunta(prob_a_priori : list[float], matriz_transicion_canal: list[list[float]]):
    """
    Prob simultaneo\n
    Prob conjunta: P(a,b) = P(ai/bj).P(bj) = P(bj/ai).P(ai)\n
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

def get_entropia_a_priori(prob_a_priori: list[float]):
    """Si se trata de la entrada la medida de la incertidumbre sobre el simbolo que emitira la fuente antes de recibir un simbolo de salida determinado"""
    return get_entropia_lista_prob(prob_a_priori)


def get_entropia_a_posteriori(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    """
    Representa el numero medio de bits necesarios para definir la entrada tras la recepcion y lectura del simbolo bj
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

def get_entropia_salida(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    """Entropia de salida H(B): entropia de la distribucion de probabilidades de salida"""
    prob_b = get_lista_probabilidades_salida(prob_a_priori, matriz_transicion_canal)
    return get_entropia_lista_prob(prob_b)

def get_ruido(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    """H(A/B): Mide la informacion que queda en A despues de observar B, repesenta la perdida de informacion sobre A causada por el canal """
    prob_b = get_lista_probabilidades_salida(prob_a_priori, matriz_transicion_canal)
    h_posteriori = get_entropia_a_posteriori(prob_a_priori, matriz_transicion_canal)
    return sum(pb * h for pb, h in zip(prob_b, h_posteriori))

def get_perdida(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    """H(B/A): Incertidumbre de la salida conociendo la entrada"""
    total = 0
    for i, fila in enumerate(matriz_transicion_canal):
        h_fila = sum(p * log2(1 / p) for p in fila if p > 0)
        total += prob_a_priori[i] * h_fila
    return total

def get_entropia_afin(prob_a_priori, matriz_transicion_canal):
    """Incertidumbre total del par entrada / salida\n
        Es la suma H(A,B) = de H(A) + H(B/A) = H(B) + H(A/B) = H(B,A)"""
    conjunta = get_matriz_prob_conjunta(prob_a_priori, matriz_transicion_canal)
    return sum(p * log2(1 / p) for fila in conjunta for p in fila if p > 0)


def get_informacion_mutua(prob_a_priori: list[float], matriz_transicion_canal: list[list[float]]):
    """Informacion mutua: I(A;B) = H(A) - H(A|B)"""
    return get_entropia_lista_prob(prob_a_priori) - get_ruido(prob_a_priori, matriz_transicion_canal)


def es_canal_sin_ruido(prob: list[float], matriz: list[list[float]]):
    """Canal sin ruido: un solo elemento distinto de cero en cada columna\n
    Si H(A/B) = 0 luego se cumple que I(A,B) = H(A)"""
    ruido = get_ruido(prob, matriz)
    return ruido == 0


def es_canal_determinante(prob: list[float], matriz: list[list[float]]):
    """Canal determinante: un solo elemento distinto de cero en cada fila\n
    Si H(B/A) = 0 luego se cumple que I(A,B) = H(B)"""
    perdida = get_perdida(prob, matriz)
    return perdida == 0

def get_canal_compuesto(canal1: list[list[float]], canal2: list[list[float]]):
    """De un canal P y un canal determinante se devuelve un canal reducido"""
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

""" Funciono mal el px, por ahi sirve en otro momento
def get_capacidad(canal: list[list[float]], tol=1e-12, max_iter=10000):
    \"\"\"Valor maximo al cual la informacion puede ser transmitida por un canal"\""
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
"""

def get_capacidad(canal: list[list[float]], tol=1e-12, max_iter=10000):
    """Valor maximo al cual la informacion puede ser transmitida por un canal y la prob de entrada"""
    n, m = len(canal), len(canal[0])
    px = [1 / n] * n

    for _ in range(max_iter):
        py = [sum(px[i] * canal[i][j] for i in range(n)) for j in range(m)]

        # Divergencia D(P(.|x) || p(y)) en nats para cada entrada
        d = []
        for i in range(n):
            s = 0.0
            for j in range(m):
                if canal[i][j] > 0:
                    s += canal[i][j] * log(canal[i][j] / py[j])
            d.append(s)

        nuevo = [px[i] * exp(d[i]) for i in range(n)]
        total = sum(nuevo)
        nuevo = [v / total for v in nuevo]

        converge = max(abs(nuevo[i] - px[i]) for i in range(n)) < tol
        px = nuevo
        if converge:
            break

    # Capacidad = informacion mutua con la distribucion optima
    py = [sum(px[i] * canal[i][j] for i in range(n)) for j in range(m)]
    info = 0.0
    for i in range(n):
        for j in range(m):
            if canal[i][j] > 0:
                info += px[i] * canal[i][j] * log2(canal[i][j] / py[j])
    return info, px


def get_informacion_mutua_matriz_lista(canal: list[list[float]], prob_entrada: list[float]):
    """Variante auxiliar para informacion mutua entre matriz y lista"""
    n, m = len(canal), len(canal[0])
    py = [sum(prob_entrada[i] * canal[i][j] for i in range(n)) for j in range(m)]
    info = 0.0
    for i in range(n):
        for j in range(m):
            if prob_entrada[i] > 0 and canal[i][j] > 0:
                info += prob_entrada[i] * canal[i][j] * log2(canal[i][j] / py[j])
    return info

def es_canal_uniforme(canal: list[list[float]], tol=1e-9):
    """
    Devuelve True si todas las filas del canal son permutaciones entre sí,
    es decir, si todas contienen los mismos valores en distinto orden.
    """
    base = sorted(canal[0])
    for fila in canal[1:]:
        otra = sorted(fila)
        for a, b in zip(base, otra):
            if abs(a - b) > tol:
                return False
    return True


def get_capacidad_si_det_sinruido_uni(canal: list[list[float]]):
    """Calcula capacidad solo si es un canal: determinanto / sin ruido / uniforme"""
    if ( es_canal_determinante(canal) or es_canal_sin_ruido(canal) or es_canal_uniforme):
        return get_capacidad(canal)
    return 0

def capacidad_binaria(canal: list[list[float]], paso: int = 0.0001):
    """
    DEVUELVE P OPTIMO\n
    Estima la capacidad de un canal binario (2 entradas) recorriendo las
    probabilidades a priori p(x0) = 0, paso, 2*paso, ..., 1 y calculando la
    informacion mutua para cada una.

    canal: matriz de 2 filas (entradas 0 y 1) x m columnas (salidas)
    paso: separacion entre valores consecutivos de p(x0), entre 0 y 1

    Devuelve (capacidad_estimada, p), donde p es la probabilidad a priori
    p(x0) para la cual la informacion mutua es maxima. La distribucion de
    entrada completa es [p, 1 - p].
    """
    if len(canal) != 2:
        raise ValueError("El canal debe ser binario: 2 filas (2 entradas).")
    if not (0 < paso <= 1):
        raise ValueError("El paso debe estar en el intervalo (0, 1].")

    cantidad = int(round(1 / paso))
    mejor_info = -1.0
    mejor_p = 0.0

    for k in range(cantidad + 1):
        p = min(k * paso, 1.0)
        info = get_informacion_mutua_matriz_lista(canal, [p, 1 - p])
        if info > mejor_info:
            mejor_info = info
            mejor_p = p

    return mejor_info, mejor_p

def prob_entrada_optima_binaria(canal: list[list[float]]):
    """"Devuelve P y 1-P OPTIMO\n
    se usa la funcion de capacidad_binaria(canal) para obtener los que den mayor informacion mutua"""
    _ ,p = capacidad_binaria(canal)
    return p, 1-p

def get_probabilidad_error_canal(canal: list[list[float]], prob_entrada: list[float]):
    """
    Calcula la probabilidad de error del canal usando la regla de decision
    de maxima verosimilitud (ML).

    prob_entrada: lista con las probabilidades a priori p(x_i)
    canal: matriz de n filas (entradas) x m columnas (salidas), canal[i][j] = P(y_j | x_i)

    Regla ML: para cada salida y_j se decide la entrada x_i que maximiza
    P(y_j | x_i), sin usar las probabilidades a priori.

    Devuelve (probabilidad_de_error, decision), donde decision[j] es la
    entrada elegida cuando se recibe la salida y_j.
    """
    n, m = len(canal), len(canal[0])

    if len(prob_entrada) != n:
        raise ValueError(
            f"La lista de probabilidades a priori tiene {len(prob_entrada)} valores "
            f"y el canal tiene {n} entradas."
        )
    if abs(sum(prob_entrada) - 1.0) > 1e-9:
        raise ValueError("Las probabilidades a priori deben sumar 1.")

    p_acierto = 0.0
    decision = []
    for j in range(m):
        i_ml = max(range(n), key=lambda i: canal[i][j])
        decision.append(i_ml)
        p_acierto += prob_entrada[i_ml] * canal[i_ml][j]

    return 1 - p_acierto, decision

def decodificar_codigo(codigos: list[str], codigo: str, alfabeto=None):
    """Decodifica `codigo` usando una lista de palabras código.
 
    Funciona con cualquier alfabeto de código (binario, ternario, letras,
    dígitos, etc.): cada elemento de `codigo` es un símbolo del código.
    Las palabras código deben formar un código prefijo (ninguna es prefijo
    de otra) para que la decodificación sea única.
 
    codigos:  lista de palabras código, p. ej. ["11", "01", "00", "10"].
    codigo:   cadena (o secuencia) a decodificar.
    alfabeto: símbolos fuente, en el mismo orden que `codigos`. Si se omite,
              se usan "a", "b", "c", ... en orden.
 
    Ejemplos:
        decodificar_codigo(["11", "01", "00", "10"], "1100111001111001")
        -> "acadbadb"
        decodificar_codigo(["0", "10", "11"], "0101100")  # también binario
        decodificar_codigo(["0", "1", "20", "21"], "2102001")  # ternario
    """
    if alfabeto is None:
        if len(codigos) > 26:
            raise ValueError("Con más de 26 códigos hay que indicar el alfabeto")
        alfabeto = [chr(ord("a") + i) for i in range(len(codigos))]
    if len(alfabeto) != len(codigos):
        raise ValueError("El alfabeto y la lista de códigos deben tener igual longitud")
 
    tabla = dict(zip(codigos, alfabeto))
    mensaje = []
    actual = ""
    for simbolo in codigo:
        actual += simbolo
        if actual in tabla:
            mensaje.append(tabla[actual])
            actual = ""
 
    if actual:
        raise ValueError(f"Quedaron símbolos sin decodificar: {actual!r}")
    return "".join(mensaje)


def codificar_a_string(alfabeto: list[str], codigos: list[str], mensaje: str) -> str:
    """Codifica `mensaje` con la lista de códigos y devuelve el resultado como string.
    alfabeto: símbolos fuente; alfabeto[i] se codifica con codigos[i].
    codigos:  lista de palabras código (por ej. la que devuelve Huffman o Shannon-Fano).
    Ej: codificar_a_string(["A","B","C"], ["0","10","11"], "ABAC") -> "010011"
    """
    if len(alfabeto) != len(codigos):
        raise ValueError("El alfabeto y la lista de códigos deben tener igual longitud")

    tabla = dict(zip(alfabeto, codigos))
    try:
        return "".join(tabla[simbolo] for simbolo in mensaje)
    except KeyError as e:
        raise ValueError(f"El símbolo {e.args[0]!r} no pertenece al alfabeto") from None


def decodificar_desde_string(alfabeto: list[str], codigos: list[str], codificado: str) -> str:
    """Operación inversa de `codificar_a_string`."""
    return decodificar_codigo(codigos, codificado, alfabeto)

####################################################### FORMATEO ##################################################################

# Formateo con punto flotante

"""
print("entropia: {h:.2f}".format(h = entropia))
"""

# Dar tamaño minimo 5 hacer que se centre a izquierda
"""
print(f"{'Entropia a priori:':<25}", [f"{entropia_a_priori:.4f}"])
"""

# Imprimir bytearray
"""
print("Bytearray: ", list(mi_bytearray), f"({len(mi_bytearray)} bytes)")
"""

# Loopear sobre argumentos para funcion 
"""
ejemplos = {
    "1" : (prob_a_priori1, matriz1),
    "31" : (prob_a_priori31, matriz31),
    "32" : (prob_a_priori32, matriz32),
    "6"  : (probabilidades_entrada6, matriz6)
}

for nombre, (prob, matriz) in ejemplos.items():
    entropia_a_priori = get_entropia_lista_prob(prob)
    entropia_a_posteriori = get_entropia_a_posteriori(prob, matriz)
    print(nombre)
    print(f"{'Entropia a priori:':<25}", [f"{entropia_a_priori:.4f}"])
    print(f"{'Entropia a posteriori:':<25}", [f"{p:.4f}" for p in entropia_a_posteriori])"""

# Se puede loopear sobre funciones para no tener que reescribir todos los print para cada funcion especifica 
"""
alfabeto = "abcdef"
P = [0.4, 0.2, 0.2, 0.1, 0.05, 0.05]
mensaje = "abacabadeffedcba"
 
for nombre, funcion in (("Huffman", get_codificacion_huffman), ("Shannon-Fano", get_codificacion_shannon_fano)):
    codigos = funcion(P)
    datos = codificar_a_bytearray(alfabeto, codigos, mensaje)
    recuperado = decodificar_bytearray(alfabeto, codigos, datos)
    print(nombre)
    print("  codigos:   ", codigos)
    print("  bytes:     ", list(datos))
    print("  bits:      ", "".join(format(b, "08b") for b in datos[1:]))
    print("  decodificado:", recuperado, "->", "OK" if recuperado == mensaje else "ERROR")
    print("  tasa de compresion:", round(get_tasa_compresion(mensaje, datos), 4))
"""


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

print("============================== Ejercicio 1 ==============================\n")

mensaje = "GIIHGGGHGIHHIHIIGFHH"

alf, prob = get_listas_alf_prob(mensaje)
entropia = get_entropia_lista_prob(prob)
print(f"Entropia fuente: {entropia:.4f}")

codigo = get_codificacion_huffman(prob)

"""datos = codificar_a_bytearray(alf, codigo, mensaje)
tasa_compresion = get_tasa_compresion_bytearray(mensaje, datos)
print("Tasa compresion: {c:.4f}".format(c = tasa_compresion))"""

codificado = codificar_a_string(alf, codigo, mensaje)
tasa_compresion = get_tasa_compresion_str(mensaje, codificado)
print("Tasa compresion: {c:.4f}".format(c = tasa_compresion))


prob_ext, _ = get_lista_extension_n(alf, prob, 3)
codigo_ext = get_codificacion_huffman(prob_ext)

long_cod = get_longitud_media_codigo(prob, codigo)
rendimiento, redundancia = calcula_rendimiento_redundancia(prob, codigo)
print("\nCodigo extension 1:")
print("Largo medio: {l:.4f}".format(l = long_cod))
print("Rendimiento: {r:.4f}".format(r = rendimiento))
print("Redundancia: {r:.4f}".format(r = redundancia))
print("Primer teorema de Shannon: ", end="")
print("Cumple" if primer_teorema_shanon(prob, codigo, 1) else "No cumple")


long_cod_ext = get_longitud_media_codigo(prob_ext, codigo_ext)
rendimiento_ext, redundancia_ext = calcula_rendimiento_redundancia(prob_ext, codigo_ext)
print("\nCodigo extension 3:")
print("Largo medio: {l:.4f}".format(l = long_cod_ext))
print("Rendimiento: {r:.4f}".format(r = rendimiento_ext))
print("Redundancia: {r:.4f}".format(r = redundancia_ext))
print("Primer teorema de Shannon: ", end="")
print("Cumple" if primer_teorema_shanon(prob_ext, codigo_ext, 3) else "No cumple")

"""
Explicacion como se obtienen resultados:
a) La probabilidad del simbolo se obtiene calculando cuantas veces aparece y dividiendola por la cantidad de simbolos totales
La entropia se halla sumando la informacion de cada simbolo usando las probabilidades halladas anteriormente

b) Para tener un codigo binario optimo se uso el algoritmo de Huffman, que asigna codigos mas cortos a simbolos que aparezcan mas 
frecuentemente y codigos mas largos a los menos frecuentes.

c) La tasa de compresion es la comparacion de tamaño entre el mensaje original y codificado ->  original : codificado
Se obtiene dividiendo el tamaño original del texto con el codificado

e)La long media se calcula teniendo en cuenta el largo del codigo ponderado por la probabilidad de que sea ese codigo
El rendimiento es la entropia dividido la longitud, es que tan bien se aprobechan los bits para la codificacion
La redundacia es 1 - rendimiento y es que tanto se desaprovechan los bits fraccionarios en la codificacion

f) Para la verificacion del teorema de shannon nos fijamos que el largo este entre los bordes de la entropia y entropia + 1

  CORRECCION F:

  Antes que nada, ¿qué dice el Primer Teorema de Shannon? Se rige por la
siguiente fórmula:

H_r(S^n) <= L_n <= H_r(S^n)+1 (1)

Donde:
S es el alfabeto fuente
S^n es la extensión n de S
L_n es la longitud media de Sn
H_r es la entropía base r
Sabiendo
H(S^n)=nH(S) (2)
Reemplazando (2) en (1), obtenemos:
nH_r(S) <= L_n/n <= H_r(S)+1
Dividiendo por n miembro a miembro, obtenemos:
H_r(S) <= L_n/n <= H_r(S)+1/n (3)
El algoritmo funciona de la siguiente manera:
A partir de las palabras código, se genera la extensión S^n llamando a
una función desarrollada en la primera parte de la materia. Esta
función también retorna las probabilidades.
Se calcula L_n a partir de lo calculado en el paso anterior con una
función implementada en la primera parte.
Se calcula H_r(S)
Se retorna true o false en función de si se cumple la inecuación (3)
"""

"""Analisis de los datos:
La entropia de la fuente es de 1.78 binits, es la incertidumbre respecto a la que simbolo de entrada va a recibir, siendo lo maximo posible
una entropia de 2 si la prob de simbolos fuera equiprobable, al estar tan cerca de 2 significa que son relativamente similares la prob
de cada simbolo.
La tasa de compresion nos dice que se comprimio 4 veces el tamaño original del mensaje, por cada 4 bits que ocupaba antes, ahora ocupa 1
El largo medio del codigo normal siendo 2 significa que para cada simbolo se usan 2 bits mientras que en el codigo de extension 3
se usan 5.38, siendo que son codificacioens de a 3 mensajes esto hace que se aprovechen mejor los bits para su codificacion haciendo
que el promedio del mensaje ocupe menos, aunque aumentando la complejidad del codigo

El rendimiento del codigo de extension 3 es mucho menor al base porque al aumentar el N el largo medio se acerca cada vez mas a la
entropia de la fuente, mientras mas larga sea la extension mas optimo va a ser el uso de los bits fraccionales
La redundancia es 1 - rendimiento, al aumentar rendimiento su redundancia baja. El de orden 3 desperdicia mucho menos los bits fraccionales
Que cumpla el primer teorema de shannon significa que es un codigo suficientemente optimo, y ambos lo son
"""

print("\n============================== Ejercicio 2 ==============================\n")

entrada = "10100000101011101001111110011001"
salida = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"

alf, priori = get_listas_alf_prob(entrada)
matriz = get_matriz_canal(entrada, salida)
imprimir_matriz(matriz)

print(f"p{alf[0]}: {priori[0]:.4f}", )
print(f"p{alf[1]}: {priori[1]:.4f}")

sin_ruido = es_canal_sin_ruido(priori, matriz)
determinante = es_canal_determinante(priori, matriz)

print("Clasificacion: ", end="")
if(sin_ruido and determinante):
    print("ambos: sin ruido y determinante")
elif(sin_ruido):
    print("solo sin ruido")
elif(determinante):
    print("solo determinante")
else:
    print("ninguno")

ruido = get_ruido(priori, matriz)
perdida = get_perdida(priori, matriz)
info_mutua = get_informacion_mutua(priori, matriz)

print(f"H(A/B): {ruido:.4f}")
print(f"H(B/A): {perdida:.4f}")
print(f"I(A,B): {info_mutua:.4f}")

canal_reducido, determinante = get_reduccion_suficiente(matriz)
print("Canal reducido:")
imprimir_matriz(canal_reducido)

capacidad, prob_entrada = get_capacidad(canal_reducido)
prob_error, desicion = get_probabilidad_error_canal(canal_reducido, priori)

print(f"Capacidad: {capacidad:.4f}")
print(f"Prob error: {prob_error:.4f}")

datos = bits_a_bytearray(entrada)
if (verificar(datos)):
    print("El mensaje es correcto")
    print(entrada)
else:
    corregido = corregir_bytearray_devolver_string(datos)
    if (corregido == ""):
        print("No se pudo corregir el mensaje")
    else:
        print("Se corrige el mensaje")
        datos_corregidos = get_string_a_bytearray(corregido)
        imprimir_bits_bytearray(datos_corregidos)
        print(corregido)

"""Obtencion de resultados
a) la prob a priori se obtiene contando para cada simbolo, la cantidad de veces que aparece y dividiendola por el largo del mensaje
la matriz del canal se obtiene comparando la entrada con la salida de los correspondientes simbolos de entrada y codigo de salida,
dando asi una probabilidad de que dada tal entrada la probabilidad que se de tal salida

b) Para saber si es sin ruido se ve que para todas las filas haya silo un elemento distinto de 0
    Para saber si es determinante se ve que para cada columna solo haya un elemento distinto de 0

c) equivocacion se calcula haciendo la sumatoria probabilidad mutua de ambos por la informacion de que ocurra tal evento
    la perdida es similar
    la informacion mutua se calcula como la entropia de la entrada menos el ruido

d) Se toma las columnas que son combinacion lineal la una de la otra y se juntan sumando las probabilidades de ambas la mayor cantidad
de veces que se pueda

e) La capacidad es la mayor cantidad de informacion mutua que puede haber en el canal, se hace con una aproximacion, variando 
las probabilidades de las entradas hasta que nos toque la combinacion de mayor info mutua.

f) primero se ve la paridad cruzada, si esta da mal no se corrige
 si va mal la columna o fila de parididad tampoco se corrige
 si se detecta que hay una columna y fila entonces se corrige
"""

"""Interpretacion:
La probabilidad a priori nos dice que es un poco mas probable que aparezca un 1 que un 0

Que no sea ni un canal sin ruido o sin perdida ya nos va diciendo que el canal no es ideal
Luego con el ruido y perdida por si solo no podemos asumir nada, es cuando se agrega la comparacion con la informacion mutua
que podemos sacar conclusiones

Como I(A,B) = H(A) - H(A/B)
nos queda que H(A) = 0.9972 de lo cual el ruido se lleva 0.7158, por lo el canal es muy malo, ni hace falta
hacer lo mismo con la perdida porque ya sabemos que el canal es malo

En el canal reducido se ve que para la entrada de 0 es seguro que va a salir P/Q/R pero el que toque uno de estos codigos no significa
que haya salido de un 0 porque desde el 1, mas de la mitad de las veces va a parar a un P/Q/R, de lo unico que tenemos seguridad es que
si en el codigo salio un S es porque salio de un 1

Que la capacidad sea de 0.2988 binits es el valor maximo de informacion que puede transmitir el canal, esta capacidad es muy baja por
el ruido y perdida

El mensaje fue corregido pq solo tenia un elemento mal
"""
