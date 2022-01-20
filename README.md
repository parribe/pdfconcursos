# pdfconcursos

Se trata de un script hecho en python que tras convertir un pdf con tablas sobre concursos de traslados del Ministerio de Inclusiones, Seguridad Social y Migraciones
crea una BBDD en SQLite e introduce todos los datos de los candidatos.

Previamente se utiliza la herramienta pdftotext de la siguiente forma:
pdftotext.exe -table Listado_admitidos.pdf -nopgbrk


# Descargar: https://www.xpdfreader.com/pdftotext-man.html
# Usamos asi: pdftotext.exe -table Listado_admitidos.pdf -nopgbrk
# Nos genera Listado_admitidos.txt

