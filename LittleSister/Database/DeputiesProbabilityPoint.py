import csv
import json
import logging
import os
import re

import LittleSister.Database as Database
from LittleSister.Database.DeputiesProbabilityTable import \
    DeputiesProbabilityTable
from LittleSister.Database.GeolocalizedVoters import GeolocalizedVoters


class DeputiesProbabilityPoint(Database.Database):
    path = Database.path / "DeputiesProbabilityPoint/"

    name_format = "{}_{}_{}.csv"

    header = [
        "latitude",
        "longitude",
        "probability"
    ]

    @staticmethod
    def generate(commune_identifier, candidate_name, probability_threshold):
        logging.info(f"Generating DeputiesProbabilityPoint{(commune_identifier, candidate_name, probability_threshold)}")

        if not os.path.exists(DeputiesProbabilityPoint.path):
            os.mkdir(DeputiesProbabilityPoint.path)

        probability_table_json = json.load(open(DeputiesProbabilityTable.path / DeputiesProbabilityTable.json_name_format.format(
            commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold)))

        minimal_geo_voters = csv.reader(
            open(GeolocalizedVoters.path / f"{commune_identifier}.csv"))

        probability_point = csv.writer(
            open(DeputiesProbabilityPoint.path / DeputiesProbabilityPoint.name_format.format(commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold), "w", newline=""))

        for i, row in enumerate(minimal_geo_voters):
            if i == 0:
                probability_point.writerow(
                    ["latitude", "longitude", "probability"])
                continue

            row = {
                GeolocalizedVoters.header[j]: row[j] for j in range(len(row))}

            probability_point.writerow([row["latitude"], row["longitude"],
                                        probability_table_json.get(row["Mesa"], 0)])
