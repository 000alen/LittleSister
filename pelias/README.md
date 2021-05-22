# `pelias/` 

Instancia de [Pelias](https://github.com/pelias/docker/) para generar las bases de datos que impliquen geocodificación.

## Pre-requisitos

Para instalar los pre-requisitos se debe seguir la [guía de instalación de Pelias](https://github.com/pelias/docker/).

## Uso

Para generar la instancia de Pelias se debe comprobar si existe el directorio `data/`; en caso de que no exista, se debe ejecutar el comando `mkdir data`. Luego, se deben ejecutar los siguientes comandos:

```
pelias compose pull
pelias elastic start
pelias elastic wait
pelias elastic create
pelias download all
pelias prepare all
pelias import all
pelias compose up
```
