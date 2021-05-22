import json

from LittleSister.Database import districts_path
from LittleSister.Database.ProbabilityTable import ProbabilityTable
from LittleSister.Database.ProbabilityPoint import ProbabilityPoint
from LittleSister.Visualization import view

district = 10
candidate_name = "GONZALO WINTER ETCHEBERRY"
probability_threshold = 0

districts = json.load(open(districts_path, encoding="utf-8"))
communes_identifiers = districts[str(district)]

for commune_identifier in communes_identifiers:
    print(f"Current: {commune_identifier}")
    ProbabilityTable.generate(
        commune_identifier, candidate_name, probability_threshold)
    ProbabilityPoint.generate(
        commune_identifier, candidate_name, probability_threshold)

view(district, candidate_name, probability_threshold)
