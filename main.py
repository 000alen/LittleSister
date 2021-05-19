from LittleSister.Probability import (
    generate_probability_table, 
    generate_probability_table_json, 
    generate_probability_point
)
from LittleSister import communes_path
from json import load

commune_name = "SANTIAGO"
candidate_name = "GONZALO WINTER ETCHEBERRY"
probability_threshold = 0

communes = load(open(communes_path, encoding="utf-8"))


def get_commune_identifier(commune_name):
    for identifier, name in communes.items():
        if name == commune_name:
            return identifier


commune_identifier = get_commune_identifier(commune_name)
print(commune_identifier)

generate_probability_table(commune_identifier, candidate_name, probability_threshold)
generate_probability_table_json(commune_identifier, candidate_name, probability_threshold)
generate_probability_point(commune_identifier, candidate_name, probability_threshold)
