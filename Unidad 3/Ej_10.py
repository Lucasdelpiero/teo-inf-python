
listaCod1 = ["001", "000", "010", "101", "001", "100"]
listaCod2 = ["110", "100", "101", "001", "110", "010"]
listaCod3 = ["10", "1100", "0101", "1011", "0", "110"]
listaCod4 = ["1101", "10", "1111", "1100", "1110", "0"]
listaCod5 = ["011", "0111", "01", "0", "011111", "01111"]
listaCod6 = ["1110", "0", "110", "1101", "1011", "10"]

listas = [listaCod1, listaCod2, listaCod3, listaCod4, listaCod5, listaCod6]


listaProbabilidades = [0.10, 0.50, 0.10, 0.20, 0.05, 0.05]
listaCod7 = ["==", "<", "<=", ">", ">=", "<>"]
listaCod8 = [")", "[]", "]]", "([", "[()]", "([)]"]
listaCod9 = ["/", "*", "-", "*", "++", "+-"]
listaCod10 = [".,", ";", ",,", ":", "...", ",:;"]

listasConProb = [listaCod7, listaCod8, listaCod9, listaCod10]

# Obtienes listas de alfabeto y probabilidades UN MENSAJE
def getListasAlfProb(mensaje):  # ej: "casa"
    listaAlf = [] 
    listaProb = []

    for letra in mensaje:
        if letra not in listaAlf:
            listaAlf.append(letra)

    for letra in listaAlf:
        listaProb.append(mensaje.count(letra)/len(mensaje))

    return [listaAlf, listaProb] # listas = crearListasAlfProb(mensaje)  ;  listaAlf = listas[0] ;    listaProb = listas[1]

# Obtiene lista alfabeto de una LISTA
def getListaAlfLista(lista): # [ "001", "01", "012"]
    listaAlf = []
    for mensaje in lista:
        for letra in mensaje:
            if letra not in listaAlf:
                listaAlf.append(letra)
    return listaAlf # ["0", "1", "2"]


# Se usa para inecuacion de kraft, si:    SUMATORIA <= 1 es condificion suficiente para la existencia de 
# AL MENOS 1 codigo instantaneo de tal longitud
def getSumatoriaKraft(listaPalabras):
    alfabeto = getListaAlfLista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo
    total = 0
    for palabra in listaPalabras:
        li = len(palabra)       # li = largo de la palabra especifica
        total += r **  (-li)
    return total

# Sumatoria Kraft pero con PROBABILIDADES en cada codigo
def getSumatoriaKraftPonderada(listaProb, listaPalabras): #### NO SE USA
    alfabeto = getListaAlfLista(listaPalabras) 
    r = len(alfabeto) # r = cant de alfabeto codigo
    total = 0
    for i in range(listaPalabras):
        li = len(listaPalabras[i])       # li = largo de la palabra especifica
        prob = listaProb[i]                 
        total +=  prob *  r **  (-li)
    return total

for lista in listas:
    print(getSumatoriaKraft(lista))

for lista in listasConProb:
    print(getSumatoriaKraft(lista))

# Donde la inecuacion de kraft de <= 1 significa que existe un codigo INSTANTANEO
# Por inecuacion MacMillan si es > 1 entonces no se puede definir un codigo UNIVOCO ni INSTANTANEO