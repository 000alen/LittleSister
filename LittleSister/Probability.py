from os import mkdir
from os.path import exists
from csv import reader, writer
from json import load, dump
from pandas import read_csv
from re import sub

from LittleSister import database_path, communes_path
from LittleSister.Database import minimal_deputies_with_probability_path, minimal_geo_voters_path, minimal_geo_voters_header


probability_table_path = database_path / "probability_table/"
probability_table_name_format = "{}_{}_{}.csv"
probability_table_header = [
    "probability",
    "Mesa"
]


# XXX
def generate_probability_table(commune_identifier, candidate_name, probability_threshold):
    print("Generating probability_table")

    if not exists(probability_table_path):
        mkdir(probability_table_path)

    communes = load(open(communes_path, encoding="utf-8"))
    commune_name = communes[commune_identifier]

    df_deputies = read_csv(minimal_deputies_with_probability_path)

    df_probability = df_deputies[
        (df_deputies["Comuna"] == commune_name) & (
            df_deputies["Candidato"] == candidate_name)
    ]

    df_probability = df_probability[df_probability["probability"]
                                    > probability_threshold]

    df_probability["Mesa"] = df_probability["Nro. Mesa"].apply(
        str) + " " + df_probability["Tipo Mesa"]

    df_probability["Mesa"] = df_probability["Mesa"].apply(lambda x: x.strip())

    df_probability = df_probability[["probability", "Mesa"]]

    df_probability.to_csv(probability_table_path / probability_table_name_format.format(
        commune_identifier, sub(r" +" , "_", candidate_name), probability_threshold), index=False)


probability_table_json_path = database_path / "probability_table/"
probability_table_json_name_format = "{}_{}_{}.json"


def generate_probability_table_json(commune_identifier, candidate_name, probability_threshold):
    print("Generating probability_table_json")

    if not exists(probability_table_path):
        mkdir(probability_table_path)

    probability_table = reader(open(probability_table_path / probability_table_name_format.format(
        commune_identifier, sub(r" +" , "_", candidate_name), probability_threshold)))

    probability_table_json = {
        mesa.strip(): probability
        for i, (probability, mesa) in enumerate(probability_table)
        if i != 0
    }

    dump(probability_table_json, open(probability_table_json_path /
         probability_table_json_name_format.format(commune_identifier, sub(r" +" , "_", candidate_name), probability_threshold), "w"))


probability_point_path = database_path / "probability_point/"
probability_point_name_format = "{}_{}_{}.csv"
probability_point_header = [
    "latitude",
    "longitude",
    "probability"
]


def generate_probability_point(commune_identifier, candidate_name, probability_threshold):
    print("Generating probability_point")

    if not exists(probability_point_path):
        mkdir(probability_point_path)

    probability_table_json = load(open(probability_table_json_path / probability_table_json_name_format.format(
        commune_identifier, sub(r" +" , "_", candidate_name), probability_threshold)))

    minimal_geo_voters = reader(
        open(minimal_geo_voters_path / f"{commune_identifier}.csv"))

    probability_point = writer(
        open(probability_point_path / probability_point_name_format.format(commune_identifier, sub(r" +" , "_", candidate_name), probability_threshold), "w", newline=""))

    for i, row in enumerate(minimal_geo_voters):
        if i == 0:
            probability_point.writerow(
                ["latitude", "longitude", "probability"])
            continue

        row = {minimal_geo_voters_header[j]: row[j] for j in range(len(row))}

        probability_point.writerow([row["latitude"], row["longitude"],
                                    probability_table_json.get(row["Mesa"], 0)])
