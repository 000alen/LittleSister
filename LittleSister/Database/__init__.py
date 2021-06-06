import logging
import pathlib
import csv
import abc

path = pathlib.Path("./database/")
geojson_path = path / "geojson/"
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


def initialize():
    logging.info("Initializing Database")

    from LittleSister.Database.DeputiesElection import DeputiesElection
    from LittleSister.Database.Voters import Voters
    from LittleSister.Database.UnfilteredGeolocalizedVoters import UnfilteredGeolocalizedVoters
    from LittleSister.Database.GeolocalizedVoters import GeolocalizedVoters

    if not DeputiesElection.exists():
        DeputiesElection.generate()

    if not Voters.exists():
        Voters.generate()

    if not UnfilteredGeolocalizedVoters.exists():
        UnfilteredGeolocalizedVoters.generate()

    if not GeolocalizedVoters.exists():
        GeolocalizedVoters.generate()
