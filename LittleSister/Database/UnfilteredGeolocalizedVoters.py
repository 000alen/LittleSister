import os
import asyncio
import pathlib
import aiohttp
import json
import csv
import logging

import LittleSister.Database as Database
from LittleSister.Database.Voters import Voters


class UnfilteredGeolocalizedVoters(Database.Database):
    path = Database.path / "UnfilteredGeolocalizedVoters/"
    json_path = path / "UnfilteredGeolocalizedVoters.json"

    header = [
        "latitude",
        "longitude",
        "Circunscripcion",
        "Local?",
        "Mesa"
    ]

    pelias_search_url = "http://localhost:4000/v1/search"
    pelias_address_format = "{0}, {1}, Region Metropolitana, Chile"

    @staticmethod
    def exists():
        return os.path.exists(UnfilteredGeolocalizedVoters.json_path)

    @staticmethod
    async def worker_generate_table(session: aiohttp.ClientSession, data_table_path: pathlib.Path):
        data_table_name = data_table_path.name
        logging.info(f"Current file: {data_table_name}.csv")
        data_table = csv.reader(open(data_table_path))
        table = csv.writer(
            open(UnfilteredGeolocalizedVoters.path / data_table_name, "w", newline=""))

        for i, row in enumerate(data_table):
            if i == 0:
                table.writerow(UnfilteredGeolocalizedVoters.path)
                continue

            row_information = {Voters.header[i]: row[i]
                               for i in range(len(row))}

            address = UnfilteredGeolocalizedVoters.pelias_address_format.format(
                row_information["Domicilio"], row_information["Circunscripcion"])
            async with session.get(UnfilteredGeolocalizedVoters.pelias_search_url, params={"text": address}) as response:
                response_json = await response.json()

                if response_json["features"]:
                    latitude = response_json["features"][0]["geometry"]["coordinates"][1]
                    longitude = response_json["features"][0]["geometry"]["coordinates"][0]

                    table.writerow([latitude, longitude, *row[1::]])

    @staticmethod
    async def worker_generate():
        voters_json = json.load(Voters.json_path)
        voters_files_paths = [
            Voters.path / file_name for file_name in voters_json.values()]

        async with aiohttp.ClientSession() as session:
            tasks = [
                UnfilteredGeolocalizedVoters.worker_generate_table(session, file_path)
                for file_path in voters_files_paths
            ]

            await asyncio.gather(*tasks)

    @staticmethod
    def generate():
        logging.info("Generating UnfilteredGeolocalizedVoters")
        logging.warning("Pelias service must be running")
        asyncio.run(UnfilteredGeolocalizedVoters.worker_generate())
