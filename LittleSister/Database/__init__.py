import pathlib
import csv
import abc

path = pathlib.Path("./database/")
census_path = path / "census/"
census_json_path = census_path / "census.json"
geojson_path = path / "geojson/"
deputies_path = path / "deputies.csv"
candidates_per_district_path = path / "candidates_per_district.json"
communes_location_path = path / "communes_location.json"
communes_path = path / "communes.json"
districts_path = path / "districts.json"
pacts_path = path / "pacts.json"
parties_path = path / "parties.json"

if not path.is_dir():
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
    raise Exception(
        "The database/candidates_per_district.json file does not exist")

if not census_path.is_dir():
    raise Exception("The database/census/ folder does not exist")

if not census_json_path.is_file():
    raise Exception("The database/census/census.json file does not exist")

if not deputies_path.is_file():
    raise Exception("The database/deputies.csv file does not exist")

census_header = [
    "RUT",
    "DV",
    "Proper RUT",
    "Nombre completo",
    "Primer nombre",
    "Segundo nombre",
    "Primer apellido",
    "Segundo apellido",
    "Sexo",
    "Domicilio",
    "Circunscripcion",
    "Local?",
    "Mesa",
    "Pueblo",
]

deputies_header = [
    "Región",
    "Provincia",
    "Circ. Senatorial",
    "Distrito",
    "Comuna",
    "Circ. Electoral",
    "Local",
    "Nro. Mesa",
    "Tipo Mesa",
    "Mesas Fusionadas",
    "Electores",
    "Nro. En Voto",
    "Lista",
    "Pacto",
    "Partido",
    "Candidato",
    "Votos TRICEL"
]


class Database(abc.ABC):
    @abc.abstractstaticmethod
    def exists():
        raise NotImplementedError

    @abc.abstractstaticmethod
    def generate():
        raise NotImplementedError

    def filter(input_path: pathlib.Path, input_header: list[str], output_path: pathlib.Path, output_header: list[str]):
        input_table = csv.reader(open(input_path, encoding="utf-8"))
        output_table = csv.writer(open(output_path, "w", newline=""))

        for i, row in enumerate(input_table):
            if i == 0:
                output_table.writerow(output_header)
                continue

            row = {input_header[i]: row[i] for i in range(len(row))}
            output_table.writerow([row[key] for key in output_header])


def generate():
    print("Starting setup")

    from LittleSister.Database.Voters import Voters
    from LittleSister.Database.GeoVoters import GeoVoters
    from LittleSister.Database.GeoVotersThreshold import GeoVotersThreshold
    from LittleSister.Database.MinimalGeoVoters import MinimalGeoVoters
    from LittleSister.Database.DeputiesWithParticipation import DeputiesWithParticipation
    from LittleSister.Database.DeputiesWithProbability import DeputiesWithProbability
    from LittleSister.Database.MinimalDeputiesWithProbability import MinimalDeputiesWithProbability

    if not Voters.exists():
        Voters.generate()

    if not GeoVoters.exists():
        GeoVoters.generate()

    if not GeoVotersThreshold.exists():
        GeoVotersThreshold.generate()

    if not MinimalGeoVoters.exists():
        MinimalGeoVoters.generate()

    if not DeputiesWithParticipation.exists():
        DeputiesWithParticipation.generate()

    if not DeputiesWithProbability.exists():
        DeputiesWithProbability.generate()

    if not MinimalDeputiesWithProbability.exists():
        MinimalDeputiesWithProbability.generate()
