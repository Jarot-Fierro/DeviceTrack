Para ejecutar el proyecto sigue los siguientes pasos

1- Crea tu ambiente virtual (venv) e instala las siguiente librerias con pip.

    > python.exe -m pip install --upgrade pip,
    > pip install python-dotenv,
    > pip install psycopg2,
    > pip install Pillow,

2- Crea un archivo .env en la raíz del proyecto para guardar la SECRET KEY de Django.

3- En el .env almacena las variables para la conexión de la base de datos POSTGRESQL.

4- Reemplaza en db.py las variable de las conexiones por los nombres de las variables almacenadas en .env