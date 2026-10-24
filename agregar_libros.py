# agregar_libros.py
# Agrega 50 libros aleatorios a la API de la Biblioteca
import json
import random
import requests
from faker import Faker

APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"
CANTIDAD = 50
ID_INICIAL = 8          # los ids 5, 6 y 7 ya se usaron en Postman

fake = Faker("es_ES")


def obtener_token():
    r = requests.post(f"{APIHOST}/api/v1/loginViaBasic", auth=(LOGIN, PASSWORD))
    if r.status_code == 200:
        return r.json()["token"]
    raise Exception(f"Error {r.status_code} al autenticar: {r.text}")


def agregar_libro(libro, token):
    r = requests.post(
        f"{APIHOST}/api/v1/books",
        headers={"Content-type": "application/json", "X-API-Key": token},
        data=json.dumps(libro),
    )
    if r.status_code == 200:
        print(f"[200 OK] Libro agregado: {libro['id']} - {libro['title']}")
    else:
        print(f"[{r.status_code}] Error al agregar {libro['id']}: {r.text}")


def listar_libros():
    r = requests.get(f"{APIHOST}/api/v1/books", params={"includeISBN": "true", "sortBy": "id"})
    libros = r.json()
    print(f"\nCódigo de estado: {r.status_code}  |  Total de libros: {len(libros)}\n")
    for b in libros:
        print(f"{b['id']:>4} | {b['title'][:45]:<45} | {b['author'][:25]:<25} | {b.get('isbn', '')}")


if __name__ == "__main__":
    token = obtener_token()
    print("Token obtenido:", token)
    for i in range(ID_INICIAL, ID_INICIAL + CANTIDAD):
        libro = {
            "id": i,
            "title": fake.catch_phrase(),
            "author": fake.name(),
            "isbn": fake.isbn13() if random.random() < 0.5 else str(random.randint(10**12, 10**13 - 1)),
        }
        agregar_libro(libro, token)
    listar_libros()
