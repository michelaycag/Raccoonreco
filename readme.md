Paso a paso
0 - clonar repositorio
1- Instalar docker
2 - Abrir docker
3 - abrir code y en la terminal hay que poner docker-compose up -d en la root del proyecto
4- instalar con pip install psycopg2 es requisito para que corra main.py
5- correr el archivo createSQLFunctions en la terminal para crear la tabla necesaria en el postgres llamada face_table

almacenar caras en carpeta llamada LFW, (puede cambiarse en archivo face embeddings)

ejecutar face embeddings y esta se encarga de codificar y subir a base de datos

---------------------------------------------
(A chuelmo le anduvo directo sin instalar dlib y cmake, hay que evaluar eso)

pip install opencv-python
pip install psycopg2

https://stackoverflow.com/questions/41912372/dlib-installation-on-windows-10

(installamos cmake, reiniciamos e instalamos dlib)

https://bcsiriuschen.github.io/CARC/
