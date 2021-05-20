from LittleSister.Probability import (
    generate_probability_table,
    generate_probability_table_json,
    generate_probability_point
)
from LittleSister import districts_path
from json import load

district = 10
candidate_name = "GONZALO WINTER ETCHEBERRY"
probability_threshold = 0.03

districts = load(open(districts_path, encoding="utf-8"))
communes_identifiers = districts[str(district)]

for commune_identifier in communes_identifiers:
    print(commune_identifier)

    generate_probability_table(
        commune_identifier, candidate_name, probability_threshold)
    generate_probability_table_json(
        commune_identifier, candidate_name, probability_threshold)
    generate_probability_point(
        commune_identifier, candidate_name, probability_threshold)
