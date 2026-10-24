# Evaluacion2 – CUY6142

Script en Python que consume la API de **GraphHopper** para calcular rutas entre dos ubicaciones (por ejemplo, hasta la Biblioteca Nacional). Muestra la distancia y la duración del viaje con un máximo de dos decimales y la narrativa paso a paso en español.

También incluye los scripts usados para poblar y listar el catálogo de la API de la biblioteca en la VM DEVASC.

## Requisitos
- Python 3
- Librería `requests` (`pip3 install requests`)
- Un token (API key) de GraphHopper: https://graphhopper.com

## Ejecución
1. Clonar el repositorio y entrar a la carpeta `Evaluacion2`.
2. Editar `graphhopper_evaluacion2.py` y reemplazar `PEGA_AQUI_TU_TOKEN_DE_GRAPHHOPPER` por tu token.
3. Ejecutar: `python3 graphhopper_evaluacion2.py`
4. Ingresar el perfil de vehículo (`car`, `bike` o `foot`), el origen y el destino.
5. Para salir, escribir `s` o `salir` en cualquier pregunta.
