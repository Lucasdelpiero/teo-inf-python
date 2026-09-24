import random
#palabras = ["011", "110", "10", "1101", "011", "1110"]
#palabras = ["A", "BD", "CE", "DS", "E", "FRMI"]
palabras = ["BA", "CCB", "AC", "C", "BAC"]

# a
def generaCadena(palabras):
    palabra = ""
    for i in range(0, 8):
        palabra += palabras[random.randint(0,len(palabras) - 1)]
    return palabra

cadena = generaCadena(palabras)
print(cadena)


# Devuelve una lista con el largo de palabras
def getLongitudPalabras(palabras):
    lista = [len(palabra) for palabra in palabras]
    return lista


longitudes = getLongitudPalabras(palabras) 
print(longitudes)

# Se usa para inecuacion de kraft, si:    SUMATORIA <= 1 es condificion suficiente para la existencia de 
# AL MENOS 1 codigo instantaneo de tal  longitud
def getSumatoriaKraft(palabras):
    r = len(palabras) # r = cant de palabras codigo
    longitudes = getLongitudPalabras(palabras)
    total = 0
    for li in longitudes:
        total += r **  (-li)
    return total

print(getSumatoriaKraft(palabras))
