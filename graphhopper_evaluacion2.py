# graphhopper_evaluacion2.py
# Calculadora de rutas con la API de GraphHopper - versión en español
import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"
key = "PEGA_AQUI_TU_TOKEN_DE_GRAPHHOPPER"

SALIR = ("s", "salir")


def geocodificar(ubicacion, key):
    while ubicacion == "":
        ubicacion = input("Ingrese nuevamente la ubicación: ")
    url = geocode_url + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": key, "locale": "es"})
    respuesta = requests.get(url)
    json_data = respuesta.json()
    json_status = respuesta.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        nombre = hit["name"]
        tipo = hit.get("osm_value", "")
        pais = hit.get("country", "")
        region = hit.get("state", "")

        if region and pais:
            nueva_ubic = f"{nombre}, {region}, {pais}"
        elif pais:
            nueva_ubic = f"{nombre}, {pais}"
        else:
            nueva_ubic = nombre

        print(f"URL de la API de geocodificación para {nueva_ubic} (Tipo de ubicación: {tipo})\n{url}")
    else:
        lat = "null"
        lng = "null"
        nueva_ubic = ubicacion
        if json_status != 200:
            print(f"Estado de la API de geocodificación: {json_status}\nMensaje de error: {json_data.get('message', '')}")
    return json_status, lat, lng, nueva_ubic


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en GraphHopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    perfiles = ["car", "bike", "foot"]
    vehiculo = input("Ingrese un perfil de vehículo de la lista (o 's' / 'salir' para terminar): ").strip().lower()
    if vehiculo in SALIR:
        break
    elif vehiculo not in perfiles:
        vehiculo = "car"
        print("No se ingresó un perfil válido. Se usará el perfil 'car' (auto).")

    origen_txt = input("Ubicación de origen: ").strip()
    if origen_txt.lower() in SALIR:
        break
    origen = geocodificar(origen_txt, key)

    destino_txt = input("Destino: ").strip()
    if destino_txt.lower() in SALIR:
        break
    destino = geocodificar(destino_txt, key)

    print("=================================================")
    if origen[0] == 200 and destino[0] == 200:
        op = "&point=" + str(origen[1]) + "%2C" + str(origen[2])
        dp = "&point=" + str(destino[1]) + "%2C" + str(destino[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "profile": vehiculo, "locale": "es"}) + op + dp
        respuesta = requests.get(paths_url)
        paths_status = respuesta.status_code
        paths_data = respuesta.json()

        print(f"Estado de la API de rutas: {paths_status}\nURL de la API de rutas:\n{paths_url}")
        print("=================================================")
        print(f"Indicaciones desde {origen[3]} hasta {destino[3]} en {vehiculo}")
        print("=================================================")

        if paths_status == 200:
            km = paths_data["paths"][0]["distance"] / 1000
            millas = km / 1.61
            seg = int(paths_data["paths"][0]["time"] / 1000 % 60)
            mins = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hrs = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print(f"Distancia recorrida: {millas:.2f} millas / {km:.2f} km")
            print(f"Duración del viaje: {hrs:02d}:{mins:02d}:{seg:02d}")
            print("=================================================")
            print("Narrativa del viaje:")
            for paso in paths_data["paths"][0]["instructions"]:
                texto = paso["text"]
                dist = paso["distance"]
                print(f"{texto} ( {dist / 1000:.2f} km / {dist / 1000 / 1.61:.2f} millas )")
            print("=================================================")
        else:
            print(f"Mensaje de error: {paths_data.get('message', '')}")
            print("*************************************************")
    else:
        print("No se pudo obtener la ubicación de origen o destino.")

print("Programa finalizado. ¡Hasta pronto!")
