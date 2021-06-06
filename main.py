import json

from LittleSister.Database import districts_path
from LittleSister.Database.DeputiesProbabilityTable import DeputiesProbabilityTable
from LittleSister.Database.DeputiesProbabilityPoint import DeputiesProbabilityPoint
from LittleSister.Visualization import view

district = 10
candidate_name = "GONZALO WINTER ETCHEBERRY"
probability_threshold = 0

districts = json.load(open(districts_path, encoding="utf-8"))
communes_identifiers = districts[str(district)]

for commune_identifier in communes_identifiers:
    DeputiesProbabilityTable.generate(
        commune_identifier, candidate_name, probability_threshold)
    DeputiesProbabilityPoint.generate(
        commune_identifier, candidate_name, probability_threshold)

view(district, candidate_name, probability_threshold)
