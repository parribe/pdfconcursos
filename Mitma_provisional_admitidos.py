# Descargar: https://www.xpdfreader.com/pdftotext-man.html
# Usamos asi: pdftotext.exe -table Listado_admitidos.pdf -nopgbrk
# Nos genera Listado_admitidos.txt

## Hay que arreglar previamente el documento de mitma para que los DNI que tengan más de 1 peticiones, el DNI se posicione en la primera de las lineas y no en el centro.


import re
import sqlite3
from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    #cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")

    cursorObj.execute("CREATE TABLE concurso(id INTEGER PRIMARY KEY, dni text, orden text, anexo text)")

    con.commit()

con = sql_connection()

sql_table(con) #solo lo llamamos la primera vez ya que crea la tabla y si ya está creada falla

sql_connection()

con.commit()


f = open("Listado_admitidos.txt", "r")
listado=[]
nuevo_listado=[]

patron=["D.N.I.","Preferencia"] #Limpiamos el texto intermedio que hay en el documento

#Leemos linea a linea el fichero
for i in f.readlines():
    if patron[0] in i or patron[1] in i: #Saltamos la líneas que contienen el texto de cabecera de las columnas de documento
        continue
    else:
        
        listado.append(re.split('  +', i)) #creamos una lista con los elementos que se separan más de 2 espacios entre ellos y lo hacemos por linea

#ELIMINAMOS LOS SALTOS DE LINEA
for x in listado:
	t = list(map(lambda s: s.strip(), x))
	[s for s in listado if "" in s]
	nuevo_listado.append(t)

sinElementosVacios=[]

#Elimina los espacion de los registro que tienen más de 3 elemento(los que valer)
for cosa in nuevo_listado:
	borraEspacios=[item for item in cosa if item]
	if len(cosa)<3:
		pass
	else:
		sinElementosVacios.append(borraEspacios)

matched_indexes=[]
contador=0
for i in sinElementosVacios:
	#print (i)
	if len(i)==3:
		matched_indexes.append(contador)
		contador+=1
	else:
		contador+=1
matched_indexes.append(len(sinElementosVacios)) #añadimos como ultimo elemento el ultimo registro

auxInicial=0
auxFinal=1
listaAgrupadaPorIdInstancia=[]

for i in range (len(matched_indexes)-1): #ponemos -1 pq el ultimo elemento no tiene otro más con el que hacer sublistado
	agrupa=(sinElementosVacios[matched_indexes[auxInicial]:matched_indexes[auxFinal]])
	#print (sinElementosVacios[matched_indexes[auxInicial]:matched_indexes[auxFinal]])
	listaAgrupadaPorIdInstancia.append(agrupa)
	auxInicial+=1
	auxFinal+=1

#print (listaAgrupadaPorIdInstancia)
for i in listaAgrupadaPorIdInstancia:
	#print (i)
	# print (len(i))
	if len(i)>1:
		id_instancia=i[0][0] #Guardamos el valor del primer elemento de cada lista cuya longitud sea mayor a 1
		# dni=i[0][1]
		# apellidos=i[0][2]
		# nombre=i[0][3]
		for x in range(len(i)): #Para cada elemento de la lista excluyendo al elemento 0, insertamos el dni en cada 1 de los campos que no lo llevan
			if x==0:
				pass
			else:
				# i[x].insert(0,nombre)
				# i[x].insert(0,apellidos)
				# i[x].insert(0,dni)
				i[x].insert(0,id_instancia)

#print (listaAgrupadaPorIdInstancia)

# #insertamos en la tabla creada los datos obtenidos
for item in listaAgrupadaPorIdInstancia:
	for i in item:
		print (i)
		con.execute("INSERT INTO concurso(dni,orden,anexo) VALUES (?,?,?)", i) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
		con.commit()