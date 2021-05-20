import os
import csv

import LittleSister.Database as Database
from LittleSister.Database.DeputiesWithParticipation import DeputiesWithParticipation


class DeputiesWithProbability(Database.Database):
    path = Database.path / "deputies_with_probability.csv"

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
        "participation",
        "probability"
    ]

    @staticmethod
    def exists():
        return os.path.exists(DeputiesWithProbability.path)

    @staticmethod
    def generate():
        print("Generating deputies_with_probability")

        # assert has_deputies_with_participation()

        deputies_with_participation = csv.reader(
            open(DeputiesWithParticipation.path))
        deputies_with_probability = csv.writer(
            open(DeputiesWithProbability.path, "w", newline=""))

        for i, row in enumerate(deputies_with_participation):
            if i == 0:
                deputies_with_probability.writerow(
                    DeputiesWithProbability.header)
                continue

            row = {
                DeputiesWithParticipation.header[i]: row[i] for i in range(len(row))}

            probability = float(row["Votos TRICEL"]) / \
                float(row["participation"])

            row = [row[key] for key in DeputiesWithParticipation.header]

            deputies_with_probability.writerow([*row, probability])
