import math
# Crea listas de alfabeto y probabilidades con caracteres de mensajes
def get_listas_alf_prob(mensaje: String):  # ej: "casa"
    listaAlf = [] 
    listaProb = []

    for letra in mensaje:
        if letra not in listaAlf:
            listaAlf.append(letra)

    for letra in listaAlf:
        listaProb.append(mensaje.count(letra)/len(mensaje))

    return [listaAlf, listaProb] # listas = crearListasAlfProb(mensaje)  ;  listaAlf = listas[0] ;    listaProb = listas[1]



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

    return extensiones, probabilidades_ext


mensaje= ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"
listas = get_listas_alf_prob(mensaje)
listaAlfabeto = listas[0]
listaProbabilidad = listas[1]


listas = get_lista_extension_n(listaAlfabeto, listaProbabilidad, 2)
listaExtCod = listas[0]
listaExtProb = listas[1]
mensaje = ":."
pos = listaExtCod.index(mensaje)
prob = listaExtProb[pos]
print("Prob({mensaje}) = {prob}".format(mensaje= mensaje, prob = prob))



#probabilidad = get_prob_extension(mensaje, listaAlfabeto, listaProbabilidad)
#print(probabilidad)