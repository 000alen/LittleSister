import os
import csv
import json
import pandas
import re

import LittleSister.Database as Database
from LittleSister.Database.MinimalGeolocalizedVoters import MinimalGeolocalizedVoters
from LittleSister.Database.MinimalDeputiesWithProbability import MinimalDeputiesWithProbability
from LittleSister.Database.ProbabilityTable import ProbabilityTable


class ProbabilityPoint(Database.Database):
    path = Database.path / "ProbabilityPoint/"

    name_format = "{}_{}_{}.csv"

    header = [
        "latitude",
        "longitude",
        "probability"
    ]

    @staticmethod
    def generate(commune_identifier, candidate_name, probability_threshold):
        print("Generating probability_point")

        if not os.path.exists(ProbabilityPoint.path):
            os.mkdir(ProbabilityPoint.path)

        probability_table_json = json.load(open(ProbabilityTable.json_path / ProbabilityTable.json_name_format.format(
            commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold)))

        minimal_geo_voters = csv.reader(
            open(MinimalGeolocalizedVoters.path / f"{commune_identifier}.csv"))

        probability_point = csv.writer(
            open(ProbabilityPoint.path / ProbabilityPoint.name_format.format(commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold), "w", newline=""))

        for i, row in enumerate(minimal_geo_voters):
            if i == 0:
                probability_point.writerow(
                    ["latitude", "longitude", "probability"])
                continue

            row = {
                MinimalGeolocalizedVoters.header[j]: row[j] for j in range(len(row))}

            probability_point.writerow([row["latitude"], row["longitude"],
                                        probability_table_json.get(row["Mesa"], 0)])
