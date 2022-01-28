# Descargar: https://www.xpdfreader.com/pdftotext-man.html
# Usamos asi: pdftotext.exe -table Listado_admitidos.pdf -nopgbrk
# Nos genera Listado_admitidos.txt




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

    cursorObj.execute("CREATE TABLE concurso(id INTEGER PRIMARY KEY, id_inst text, dni text, apellidos text, nombre text, orden integer, puesto integer, id_cuerpo integer, causa_exclu text)")

    con.commit()

con = sql_connection()

sql_table(con) #solo lo llamamos la primera vez ya que crea la tabla y si ya está creada falla

sql_connection()

con.commit()


f = open("Listado_admitidos.txt", "r")
listado=[]
nuevo_listado=[]

patron=["ID","INSTANCIA"] #Limpiamos el texto intermedio que hay en el documento

#Leemos linea a linea el fichero
for i in f.readlines():
    if patron[0] in i or patron[1] in i: #Saltamos la líneas que contienen el texto de cabecera de las columnas de documento
        continue
    else:
        
        listado.append(re.split('  +', i)) #creamos una lista con los elementos que se separan más de 2 espacios entre ellos y lo hacemos por linea

#ELIMINAMOS LOS SALTOS DE LINEA
for x in listado:
	t = list(map(lambda s: s.strip(), x))
	nuevo_listado.append(t)

#CREAMOS UNA LISTA CON LOS ELEMENTOS EN DONDE SE ENCUENTRAN LOS DNI. La variable contador tomará el valor de las posiciones de la lista.
pattern = '^\d'

matched_indexes=[]
contador=0

sinElementosVacios=[]

#Elimina los espacion de los registro que tienen más de 3 elemento(los que valer)
for cosa in nuevo_listado:
	borraEspacios=[item for item in cosa if item]
	if len(cosa)<3:
		pass
	else:
		sinElementosVacios.append(borraEspacios)

#print (sinElementosVacios)
#Hacemos una lista del lugar donde se encuentran los nombres de los participantes y su primera peticion de puesto
for i in sinElementosVacios:
	if len(i)==8:
		matched_indexes.append(contador)
		contador+=1
	else:
		contador+=1
#print (matched_indexes)

#print (sinElementosVacios[matched_indexes[0]:matched_indexes[2-1]])

#Crea una lista separada con todas las candidaturas de cada participante
auxInicial=0
auxFinal=1
listaAgrupadaPorIdInstancia=[]
for i in range (len(matched_indexes)-1):
	agrupa=(sinElementosVacios[matched_indexes[auxInicial]:matched_indexes[auxFinal]])
	#print (sinElementosVacios[matched_indexes[auxInicial]:matched_indexes[auxFinal]])
	listaAgrupadaPorIdInstancia.append(agrupa)
	auxInicial+=1
	auxFinal+=1

#Añadimos al último concursante por ser el ultimo y no tener otra lista de 8 elementos final con la que delimitar
#print (sinElementosVacios[matched_indexes[-1]:(len(sinElementosVacios))])
listaAgrupadaPorIdInstancia.append((sinElementosVacios[matched_indexes[-1]:(len(sinElementosVacios))]))

#print(listaAgrupadaPorIdInstancia)

#print (listaAgrupadaPorIdInstancia[1][0]) #['13', '0074', 'AGUDO GORDILLO', 'JOSE MARIA', '68', '1756977', '1135', 'R003']

#print (listaAgrupadaPorIdInstancia[1])#[['13', '0074', 'AGUDO GORDILLO', 'JOSE MARIA', '68', '1756977', '1135', 'R003'], ['69', '3196762', '1135', 'R003'], ['70', '3424999', '1135', 'R003'], ['139', '1972406', '1135', 'R003'], ['140', '2409656', '1135', 'R003']]
#AÑADIMOS LOS CAMPOS NECESARIOS A CADA UNA DE LAS LISTAS HASTA QUE TODAS TENGAN 8 ELEMENTOS, A EXCEPCIÓN DE LISTAS DONDE SOLO HAY UN CONCURSANTE
for i in listaAgrupadaPorIdInstancia:
	# print (i)
	# print (len(i))
	if len(i)>1:
		id_instancia=i[0][0]
		dni=i[0][1]
		apellidos=i[0][2]
		nombre=i[0][3]
		for x in range(len(i)):
			if x==0:
				pass
			else:
				i[x].insert(0,nombre)
				i[x].insert(0,apellidos)
				i[x].insert(0,dni)
				i[x].insert(0,id_instancia)
	#print (i)
	#print (len(i))

#print (listaAgrupadaPorIdInstancia)

 #insertamos en la tabla creada los datos obtenidos

for item in listaAgrupadaPorIdInstancia:
	if len(item)>1:
		for i in item:
			#print (i)
			con.execute("INSERT INTO concurso(id_inst,dni,apellidos,nombre,orden,puesto,id_cuerpo,causa_exclu) VALUES (?,?,?,?,?,?,?,?)", i)
			con.commit()
	elif len(item)==1:
		for i in item:
			#print (i)
			con.execute("INSERT INTO concurso(id_inst,dni,apellidos,nombre,orden,puesto,id_cuerpo,causa_exclu) VALUES (?,?,?,?,?,?,?,?)", i)
			con.commit()
	else:
		print("Tiene elementos no controlados")

 	# con.execute("INSERT INTO concurso(id_inst,dni,apellidos,nombre,orden,puesto,id_cuerpo,causa_exclu) VALUES (?,?,?,?,?,?,?,?)", item)
 	# con.commit()