# Web scraping de películas en Wikipedia

El programa recorre los listados de películas de mayor recaudación de Wikipedia en inglés entre 2000 y 2025. Después visita los artículos de las películas y guarda sus datos en un archivo CSV.

## Requisitos

- Python 3.10 o superior.
- Conexión a Internet.
- Las librerías indicadas en `requirements.txt`:
  - `requests==2.34.2`: descarga las páginas.
  - `beautifulsoup4==4.15.0`: permite buscar y extraer datos del HTML.


## Archivos del proyecto

- `source/scraper.py`: código del programa.
- `data/`: carpeta donde se guarda el resultado.
- `requirements.txt`: dependencias y sus versiones.
- `README.md`: instrucciones de uso.

## Ejecución

1. Abre una terminal en la raíz del proyecto, donde están `requirements.txt` y las carpetas `source` y `data`. Si utilizas un entorno virtual, ejecuta los comandos con ese entorno activo.

2. Instala las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Ejecuta el programa:

   ```bash
   python source/scraper.py
   ```

El programa muestra el progreso en la terminal y espera tres segundos antes de cada petición HTTP.

## Resultado

Los datos se guardan en `data/data.csv`, con los siguientes campos:

- Título.
- Año del listado.
- URL.
- Director.
- Productor.
- Fechas de estreno.
- Duración.
- Presupuesto.
- Recaudación.
- Idioma.
- País.
- Banda sonora (música)

