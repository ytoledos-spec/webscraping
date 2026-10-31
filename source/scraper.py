import csv
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

anios = range(2000, 2026)
#anios = [2021]

headers = {
    "User-Agent": "PracticaCineBot/1.0 (ytoledos@uoc.edu)"
}


# Usamos esta función para todas las descargas.
def descargar(url):
    time.sleep(3)

    try:
        respuesta = requests.get(url, headers=headers, timeout=(5, 20))

        respuesta.raise_for_status()
        return respuesta

    except requests.RequestException as error:
        print(f"No se pudo descargar {url}: {error}")
        return None


# Busca un dato dentro de la ficha de una película.
def obtener_dato(ficha, etiquetas):
    for fila in ficha.find_all("tr"):
        nombre = fila.find("th", recursive=False)
        valor = fila.find("td", recursive=False)

        if nombre is not None and valor is not None:
            if nombre.get_text(" ", strip=True) in etiquetas:

                # Eliminar las referencias, como [1] o [2].
                for referencia in valor.select("sup.reference"):
                    referencia.decompose()

                return valor.get_text(" ", strip=True)

    return ""


# 1. Recorrer los años y reunir los enlaces.
peliculas = []

for anio in anios:
    url = f"https://en.wikipedia.org/wiki/{anio}_in_film"
    respuesta = descargar(url)

    if respuesta is None:
        continue

    soup = BeautifulSoup(respuesta.content, "html.parser")
    seccion = soup.find(id="Highest-grossing_films")

    if seccion is None:
        print(f"No se encontró la sección de taquilla de {anio}.")
        continue

    tabla = seccion.find_next("table", class_="wikitable")

    if tabla is None:
        print(f"No se encontró la tabla de {anio}.")
        continue

    # Saltamos la primera fila, que contiene los encabezados.
    for fila in tabla.find_all("tr")[1:]:
        celdas = fila.find_all(["th", "td"], recursive=False)

        if len(celdas) < 2:
            continue

        # La segunda columna contiene el título.
        enlace = celdas[1].find("a", href=True)

        if enlace is not None:
            peliculas.append({
                "titulo": enlace.get_text(strip=True),
                "anio_listado": anio,
                "url": urljoin(respuesta.url, enlace["href"])
            })

    print(f"Listado de {anio} revisado.")

print(f"Enlaces encontrados: {len(peliculas)}")


# 2. Crear el CSV en la carpeta dataset .
carpeta = Path(__file__).resolve().parent.parent / "dataset"
ruta_csv = carpeta / "data.csv"

columnas = [
    "titulo", "anio_listado", "url", "director", "producida" ,"fechas_estreno",
    "duracion", "presupuesto", "recaudacion", "idioma", "pais", "musica"
]

# Reutilizamos los datos si una misma URL aparece otra vez.
datos_fichas = {}
guardadas = 0

with ruta_csv.open("w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas, delimiter=";")
    escritor.writeheader()

    # 3. Visitar las películas y guardar cada resultado.
    for pelicula in peliculas:
        url = pelicula["url"]

        if url not in datos_fichas:
            respuesta = descargar(url)

            if respuesta is None:
                continue

            soup = BeautifulSoup(respuesta.content, "html.parser")
            ficha = soup.find("table", class_="infobox")

            if ficha is None:
                print(f"No se encontró la ficha de {pelicula['titulo']}.")
                continue

            datos_fichas[url] = {
                "director": obtener_dato(ficha, ["Directed by"]),
                "producida": obtener_dato(ficha, ["Produced by"]),
                "fechas_estreno": obtener_dato(
                    ficha, ["Release date", "Release dates"]
                ),
                "duracion": obtener_dato(ficha, ["Running time"]),
                "presupuesto": obtener_dato(ficha, ["Budget"]),
                "recaudacion": obtener_dato(ficha, ["Box office"]),
                "idioma": obtener_dato(ficha, ["Language", "Languages"]),
                "pais": obtener_dato(ficha, ["Country", "Countries"]),
                "musica": obtener_dato(ficha, ["Music by", "Music"])
            }

        pelicula.update(datos_fichas[url])
        escritor.writerow(pelicula)

        guardadas += 1
        print(f"Guardada: {pelicula['titulo']}")

print(f"Filas guardadas: {guardadas}")
print(f"CSV: {ruta_csv}")