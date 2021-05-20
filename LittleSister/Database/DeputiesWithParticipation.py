import os
import csv

import LittleSister.Database as Database


class DeputiesWithParticipation(Database.Database):
    path = Database.path / "deputies_with_participation.csv"

    header = [
        "Distrito",
        "Comuna",
        "Circ. Electoral",
        "Local",
        "Nro. Mesa",
        "Tipo Mesa",
        "Mesas Fusionadas",
        "Electores",
        "Lista",
        "Pacto",
        "Partido",
        "Candidato",
        "Votos TRICEL",
        "participation"
    ]

    @staticmethod
    def exists():
        return os.path.exists(DeputiesWithParticipation.path)

    @staticmethod
    def generate():
        print("Generating deputies_with_participation")

        deputies = csv.reader(open(Database.deputies_path))
        deputies_with_participation = csv.writer(
            open(DeputiesWithParticipation.path, "w", newline=""))

        current_local = None
        current_number = None
        current_type = None
        buffer = []

        for i, row in enumerate(deputies):
            if i == 0:
                deputies_with_participation.writerow(
                    DeputiesWithParticipation.header)
                continue

            row = {Database.deputies_header[i]: row[i]
                   for i in range(len(row))}

            if current_local is None:
                current_local = row["Local"]
                current_number = row["Nro. Mesa"]
                current_type = row["Tipo Mesa"]
                buffer.append([row[key]
                               for key in DeputiesWithParticipation.header[:-1]])
            elif (
                current_local == row["Local"]
                and current_number == row["Nro. Mesa"]
                and current_type == row["Tipo Mesa"]
            ):
                buffer.append([row[key]
                               for key in DeputiesWithParticipation.header[:-1]])
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
                    deputies_with_participation.writerow(
                        [*buffered, participation])

                buffer = [[row[key]
                           for key in DeputiesWithParticipation.header[:-1]]]
            elif current_number == row["Local"]:
                current_number = row["Nro. Mesa"]
                current_type = row["Tipo Mesa"]

                participation = sum(
                    int(_[-1])
                    for _ in buffer
                )

                for buffered in buffer:
                    deputies_with_participation.writerow(
                        [*buffered, participation])

                buffer = [[row[key]
                           for key in DeputiesWithParticipation.header[:-1]]]
            else:
                current_local = row["Local"]
                current_number = row["Nro. Mesa"]
                current_type = row["Tipo Mesa"]

                participation = sum(
                    int(_[-1])
                    for _ in buffer
                )

                for buffered in buffer:
                    deputies_with_participation.writerow(
                        [*buffered, participation])

                buffer = [[row[key]
                           for key in DeputiesWithParticipation.header[:-1]]]
        else:
            current_local = row["Local"]
            current_number = row["Nro. Mesa"]
            current_type = row["Tipo Mesa"]

            participation = sum(
                int(_[-1])
                for _ in buffer
            )

            for buffered in buffer:
                deputies_with_participation.writerow(
                    [*buffered, participation])
