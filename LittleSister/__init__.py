"""
communes.json
    {identifier}: {commune}

districts.json
    {district}: [{identifier}, ...]

pacts.json
    {pact}: {{party}: [{candidate}, ...], ...}

parties.json
    {party}: [{candidate}, ...]

candidates_per_district.json
    {district}: [{candidate}, ...]

census/
    {identifier}.csv
        RUT
        DV
        Proper RUT
        Nombre completo
        Primer nombre
        Segundo nombre
        Primer apellido
        Segundo apellido
        Sexo
        Domicilio
        Circunscripcion
        Local?
        Mesa
        Pueblo

deputies.csv
    Región
    Provincia
    Circ. Senatorial
    Distrito
    Comuna
    Circ. Electoral
    Local
    Nro. Mesa
    Tipo Mesa
    Mesas Fusionadas
    Electores
    Nro. En Voto
    Lista
    Pacto
    Partido
    Candidato
    Votos TRICEL

census/ -> voters/
    {identifier}.csv
        Domicilio
        Circunscripcion
        Local?
        Mesa

voters/ -> geo_voters/
    {identifier}.csv
        * latitude
        * longitude
        Circunscripcion
        Local?
        Mesa

geo_voters -> minimal_geo_voters/
    {identifier}.csv
        * latitude
        * longitude
        Circunscripcion
        Mesa

deputies.csv -> deputies_with_participation.csv
    Distrito
    Comuna
    Circ. Electoral
    Local
    Nro. Mesa
    Tipo Mesa
    Mesas Fusionadas
    Electores
    Lista
    Pacto
    Partido
    Candidato
    Votos TRICEL
    * Participacion

deputies_with_participation.csv -> deputies_with_probability.csv
    Distrito
    Comuna
    Circ. Electoral
    Local
    Nro. Mesa
    Tipo Mesa
    Mesas Fusionadas
    Electores
    Lista
    Pacto
    Partido
    Candidato
    Votos TRICEL
    Participacion
    * Probabilidad

deputies_with_probability.csv -> minimal_deputies_with_probability.csv
    Distrito
    Comuna
    Circ. Electoral
    Nro. Mesa
    Tipo Mesa
    Electores
    Lista
    Pacto
    Partido
    Candidato
    Votos TRICEL
    Participacion
    Probabilidad
"""

from pathlib import Path

database_path = Path("./database/")

communes_path = database_path / "communes.json"
districts_path = database_path / "districts.json"
pacts_path = database_path / "pacts.json"
parties_path = database_path / "parties.json"
candidates_per_district_path = database_path / "candidates_per_district.json"

census_path = database_path / "census/"
census_json_path = census_path / "census.json"

deputies_path = database_path / "deputies.csv"

if not database_path.is_dir():
    raise Exception("The database/ folder does not exist")

if not communes_path.is_file():
    raise Exception("The database/communes.json file does not exist")

if not districts_path.is_file():
    raise Exception("The database/districts.json file does not exist")

if not pacts_path.is_file():
    raise Exception("The database/pacts.json file does not exist")

if not parties_path.is_file():
    raise Exception("The database/parties.json file does not exist")

if not candidates_per_district_path.is_file():
    raise Exception("The database/candidates_per_district.json file does not exist")

if not census_path.is_dir():
    raise Exception("The database/census/ folder does not exist")

if not census_json_path.is_file():
    raise Exception("The database/census/census.json file does not exist")

if not deputies_path.is_file():
    raise Exception("The database/deputies.csv file does not exist")
