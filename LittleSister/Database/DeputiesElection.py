import logging
import os
import csv
import pandas

import LittleSister.Database as Database


class DeputiesElection(Database.Database):
    final_stage = 2

    path_stage_0 = Database.path / "DeputiesElection/0.csv"
    path_stage_1 = Database.path / "DeputiesElection/1.csv"
    path_stage_2 = Database.path / "DeputiesElection/2.csv"
    path = Database.path / f"DeputiesElection/{final_stage}.csv"
    json_path = path / "DeputiesElection.json"

    header = [
        "Región",
        "Provincia",
        "Circ. Senatorial",
        "Distrito",
        "Comuna",
        "Circ. Electoral",
        "Local",
        "Nro. Mesa",
        "Tipo Mesa",
        "Mesas Fusionadas",
        "Electores",
        "Nro. En Voto",
        "Lista",
        "Pacto",
        "Partido",
        "Candidato",
        "Votos TRICEL",
        "participation",
        "probability"
    ]

    @staticmethod
    def exists():
        return os.path.exists(DeputiesElection.json_path)

    @staticmethod
    def generate():
        logging.info("Generating DeputiesElection")
        DeputiesElection.generate_stage_1()
        DeputiesElection.generate_stage_2()

    @staticmethod
    def generate_stage_1():
        logging.info("Generating DeputiesElection stage 1")

        stage_0 = csv.reader(open(DeputiesElection.path_stage_0))
        stage_1 = csv.writer(
            open(DeputiesElection.path_stage_1, "w", newline=""))

        current_local = None
        current_number = None
        current_type = None
        buffer = []

        for i, row in enumerate(stage_0):
            if i == 0:
                stage_1.writerow(
                    DeputiesElection.header)
                continue

            row = {DeputiesElection.header[i]: row[i]
                   for i in range(len(row))}

            if current_local is None:
                current_local = row["Local"]
                current_number = row["Nro. Mesa"]
                current_type = row["Tipo Mesa"]
                buffer.append([row[key]
                               for key in DeputiesElection.header[:-2]])
            elif (
                current_local == row["Local"]
                and current_number == row["Nro. Mesa"]
                and current_type == row["Tipo Mesa"]
            ):
                buffer.append([row[key]
                               for key in DeputiesElection.header[:-2]])
            elif (
                current_local == row["Local"]
                and current_number == row["Nro. Mesa"]
            ):
                current_type = row["Tipo Mesa"]

                participation = sum(
                    int(_[-1])
                    for _ in buffer
                )

                for buffered in buffer:
                    stage_1.writerow(
                        [*buffered, participation])

                buffer = [[row[key]
                           for key in DeputiesElection.header[:-2]]]
            elif current_number == row["Local"]:
                current_number = row["Nro. Mesa"]
                current_type = row["Tipo Mesa"]

                participation = sum(
                    int(_[-1])
                    for _ in buffer
                )

                for buffered in buffer:
                    stage_1.writerow(
                        [*buffered, participation])

                buffer = [[row[key]
                           for key in DeputiesElection.header[:-2]]]
            else:
                current_local = row["Local"]
                current_number = row["Nro. Mesa"]
                current_type = row["Tipo Mesa"]

                participation = sum(
                    int(_[-1])
                    for _ in buffer
                )

                for buffered in buffer:
                    stage_1.writerow(
                        [*buffered, participation])

                buffer = [[row[key]
                           for key in DeputiesElection.header[:-2]]]
        else:
            current_local = row["Local"]
            current_number = row["Nro. Mesa"]
            current_type = row["Tipo Mesa"]

            participation = sum(
                int(_[-1])
                for _ in buffer
            )

            for buffered in buffer:
                stage_1.writerow(
                    [*buffered, participation])

    @staticmethod
    def generate_stage_2():
        logging.info("Generating DeputiesElection stage 2")

        stage_1 = csv.reader(
            open(DeputiesElection.path_stage_1))
        stage_2 = csv.writer(
            open(DeputiesElection.path_stage_2, "w", newline=""))

        for i, row in enumerate(stage_1):
            if i == 0:
                stage_2.writerow(
                    DeputiesElection.header)
                continue

            row = {
                DeputiesElection.header[i]: row[i] for i in range(len(row))}

            probability = float(row["Votos TRICEL"]) / \
                float(row["participation"])

            row = [row[key] for key in DeputiesElection.header[:-1]]

            stage_2.writerow([*row, probability])
