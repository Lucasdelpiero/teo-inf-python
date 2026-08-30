from math import log2
import random

alfabeto = []
probabilidades = []
mensaje = ["c","a","s","a"]

# Crea alfabeto con caracteres de mensajes
def creaListas(mensaje):
    alf = []
    prob = []

    for elem in mensaje:
        if elem not in alf:
            alf.append(elem)

    for elem in alf:
        prob.append(mensaje.count(elem)/len(mensaje))

    return [alf, prob]


listas = creaListas(mensaje)
alfabeto = listas[0]
probabilidades = listas[1]

print(alfabeto)
print(probabilidades)

#-------------------------------------------------

# Segun el numero ingresado devuelve la pos del elemento segun su probabilidad acumulada
def getNum(n, acum):
    for i in range(len(acum)):
        if n < acum[i]:
            return i



# Genera palabra de largo N  
def genPalabra(n, alf, prob):
    palabra = ""
    acum = []
    # Genera lista con probabilidad acumulada de alfabeto
    for i in range(len(alf)):
        if i == 0: 
            acum.append(prob[i])
        else:
            acum.append(prob[i] + acum[i - 1])
    print(acum)

    # genera la palabra segun un numero aleatorio y lista acumulada
    for i in range(n):
        palabra += alf[getNum(random.random(), acum)]

    return palabra

            
palabra = genPalabra(4, alfabeto, probabilidades)

print(palabra)
    