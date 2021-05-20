import os
import json
import geopandas
import pandas

import LittleSister.Database as Database
from LittleSister.Database.GeoVoters import GeoVoters


class GeoVotersThreshold(Database.Database):
    path = Database.path / "geo_voters_threshold/"
    json_path = path / "geo_voters_threshold.json"

    header = [
        "latitude",
        "longitude",
        "Circunscripcion",
        "Local?",
        "Mesa"
    ]

    @staticmethod
    def exists():
        return os.path.exists(GeoVotersThreshold.path)

    @staticmethod
    def generate():
        print("Generating geo_voters_threshold")

        if not os.path.exists(GeoVotersThreshold.path):
            os.mkdir(GeoVotersThreshold.path)

        geo_voters_json = json.load(
            open(GeoVoters.json_path, encoding="utf-8"))
        for identifier, file_name in geo_voters_json.items():
            print(f"current: {identifier}")

            current_geo_voters = pandas.read_csv(GeoVoters.path / file_name)

            current_points = geopandas.points_from_xy(
                current_geo_voters.longitude, current_geo_voters.latitude)

            current_geojson = geopandas.read_file(
                Database.geojson_path / f"{identifier}.geojson")

            for i, current_point in enumerate(current_points):
                if not current_geojson.geometry.contains(current_point).any():
                    current_geo_voters.drop(i, inplace=True)

            current_geo_voters.to_csv(
                GeoVotersThreshold.path / file_name, index=False)

        json.dump(geo_voters_json, open(
            GeoVotersThreshold.json_path, "w", encoding="utf-8"))
