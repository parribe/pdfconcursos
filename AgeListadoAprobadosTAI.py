# Descargar: https://www.xpdfreader.com/pdftotext-man.html
# Usamos asi: pdftotext.exe -table Listado_admitidos.pdf -nopgbrk
# Nos genera Listado_admitidos.txt




import re
import sqlite3
from sqlite3 import Error



def trocearLineaPorDNI(lista): #Funcion usada cuando hay dos DNI por linea
	#print(lista)
	lista2=[]
	lista3=[]
	for x in lista:
	 	t = list(map(lambda s: s.strip(), x))
	 	lista2.append(t)
	#print(lista2)
	for j in lista2:
		if len(j)>3:
	#		print(j[3:])
	#		print(j[:3])
			lista3.append(j[3:])
			lista3.append(j[:3])
		else:
			lista3.append(j)
	#print (lista2)
	return (lista3)


def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE concurso(id INTEGER PRIMARY KEY, 'col0' text, 'col1' text, 'col2' text)")

    con.commit()




f = open("Listado_admitidos.txt", "r")
listado=[]
patron="***" 

#Leemos linea a linea el fichero
for i in f.readlines():
    if patron in i: #Nos quedamos solo con las lineas que tenga ***
    		#print(i.count(patron))
   		listado.append(re.split('  +', i)) #creamos una lista con los elementos que se separan más de 2 espacios entre ellos y lo hacemos por linea
    else:
        
        continue

#if variosDNIporLinea:
nuevo_listado=trocearLineaPorDNI(listado)

con = sql_connection()

sql_table(con) #solo lo llamamos la primera vez ya que crea la tabla y si ya está creada falla

sql_connection()

con.commit()

# # #insertamos en la tabla creada los datos obtenidos
for item in nuevo_listado:
	con.execute("INSERT INTO concurso(col0,col1,col2) VALUES (?,?,?)", item) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
	con.commit()