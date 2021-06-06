import os
import json
import geopandas
import pandas
import logging

import LittleSister.Database as Database
from LittleSister.Database.UnfilteredGeolocalizedVoters import UnfilteredGeolocalizedVoters


class GeolocalizedVoters(Database.Database):
    path = Database.path / "GeolocalizedVoters/"
    json_path = path / "GeolocalizedVoters.json"

    header = [
        "latitude",
        "longitude",
        "Circunscripcion",
        "Local?",
        "Mesa"
    ]

    @staticmethod
    def exists():
        return os.path.exists(GeolocalizedVoters.path)

    @staticmethod
    def generate():
        logging.info("Generating GeolocalizedVotes")

        if not os.path.exists(GeolocalizedVoters.path):
            os.mkdir(GeolocalizedVoters.path)

        geo_voters_json = json.load(
            open(UnfilteredGeolocalizedVoters.json_path, encoding="utf-8"))
        for identifier, file_name in geo_voters_json.items():
            logging.info(f"Current file: {identifier}.csv")

            current_geo_voters = pandas.read_csv(UnfilteredGeolocalizedVoters.path / file_name)

            current_points = geopandas.points_from_xy(
                current_geo_voters.longitude, current_geo_voters.latitude)

            current_geojson = geopandas.read_file(
                Database.geojson_path / f"{identifier}.geojson")

            for i, current_point in enumerate(current_points):
                if not current_geojson.geometry.contains(current_point).any():
                    current_geo_voters.drop(i, inplace=True)

            current_geo_voters.to_csv(
                GeolocalizedVoters.path / file_name, index=False)

        json.dump(geo_voters_json, open(
            GeolocalizedVoters.json_path, "w", encoding="utf-8"))
