import os
import csv
import json
import pandas
import re

import LittleSister.Database as Database
from LittleSister.Database.DeputiesElection import DeputiesElection


class DeputiesProbabilityTable(Database.Database):
    path = Database.path / "DeputiesProbabilityTable/"

    name_format = "{}_{}_{}.csv"
    json_name_format = "{}_{}_{}.json"

    header = [
        "probability",
        "Mesa"
    ]

    @staticmethod
    def generate_csv(commune_identifier, candidate_name, probability_threshold):
        print("Generating probability_table")

        if not os.path.exists(DeputiesProbabilityTable.path):
            os.mkdir(DeputiesProbabilityTable.path)

        communes = json.load(open(Database.communes_path, encoding="utf-8"))
        commune_name = communes[commune_identifier]

        df_deputies = pandas.read_csv(DeputiesElection.path)

        df_probability = df_deputies[
            (df_deputies["Comuna"] == commune_name) & (
                df_deputies["Candidato"] == candidate_name)
        ]

        df_probability = df_probability[df_probability["probability"]
                                        > probability_threshold]

        df_probability["Mesa"] = df_probability["Nro. Mesa"].apply(
            str) + " " + df_probability["Tipo Mesa"]

        df_probability["Mesa"] = df_probability["Mesa"].apply(
            lambda x: x.strip())

        df_probability = df_probability[["probability", "Mesa"]]

        df_probability.to_csv(DeputiesProbabilityTable.path / DeputiesProbabilityTable.name_format.format(
            commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold), index=False)

    @staticmethod
    def generate(commune_identifier, candidate_name, probability_threshold):
        print("Generating probability_table_json")

        if not os.path.exists(DeputiesProbabilityTable.path):
            os.mkdir(DeputiesProbabilityTable.path)

        DeputiesProbabilityTable.generate_csv(commune_identifier, candidate_name, probability_threshold)

        probability_table = csv.reader(open(DeputiesProbabilityTable.path / DeputiesProbabilityTable.name_format.format(
            commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold)))

        probability_table_json = {
            mesa.strip(): probability
            for i, (probability, mesa) in enumerate(probability_table)
            if i != 0
        }

        json.dump(probability_table_json, open(DeputiesProbabilityTable.path /
                                               DeputiesProbabilityTable.json_name_format.format(commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold), "w"))
