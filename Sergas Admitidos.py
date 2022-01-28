# Descargar: https://www.xpdfreader.com/pdftotext-man.html
# Usamos asi: pdftotext.exe -table Listado_admitidos.pdf -nopgbrk
# Nos genera Listado_admitidos.txt




import re
import sqlite3
from sqlite3 import Error



def trocearLineaPorDNI(lista): #Funcion usada cuando hay dos DNI por linea
	lista2=[]
	for x in lista:
		t = list(map(lambda s: s.strip(), x))
		lista2.append(t)
	listatroceada=[]
	for y in lista2:
		contadoraux=0
		ayuda=[]
		for i in y:
			patron="***"
			if patron in i:
				ayuda.append(contadoraux) 
				contadoraux+=1
			else:
				contadoraux+=1
		if len(ayuda)>1:
			cadenaBuena=(y[(ayuda[0]):(ayuda[1])])
			listatroceada.append(cadenaBuena)

		else:
			listatroceada.append(y)
	return (listatroceada)


def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE concurso(id INTEGER PRIMARY KEY, 'col0' text, 'col1' text, 'col2' text, 'col3' text, 'col4' text, 'col5' text)")

    con.commit()




f = open("Listado_admitidos.txt", "r")
listado=[]
patron="***" 
variosDNIporLinea=False

#Leemos linea a linea el fichero
for i in f.readlines():
    if patron in i: #Nos quedamos solo con las lineas que tenga ***
    		#print(i.count(patron))
   		listado.append(re.split('  +', i)) #creamos una lista con los elementos que se separan más de 2 espacios entre ellos y lo hacemos por linea
    else:
        
        continue

#Comprobamos que en el primer elemento y previsiblemente en el resto hay dos DNI por linea
str_match = [s for s in listado[0] if "***" in s]
if len(str_match)>1:
	variosDNIporLinea=True

print (variosDNIporLinea)

#if variosDNIporLinea:
nuevo_listado=trocearLineaPorDNI(listado)

# tabla=[]
# tabla2=[]
# tabla3=[]
# for i in range(len(nuevo_listado[0])+1):
# 	tabla3.append('\'col'+str(i)+'\''+' text')
# 	tabla2.append("?")
# 	tabla.append("col"+str(i))

# columnas=(",".join(tabla))
# valores=(",".join(tabla2))
# creartabla=(",".join(tabla3))
# print (creartabla)

for i in nuevo_listado:
	if len(i)<6:
		i.append("null")
con = sql_connection()

sql_table(con) #solo lo llamamos la primera vez ya que crea la tabla y si ya está creada falla

sql_connection()

con.commit()



#insertamos en la tabla creada los datos obtenidos
for item in nuevo_listado:
	con.execute("INSERT INTO concurso(col0,col1,col2,col3,col4,col5) VALUES (?,?,?,?,?,?)", item) #se ponen tantas ? como elementos reales hay en el listado, no se cuenta con el id que es autoincrementado
	con.commit()
	print (item)