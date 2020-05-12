import sys

'''
La funcion parser() toma sys.argv[0] como filas y sys.argv[1] como columnas a preparar en la qtable
teniendo en cuenta los calculos pues hay 6 posibles acciones (columnas)
'''
text_file = open("qtable.txt","w")
salida = ""
alto = int(sys.argv[1])*int(sys.argv[2])*4
ancho = 6
for i in range(0, alto):
    for j in range(0, ancho):
        salida = salida + "0.0 "
    if i != alto-1:
        salida = salida + "\n"

text_file.write(salida)
text_file.close()

text_file = open("qtable.ini.txt","w")
text_file.write(salida)
text_file.close()