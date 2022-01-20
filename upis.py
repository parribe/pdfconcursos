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

    cursorObj.execute("CREATE TABLE concurso(id INTEGER PRIMARY KEY, dni text, apellidos text, nombre text, orden_pref integer, orden_conv integer)")

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
	nuevo_listado.append(t)

#CREAMOS UNA LISTA CON LOS ELEMENTOS EN DONDE SE ENCUENTRAN LOS DNI. La variable contador tomará el valor de las posiciones de la lista.
pattern = '¿¿¿'

matched_indexes=[]
contador=0

for cosa in nuevo_listado:
	for cosita in cosa:
		cosita=cosita.replace("*", "¿")
		if re.match(pattern,cosita):
			matched_indexes.append(contador) #nos quedamos con la posicion en donde haya dnis
	contador+=1

#CREAMOS UNA NUEVA LISTA CON LOS ELEMENTOS QUE VAN DESDE UN DNI AL SIGUIENTE. i toma valores entre de 0 a 297 y tupinamba toma los valores de los indices donde hay dnis marcado en la variable matched_indexes
listadoPrimerArreglo=[]

tupinanba=1
for i in range (len(matched_indexes)-1):
	arreglo=(nuevo_listado[(matched_indexes[i]):(matched_indexes[tupinanba])]) #cogemos de nuevo_listado los elemento que van desde el elemento matched_indexes[i] hasta matched_indexes[contador]
	listadoPrimerArreglo.append(arreglo)
	tupinanba+=1


#Añadimos al último concursante ya que no es añadido porque no delimita con ??? con el siguiente concursante al ser el último
ultimoConcursante=nuevo_listado[(matched_indexes[-1]):contador] #Usamos -1 para seleccionar el ultimo elemento de la lista y contador del bucle for anterior que tiene el total de los registros.
listadoPrimerArreglo.append(ultimoConcursante)

#ELIMINAMOS EL PRIMER ELEMENTO DE DE LA SEGUNDA y SIGUIENTES LISTAS DE CADA SOLICITUD POR ESTAR VACIO, DESPUES AÑADIMOS NOMBRE, APELLIDOS Y DNI A CADA UNA DE LAS SOLICITUDES QUE NO LO LLEVAN
for i in listadoPrimerArreglo: #Recorremos los elementos del listado ## ejemplo [['¿¿¿1029¿¿', 'ABAD GARCIA', 'FERNANDO', '1', '172'], ['', '2', '122'], ['', '3', '173']]
	largo=len(i) # calculamos el número de elementos de la lista # en nuestro ejemplo es 3
	if largo>1: # si tiene más de un elemento lo pasamos al bucle for
		for z in range (largo): # recorremos en nuesto ejemplo. para la primera vuelta z vale 0 por lo que al entrar en el if salta a la siguiente iteración del for.     #en la segunda vuelta z vale 1, entra en el else y borra el primer elemento del segundo elemento del array. 
			if z==0:            #en la tercera(y ultima vuelta) vuelta z vale 2 y borra el primer elemento del tercer elemento del array
				continue
			else:
				del i[z][0]
	dni_aux=i[0][0] #variable que contiene el primer elemento de la primera lista, es decir, el DNI '¿¿¿1029¿¿'
	apell_aux=i[0][1] #variable que contiene el segundo elemento de la primera lista, es decir, los APELLIDOS 'ABAD GARCIA'
	nombre_aux=i[0][2] # varialble que contiene el tercer elemento de la primera lista, es decir, el NOMBRE 'FERNANDO'
	for z in range (largo): #de nuevo los valores de z en este caso de ejemplo irán del 0 al 2 (pq largo=3).
		if z==0:            #si vale z vale 0 saltamos a la siguiente iteración del for pq o es una lista vacia o una lista completa (la lista vacia se llenará con dni, apellidos y nombre pero se filtrará antes de meterse en bbdd)
			continue
		else: # para z = 1 y z = 2 se insertan uno a uno como primer elemento de la lista el nombre, luego los apellidos y luego el dni
			i[z].insert(0,nombre_aux) 
			i[z].insert(0,apell_aux)
			i[z].insert(0,dni_aux)

#Resultando esto: [['¿¿¿1029¿¿', 'ABAD GARCIA', 'FERNANDO', '1', '172'], ['¿¿¿1029¿¿', 'ABAD GARCIA', 'FERNANDO', '2', '122'], ['¿¿¿1029¿¿', 'ABAD GARCIA', 'FERNANDO', '3', '173']]

#insertamos en la tabla creada los datos obtenidos
for item in listadoPrimerArreglo:
	for i in item:
		if len(i)<5 : #Debido a que hay elementos vacios se han llenado con nombre,apellidos y dni pero no hay mas datos. Lo filtramos y solo insertamos en bbdd los datos que valen
			continue
		elif len(i)==5:
			con.execute("INSERT INTO concurso(dni,apellidos,nombre,orden_pref,orden_conv) VALUES (?,?,?,?,?)", i) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
			con.commit()
			print (i)
		elif len(i)==6: #Por problemas al pasar de pdf a texto a veces hay más espacios entre nombre y apellidos y lo controlamos uniendo campos antes de insertar en bbdd
			i=[i[0],i[1]+i[2],i[3],i[4],i[5]]
			con.execute("INSERT INTO concurso(dni,apellidos,nombre,orden_pref,orden_conv) VALUES (?,?,?,?,?)", i) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
			con.commit()
			print (i)
		elif len(i)==7: #Por problemas al pasar de pdf a texto a veces hay más espacios entre nombre y apellidos y lo controlamos uniendo campos antes de insertar en bbdd
			i=[i[0],i[1]+i[2]+i[3],i[4],i[5],i[6]]
			con.execute("INSERT INTO concurso(dni,apellidos,nombre,orden_pref,orden_conv) VALUES (?,?,?,?,?)", i) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
			con.commit()
			print (i)
		elif len(i)==8: #Por problemas al pasar de pdf a texto a veces hay más espacios entre nombre y apellidos y lo controlamos uniendo campos antes de insertar en bbdd
			i=[i[0],i[1]+i[2]+i[3]+i[4],i[5],i[6],i[7]]
			con.execute("INSERT INTO concurso(dni,apellidos,nombre,orden_pref,orden_conv) VALUES (?,?,?,?,?)", i) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
			con.commit()
			print(i)
		elif len(i)==9: #Por problemas al pasar de pdf a texto a veces hay más espacios entre nombre y apellidos y lo controlamos uniendo campos antes de insertar en bbdd
			i=[i[0],i[1]+i[2]+i[3]+i[4]+i[5],i[6],i[7],i[8]]
			con.execute("INSERT INTO concurso(dni,apellidos,nombre,orden_pref,orden_conv) VALUES (?,?,?,?,?)", i) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
			con.commit()
			print(i)
		else:
			print("Hay alguno de más no controlado")