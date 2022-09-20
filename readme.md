# Proyecto Final de Titulación

## UTEC - Licenciatura en tecnologías de la información

### Raccoon Reco

El presente trabajo expone el plan para la implementación de un sistema de reconocimiento facial, que dará una solución moderna y dinámica para el control y recolección de datos de acceso de clientes o usuarios finales a distintos tipos de establecimientos.

Este repo corresponde al backend de nuestra solución, separada en 3 repos: backend, frontend y docker, donde cada uno de ellos almacena las diferentes soluciones en cada uno de estos planos de nuestra arquitectura.

[repo backend](https://github.com/michelaycag/Raccoonreco)
[repo frontend](https://github.com/AriasFacundo/Raccoonreco-frontend)
[repo docker](https://github.com/chuelmo-utec/Raccoonreco-docker)

## Pasos para tener la solución funcionando

Prerequisitos: Tener docker instalado en el sistema host.

- Crear una carpeta en el disco donde se puedan clonar los 3 repositorios, es importante hacerlo de esta manera porque el repo docker usa scripts con rutas relativas tanto al repo de backend como al repo de frontend.
- Clonar los 3 repos dentro de la carpeta creada
- Abrir una terminal en la carpeta del repo de backend y crear la carpeta pg-data que será donde se persistan los datos.
- Moverse a la carpeta del repo de docker
- Ejecutar `docker-compose up -d`
- Ahora moverse nuevamente a la carpeta del repo de backend y ejecutar el siguiente comando: `python3 createSQLfunctions.py` (para este paso es necesario tener instalado python 3.10 en el host)
- Abrir en el navegador: http://localhost:9393 para verificar que el backend está levantado
- Abrir http://localhost:8080/insertUser.html para ingresar fotos.
- Abrir http://localhost:8080/index.html para realizar el reconocimiento facial.
