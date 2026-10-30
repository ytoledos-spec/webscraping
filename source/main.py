import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

anio = 2021
url = f"https://en.wikipedia.org/wiki/{anio}_in_film"

headers = {
    "User-Agent": "PracticaCineBot/1.0 (ytoledos@uoc.edu)"
}

# 1. Descargar la página
try:
    respuesta = requests.get(url, headers=headers, timeout=(5, 20))
    respuesta.raise_for_status()
except requests.RequestException as error:
    raise SystemExit(f"No se pudo descargar la página: {error}")

# 2. Preparar el HTML para buscar sus elementos
soup = BeautifulSoup(respuesta.content, "html.parser")

# 3. Buscar la tabla mediante su caption
tabla = None

for caption in soup.find_all("caption"):
    # Quitar las referencias del caption, como [2] y [3]
    for referencia in caption.find_all("sup"):
        referencia.decompose()

    texto = caption.get_text(" ", strip=True)

    if texto == f"Highest-grossing films of {anio}":
        tabla = caption.find_parent("table")
        break

if tabla is None:
    raise SystemExit("No se encontró la tabla de películas.")

# 4. Obtener el título y el enlace de cada película
for fila in tabla.find_all("tr"):
    celda = fila.find("td", recursive=False)

    if celda is not None:
        enlace = celda.find("a", href=True)

        if enlace is not None:
            titulo = enlace.get_text(strip=True)
            url_pelicula = urljoin(respuesta.url, enlace["href"])

            print(f"{titulo} → {url_pelicula}")
