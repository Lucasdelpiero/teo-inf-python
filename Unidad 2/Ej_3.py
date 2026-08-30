from math import log2

def getEntropiaEquiprob(num):
    return log2(num)

print("Entropia de dado de 6 caras: " + str(getEntropiaEquiprob(6)))

probabilidades = [1/9, 1/6, 1/9, 1/9, 1/6, 1/3]

def getEntropia(prob):
    total = 0
    for elem in prob:
        total += elem * log2(1/elem)
    return total

print("Entropia de nuevo dado: " + str(getEntropia(probabilidades)))