# LittleSister

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

Herramienta para análisis y visualización de datos de las elecciones chilenas.

## Instalación

Para instalar las librerías necesarias, se debe ejecutar el comando `pip install -r requirements.txt`. Se recomienda el uso de [Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) para manejar las dependencias.

Luego, es necesario [descargar las bases de datos necesarias](./database/README.md). 

Finalmente, es necesario instalar [Pelias](https://github.com/pelias/docker/). Una vez hecha la instalación, es necesario [generar una instancia de Pelias](./pelias/README.md) para generar las bases de datos que implican geocodificación.

## Uso

Para generar las bases de datos complementarias se debe usar el comando `python -m LittleSister --generate-database`.

Para generar puntos probabilísticos se debe usar el comando `python -m LittleSister --generate-point --commune-identifer {commune_identifier} --candidate-name {candidate_name} --probability-threshold {probability_threshold}`. Donde `commune_identifier` es el identificador de la comuna, `candidate_name` es el nombre del (la) candidato (a) y `probability_threshold` es el umbral mínimo de probabilidad a considerar.

Para ver las opciones de comandos disponibles se debe usar el comando `python - LittleSister --help`.
