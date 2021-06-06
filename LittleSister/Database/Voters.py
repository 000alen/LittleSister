import json
import logging
import os

import LittleSister.Database as Database
from LittleSister.Database.ElectoralCensus import ElectoralCensus


class Voters(Database.Database):
    path = Database.path / "Voters/"
    json_path = path / "Voters.json"

    header = [
        "Domicilio",
        "Circunscripcion",
        "Local?",
        "Mesa"
    ]

    @staticmethod
    def exists():
        return os.path.exists(Voters.json_path)

    @staticmethod
    def generate():
        logging.info("Generating Voters")

        if not os.path.exists(Voters.path):
            logging.debug("Voters folder does not exist; creating folder")
            os.mkdir(Voters.path)

        census_json = json.load(
            open(ElectoralCensus.json_path, encoding="utf-8"))
        for file_name in census_json.values():
            logging.info(f"Current file: {file_name}")

            Voters.filter(
                ElectoralCensus.path / file_name,
                ElectoralCensus.header,
                Voters.path / file_name,
                Voters.header
            )

        json.dump(census_json, open(Voters.json_path, "w", encoding="utf-8"))
