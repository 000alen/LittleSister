import os
import csv
import json
import pandas
import re

import LittleSister.Database as Database
from LittleSister.Database.MinimalGeolocalizedVoters import MinimalGeolocalizedVoters
from LittleSister.Database.MinimalDeputiesWithProbability import MinimalDeputiesWithProbability


class ProbabilityTable(Database.Database):
    path = Database.path / "ProbabilityTable/"
    json_path = Database.path / "ProbabilityPoint/"

    name_format = "{}_{}_{}.csv"
    json_name_format = "{}_{}_{}.json"

    header = [
        "probability",
        "Mesa"
    ]

    @staticmethod
    def generate_csv(commune_identifier, candidate_name, probability_threshold):
        print("Generating probability_table")

        if not os.path.exists(ProbabilityTable.path):
            os.mkdir(ProbabilityTable.path)

        communes = json.load(open(Database.communes_path, encoding="utf-8"))
        commune_name = communes[commune_identifier]

        df_deputies = pandas.read_csv(MinimalDeputiesWithProbability.path)

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

        df_probability.to_csv(ProbabilityTable.path / ProbabilityTable.name_format.format(
            commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold), index=False)

    @staticmethod
    def generate(commune_identifier, candidate_name, probability_threshold):
        print("Generating probability_table_json")

        if not os.path.exists(ProbabilityTable.path):
            os.mkdir(ProbabilityTable.path)

        ProbabilityTable.generate_csv(commune_identifier, candidate_name, probability_threshold)

        probability_table = csv.reader(open(ProbabilityTable.path / ProbabilityTable.name_format.format(
            commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold)))

        probability_table_json = {
            mesa.strip(): probability
            for i, (probability, mesa) in enumerate(probability_table)
            if i != 0
        }

        json.dump(probability_table_json, open(ProbabilityTable.json_path /
                                               ProbabilityTable.json_name_format.format(commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold), "w"))
