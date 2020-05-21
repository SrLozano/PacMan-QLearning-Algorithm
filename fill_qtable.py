import sys

'''
La funcion parser() toma sys.argv[0] como filas y sys.argv[1] como columnas a preparar en la qtable
teniendo en cuenta los calculos pues hay 6 posibles acciones (columnas)
'''
text_file = open("qtable.txt","w")
salida = ""
max = -1

# if int(sys.argv[1]) < int(sys.argv[2]):
#     max = 4* int(sys.argv[1])
#     print("el maximo es: " + str(sys.argv[1]))
# else:
#     max = 4*int(sys.argv[2])
#     print("el maximo es: " + str(sys.argv[2]))

max = 16

for i in range(0, max):
    for j in range(0, 4):
        salida = salida + "0.0 "
    if i != max-1:
        salida = salida + "\n"

#El 5 es por las acciones posibles, es decir North, South, East, West
# alto = int(sys.argv[1])*int(sys.argv[2])*4
# ancho = 6
# for i in range(0, alto):
#     for j in range(0, ancho):
#         salida = salida + "0.0 "
#     if i != alto-1:
#         salida = salida + "\n"

text_file.write(salida)
text_file.close()

text_file = open("qtable.ini.txt","w")
text_file.write(salida)
text_file.close()