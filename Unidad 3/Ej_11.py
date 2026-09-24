import math

listaProb = [1/9, 1/3, 1/3, 1/9, 1/9]
x1 = ["BA", "CCB", "AC", "C", "BAC"]

# Obtiene lista alfabeto de una LISTA
def getListaAlfLista(lista): # [ "001", "01", "012"]
    listaAlf = []
    for mensaje in lista:
        for letra in mensaje:
            if letra not in listaAlf:
                listaAlf.append(letra)
    return listaAlf # ["0", "1", "2"]

# Obtiene la entropia considerando PROB y LARGO de cada palabra codigo
def getEntropiaPonderadaLargo(listaProb, listaPalabras):
    total = 0
    n = len(listaPalabras)
    alfabeto = getListaAlfLista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo

    for i in range(n):
        prob = listaProb[i]
        total += prob * math.log(1/prob, r)
    return total

# Largo PROMEDIO de codigo usando su prob y largo de palabras
def getLongitudMediaCodigo(listaProb, listaPalabras):
    total = 0
    n = len(listaPalabras)
    for i in range(n):
        prob = listaProb[i]
        largo = len(listaPalabras[i])
        total += prob * largo
    return total

    

print(getEntropiaPonderadaLargo(listaProb, x1))
print(getLongitudMediaCodigo(listaProb, x1))