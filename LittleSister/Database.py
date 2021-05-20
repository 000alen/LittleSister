from os.path import exists
from os import mkdir
from asyncio import gather, run
from aiohttp import ClientSession
from json import load, dump
from csv import reader, writer
from geopandas import read_file, points_from_xy
from pandas import read_csv

from LittleSister import database_path, census_path, census_json_path, deputies_path, geojson_path

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


voters_path = database_path / "voters/"
voters_json_path = voters_path / "voters.json"
voters_header = [
    "Domicilio",
    "Circunscripcion",
    "Local?",
    "Mesa"
]


def has_voters():
    return exists(voters_json_path)


def generate_voters():
    print("Generating voters")

    if not exists(voters_path):
        mkdir(voters_path)

    census_json = load(open(census_json_path, encoding="utf-8"))
    for file_name in census_json.values():
        print(f"Current file: {file_name}")

        current_census = reader(open(census_path / file_name))
        current_voters = writer(open(voters_path / file_name, "w", newline=""))

        for row in current_census:
            row = {census_header[i]: row[i] for i in range(len(row))}

            current_voters.writerow([row[key] for key in voters_header])

    dump(census_json, open(voters_json_path, "w", encoding="utf-8"))


pelias_search_url = "http://localhost:4000/v1/search"
pelias_address_format = "{0}, {1}, Region Metropolitana, Chile"
geo_voters_path = database_path / "geo_voters/"
geo_voters_json_path = geo_voters_path / "geo_voters.json"
geo_voters_header = [
    "latitude",
    "longitude",
    "Circunscripcion",
    "Local?",
    "Mesa"
]


def has_geo_voters():
    return exists(geo_voters_json_path)


async def worker_generate_geo_voters_table(session, data_table_path):
    data_table_name = data_table_path.name
    data_table = reader(open(data_table_path))
    table = writer(open(geo_voters_path / data_table_name, "w", newline=""))

    for i, row in enumerate(data_table):
        if i == 0:
            table.writerow(geo_voters_header)
            continue

        row_information = {census_header[i]: row[i] for i in range(len(row))}

        address = pelias_address_format.format(
            row_information["Domicilio"], row_information["Circunscripcion"])
        async with session.get(pelias_search_url, params={"text": address}) as response:
            response_json = await response.json()

            if response_json["features"]:
                latitude = response_json["features"][0]["geometry"]["coordinates"][1]
                longitude = response_json["features"][0]["geometry"]["coordinates"][0]

                table.writerow([latitude, longitude, *row[1::]])

    print(f"Done: {data_table_name}")


async def worker_generate_geo_voters():
    voters_json = load(voters_json_path)
    voters_files_paths = [
        voters_path / voters_file_name for voters_file_name in voters_json.values()]

    async with ClientSession() as session:
        tasks = [
            worker_generate_geo_voters_table(session, voters_file_path)
            for voters_file_path in voters_files_paths
        ]

        await gather(*tasks)


def generate_geo_voters():
    print("Generating geo_voters")
    print("Pelias service must be running")
    run(worker_generate_geo_voters())


geo_voters_threshold_path = database_path / "geo_voters_threshold/"
geo_voters_threshold_json_path = geo_voters_threshold_path / \
    "geo_voters_threshold.json"
geo_voters_threshold_header = [
    "latitude",
    "longitude",
    "Circunscripcion",
    "Local?",
    "Mesa"
]


def has_geo_voters_threshold():
    return exists(geo_voters_threshold_json_path)


def generate_geo_voters_threshold():
    print("Generating geo_voters_threshold")

    if not exists(geo_voters_threshold_path):
        mkdir(geo_voters_threshold_path)

    geo_voters_json = load(open(geo_voters_json_path, encoding="utf-8"))
    for identifier, file_name in geo_voters_json.items():
        print(f"current: {identifier}")

        current_geo_voters = read_csv(geo_voters_path / file_name)

        current_points = points_from_xy(
            current_geo_voters.longitude, current_geo_voters.latitude)

        current_geojson = read_file(geojson_path / f"{identifier}.geojson")

        for i, current_point in enumerate(current_points):
            if not current_geojson.geometry.contains(current_point).any():
                current_geo_voters.drop(i, inplace=True)

        current_geo_voters.to_csv(
            geo_voters_threshold_path / file_name, index=False)

    dump(geo_voters_json, open(geo_voters_json_path, "w", encoding="utf-8"))


minimal_geo_voters_path = database_path / "minimal_geo_voters/"
minimal_geo_voters_json_path = minimal_geo_voters_path / "minimal_geo_voters.json"
minimal_geo_voters_header = [
    "latitude",
    "longitude",
    "Circunscripcion",
    "Mesa"
]


def has_minimal_geo_voters():
    return exists(minimal_geo_voters_json_path)


def generate_minimal_geo_voters():
    print("Generating minimal_geo_voters")

    assert has_geo_voters_threshold()

    if not exists(minimal_geo_voters_path):
        mkdir(minimal_geo_voters_path)

    geo_voters_threshold_json = load(
        open(geo_voters_threshold_json_path, encoding="utf-8"))
    for file_name in geo_voters_threshold_json.values():
        current_geo_voters_threshold = reader(
            open(geo_voters_threshold_path / file_name))
        current_minimal_geo_voters = writer(
            open(minimal_geo_voters_path / file_name, "w", newline=""))

        for row in current_geo_voters_threshold:
            row = {geo_voters_threshold_header[i]: row[i]
                   for i in range(len(row))}

            current_minimal_geo_voters.writerow(
                [row[key] for key in minimal_geo_voters_header])

    dump(geo_voters_threshold_json, open(
        minimal_geo_voters_json_path, "w", encoding="utf-8"))


deputies_with_participation_path = database_path / \
    "deputies_with_participation.csv"
deputies_with_participation_header = [
    "Distrito",
    "Comuna",
    "Circ. Electoral",
    "Local",
    "Nro. Mesa",
    "Tipo Mesa",
    "Mesas Fusionadas",
    "Electores",
    "Lista",
    "Pacto",
    "Partido",
    "Candidato",
    "Votos TRICEL",
    "participation"
]


def has_deputies_with_participation():
    return exists(deputies_with_participation_path)


def generate_deputies_with_participation():
    print("Generating deputies_with_participation")

    deputies = reader(open(deputies_path))
    deputies_with_participation = writer(
        open(deputies_with_participation_path, "w", newline=""))

    current_local = None
    current_number = None
    current_type = None
    buffer = []

    for i, row in enumerate(deputies):
        if i == 0:
            deputies_with_participation.writerow(
                deputies_with_participation_header)
            continue

        row = {deputies_header[i]: row[i] for i in range(len(row))}

        if current_local is None:
            current_local = row["Local"]
            current_number = row["Nro. Mesa"]
            current_type = row["Tipo Mesa"]
            buffer.append([row[key]
                          for key in deputies_with_participation_header[:-1]])
        elif (
            current_local == row["Local"]
            and current_number == row["Nro. Mesa"]
            and current_type == row["Tipo Mesa"]
        ):
            buffer.append([row[key]
                          for key in deputies_with_participation_header[:-1]])
        elif (
            current_local == row["Local"]
            and current_number == row["Nro. Mesa"]
        ):
            current_type = row["Tipo Mesa"]

            participation = sum(
                int(_[-1])
                for _ in buffer
            )

            for buffered in buffer:
                deputies_with_participation.writerow(
                    [*buffered, participation])

            buffer = [[row[key]
                       for key in deputies_with_participation_header[:-1]]]
        elif current_number == row["Local"]:
            current_number = row["Nro. Mesa"]
            current_type = row["Tipo Mesa"]

            participation = sum(
                int(_[-1])
                for _ in buffer
            )

            for buffered in buffer:
                deputies_with_participation.writerow(
                    [*buffered, participation])

            buffer = [[row[key]
                       for key in deputies_with_participation_header[:-1]]]
        else:
            current_local = row["Local"]
            current_number = row["Nro. Mesa"]
            current_type = row["Tipo Mesa"]

            participation = sum(
                int(_[-1])
                for _ in buffer
            )

            for buffered in buffer:
                deputies_with_participation.writerow(
                    [*buffered, participation])

            buffer = [[row[key]
                       for key in deputies_with_participation_header[:-1]]]
    else:
        current_local = row["Local"]
        current_number = row["Nro. Mesa"]
        current_type = row["Tipo Mesa"]

        participation = sum(
            int(_[-1])
            for _ in buffer
        )

        for buffered in buffer:
            deputies_with_participation.writerow([*buffered, participation])


deputies_with_probability_path = database_path / "deputies_with_probability.csv"
deputies_with_probability_header = [
    "Distrito",
    "Comuna",
    "Circ. Electoral",
    "Local",
    "Nro. Mesa",
    "Tipo Mesa",
    "Mesas Fusionadas",
    "Electores",
    "Lista",
    "Pacto",
    "Partido",
    "Candidato",
    "Votos TRICEL",
    "participation",
    "probability"
]


def has_deputies_with_probability():
    return exists(deputies_with_probability_path)


def generate_deputies_with_probability():
    print("Generating deputies_with_probability")

    assert has_deputies_with_participation()

    deputies_with_participation = reader(
        open(deputies_with_participation_path))
    deputies_with_probability = writer(
        open(deputies_with_probability_path, "w", newline=""))

    for i, row in enumerate(deputies_with_participation):
        if i == 0:
            deputies_with_probability.writerow(
                deputies_with_probability_header)
            continue

        row = {
            deputies_with_participation_header[i]: row[i] for i in range(len(row))}

        probability = float(row["Votos TRICEL"]) / float(row["participation"])

        row = [row[key] for key in deputies_with_participation_header]

        deputies_with_probability.writerow([*row, probability])


minimal_deputies_with_probability_path = database_path / \
    "minimal_deputies_with_probability.csv"
minimal_deputies_with_probability_header = [
    "Distrito",
    "Comuna",
    "Circ. Electoral",
    "Local",
    "Nro. Mesa",
    "Tipo Mesa",
    "Electores",
    "Lista",
    "Pacto",
    "Partido",
    "Candidato",
    "Votos TRICEL",
    "participation",
    "probability"
]


def has_minimal_deputies_with_probability():
    return exists(minimal_deputies_with_probability_path)


def generate_minimal_deputies_with_probability():
    print("Generating minimal_deputies_with_probability")

    assert has_deputies_with_probability()

    deputies_with_probability = reader(open(deputies_with_probability_path))
    minimal_deputies_with_probability = writer(
        open(minimal_deputies_with_probability_path, "w", newline=""))

    for i, row in enumerate(deputies_with_probability):
        if i == 0:
            minimal_deputies_with_probability.writerow(
                minimal_deputies_with_probability_header)
            continue

        row = {
            deputies_with_probability_header[i]: row[i] for i in range(len(row))}

        minimal_deputies_with_probability.writerow(
            [row[key] for key in minimal_deputies_with_probability_header])


def setup():
    print("Starting setup")

    if not has_voters():
        generate_voters()

    if not has_geo_voters():
        generate_geo_voters()

    if not has_minimal_geo_voters():
        generate_minimal_geo_voters()

    if not has_deputies_with_participation():
        generate_deputies_with_participation()

    if not has_deputies_with_probability():
        generate_deputies_with_probability()

    if not has_minimal_deputies_with_probability():
        generate_minimal_deputies_with_probability()
