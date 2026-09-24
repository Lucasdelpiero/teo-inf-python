import math

listaProbabilidades = [0.10, 0.50, 0.10, 0.20, 0.05, 0.05]
listaCod1 = ["==", "<", "<=", ">", ">=", "<>"]
listaCod2 = [")", "[]", "]]", "([", "[()]", "([)]"]
listaCod3 = ["/", "*", "-", "*", "++", "+-"]
listaCod4 = [".,", ";", ",,", ":", "...", ",:;"]

listasCod = [listaCod1, listaCod2, listaCod3, listaCod4]


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


n = len(listasCod)

for i in range(n):
    print("Codigo1: ", end="")
    for cod in listasCod[i]:
        print(f"{str(cod):>5}" , end= "") # Hace que se formatee con 5 espacios y se ajuste a la derecha
    print("")
    #print("Codigo2: " + "  ".join(listasCod[i])) # print(" ".join(map(str, miArray))) se usa MAP si son numeros pq join trabaja solo con STRINGS
    print("Entropia: {h:.2f}  | Largo: {l:.2f}\n".format(
        h = getEntropiaPonderadaLargo(listaProbabilidades, listasCod[i]),
        l = getLongitudMediaCodigo(listaProbabilidades, listasCod[i]) 
        ))

# Si es univoco su ENTROPIA <= LONGITUD (media)