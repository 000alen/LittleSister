import os
import json

import LittleSister.Database as Database
from LittleSister.Database.GeolocalizedVoters import GeolocalizedVoters


class MinimalGeolocalizedVoters(Database.Database):
    path = Database.path / "MinimalGeolocalizedVoters/"
    json_path = path / "MinimalGeolocalizedVoters.json"

    header = [
        "latitude",
        "longitude",
        "Circunscripcion",
        "Mesa"
    ]

    @staticmethod
    def exists():
        return os.path.exists(MinimalGeolocalizedVoters.path)

    @staticmethod
    def generate():
        print("Generating minimal_geo_voters")

        # assert has_geo_voters_threshold()

        if not os.path.exists(MinimalGeolocalizedVoters.path):
            os.mkdir(MinimalGeolocalizedVoters.path)

        geo_voters_threshold_json = json.load(
            open(GeolocalizedVoters.json_path, encoding="utf-8"))
        for file_name in geo_voters_threshold_json.values():
            MinimalGeolocalizedVoters.filter(
                GeolocalizedVoters.path / file_name,
                GeolocalizedVoters.header,
                MinimalGeolocalizedVoters.path / file_name,
                MinimalGeolocalizedVoters.header
            )

        json.dump(geo_voters_threshold_json, open(
            MinimalGeolocalizedVoters.json_path, "w", encoding="utf-8"))
