import os
import json

import LittleSister.Database as Database


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
        if not os.path.exists(Voters.path):
            os.mkdir(Voters.path)

        census_json = json.load(
            open(Database.census_json_path, encoding="utf-8"))
        for file_name in census_json.values():
            print(f"Current file: {file_name}")

            Voters.filter(
                Database.census_path / file_name,
                Database.census_header,
                Voters.path / file_name,
                Voters.header
            )

        json.dump(census_json, open(Voters.json_path, "w", encoding="utf-8"))
