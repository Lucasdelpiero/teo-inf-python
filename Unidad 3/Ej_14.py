import math

listaProbabilidades = [0.10, 0.50, 0.10, 0.20, 0.05, 0.05]
listaCod1 = ["==", "<", "<=", ">", ">=", "<>"]
listaCod2 = [")", "[]", "]]", "([", "[()]", "([)]"]
listaCod3 = ["/", "*", "-", "*", "++", "+-"]
listaCod4 = [".,", ";", ",,", ":", "...", ",:;"]

listasCod = [listaCod1, listaCod2, listaCod3, listaCod4]

# Obtiene lista alfabeto de una LISTA
def get_lista_alf_lista(lista): # [ "001", "01", "012"]
    listaAlf = []
    for mensaje in lista:
        for letra in mensaje:
            if letra not in listaAlf:
                listaAlf.append(letra)
    return listaAlf # ["0", "1", "2"]

# Largo PROMEDIO de codigo usando su prob y largo de palabras
def get_longitud_media_codigo(listaProb, listaPalabras):
    total = 0
    n = len(listaPalabras)
    for i in range(n):
        prob = listaProb[i]
        largo = len(listaPalabras[i])
        total += prob * largo
    return total

# Obtiene la entropia considerando PROB y LARGO de cada palabra codigo
def get_entropia_ponderada_largo(listaProb, listaPalabras):
    total = 0
    n = len(listaPalabras)
    alfabeto = get_lista_alf_lista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo

    for i in range(n):
        prob = listaProb[i]
        total += prob * math.log(1/prob, r)
    return total

# Funcion auxiliar para obtener el R (cant de simbolos de alfabeto codigo)
def get_r(listaPalabras):
    alfabeto = get_lista_alf_lista(listaPalabras)
    r = len(alfabeto)
    return r

# Funcion auxiliar 
def get_informacion(r, prob):
    return math.log(1/prob, r)

# Funcion para hacer mas rapido la comprobacion de univoco
def es_univoco(listaPalabras):
    return get_sumatoria_kraft(listaPalabras) <= 1

def get_sumatoria_kraft(listaPalabras):
    alfabeto = get_lista_alf_lista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo
    total = 0
    for palabra in listaPalabras:
        li = len(palabra)       # li = largo de la palabra especifica
        total += r **  (-li)
    return total

# Booleano que devuelve si un codigo es compacto usando su lista de prob y el largo de cada palabra codigo
def es_compacto(listaProb, listaCod):
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

prob1 = [0.13, 0.34, 0.37, 0.12, 0.04]
cods = ["BA", "CCB", "AC", "C", "BAC"]

for i in range(len(listasCod)):
    if (es_compacto(listaProbabilidades, listasCod[i])):
        print(f"{i + 1}: es compacto")
    else:
        print(f"{i + 1}: no es compacto")

