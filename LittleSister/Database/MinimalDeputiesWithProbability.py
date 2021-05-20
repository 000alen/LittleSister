import os

import LittleSister.Database as Database
from LittleSister.Database.DeputiesWithProbability import DeputiesWithProbability


class MinimalDeputiesWithProbability(Database.Database):
    path = Database.path / "minimal_deputies_with_probability.csv"
    
    header = [
        "Distrito",
        "Comuna",
        "Circ. Electoral",
        "Local",
        "Nro. Mesa",
        "Tipo Mesa",
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
        return os.path.exists(MinimalDeputiesWithProbability.path)

    @staticmethod
    def generate():
        print("Generating minimal_deputies_with_probability")

        # assert has_deputies_with_probability()

        MinimalDeputiesWithProbability.filter(
            DeputiesWithProbability.path, 
            DeputiesWithProbability.header,
            MinimalDeputiesWithProbability.path,
            MinimalDeputiesWithProbability.header
        )
