import os
import json

import LittleSister.Database as Database
from LittleSister.Database.GeoVotersThreshold import GeoVotersThreshold


class MinimalGeoVoters(Database.Database):
    path = Database.path / "minimal_geo_voters/"
    json_path = path / "minimal_geo_voters.json"

    header = [
        "latitude",
        "longitude",
        "Circunscripcion",
        "Mesa"
    ]

    @staticmethod
    def exists():
        return os.path.exists(MinimalGeoVoters.path)

    @staticmethod
    def generate():
        print("Generating minimal_geo_voters")

        # assert has_geo_voters_threshold()

        if not os.path.exists(MinimalGeoVoters.path):
            os.mkdir(MinimalGeoVoters.path)

        geo_voters_threshold_json = json.load(
            open(GeoVotersThreshold.json_path, encoding="utf-8"))
        for file_name in geo_voters_threshold_json.values():
            MinimalGeoVoters.filter(
                GeoVotersThreshold.path / file_name,
                GeoVotersThreshold.header,
                MinimalGeoVoters.path / file_name,
                MinimalGeoVoters.header
            )

        json.dump(geo_voters_threshold_json, open(
            MinimalGeoVoters.json_path, "w", encoding="utf-8"))
