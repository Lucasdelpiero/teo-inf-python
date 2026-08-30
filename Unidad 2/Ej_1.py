from math import log2

prob = [0.5, 0.25, 0.125, 0.125]
#prob = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
bits = []


#Devuelve una lista con la cantidad de bits necesarios para representar cada simbolo
def genListaBitsNecesarios(distribucion):
    nuevaLista = []
    for elem in distribucion:
        nuevaLista.append(log2(1/elem )) 
    return nuevaLista


bits = genListaBitsNecesarios(prob)

print(bits)

def getEntropia(lista):
    total = 0

    for elem in lista:
        total += elem * log2(1/elem)

    return total

print("Entropia total: " + str(getEntropia(prob)))