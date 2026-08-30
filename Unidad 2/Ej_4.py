from math import log2

casos = [0.25, 0.75, 0.5, 1, 0]


entropia = 0
print("Entropia para cada caso:")
for w in casos:
    comp = 1 - w
    if (w !=1 and w !=0):
        entropia = (w)*log2(1/w) + (comp)*log2(1/comp)
    else:
        entropia = 0
    print("Para w: " + str(w) + " = " + str(entropia))