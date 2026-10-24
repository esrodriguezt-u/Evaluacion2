# listar_libros.py
# Lista la totalidad de los libros de la biblioteca recorriendo todas las páginas de la API.
import time
import requests

APIHOST = "http://library.demo.local"

libros = {}
pagina = 0
while True:
    r = requests.get(f"{APIHOST}/api/v1/books",
                     params={"includeISBN": "true", "sortBy": "id", "page": pagina})
    if r.status_code == 429:          # límite de peticiones de la API: esperar y reintentar
        time.sleep(2)
        continue
    datos = r.json()
    if not datos:
        break
    for b in datos:
        libros[b["id"]] = b
    if len(datos) < 10:               # última página
        break
    pagina += 1
    time.sleep(1)

print(f"Código de estado: {r.status_code}  |  Páginas leídas: {pagina + 1}  |  Total de libros: {len(libros)}\n")
for b in sorted(libros.values(), key=lambda x: x["id"]):
    print(f"{b['id']:>4} | {b['title'][:45]:<45} | {b['author'][:25]:<25} | {b.get('isbn', '')}")
