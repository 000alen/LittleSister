from argparse import ArgumentParser

import LittleSister.Database as Database
from LittleSister.Probability import generate_probability_table, generate_probability_table_json, generate_probability_point

parser = ArgumentParser(
    "LittleSister",
    description="A framework to analyze chilean elections' data"
)

parser.add_argument(
    "--generate-database",
    action="store_true",
    help="starts the generate proccess for the database"
)

parser.add_argument(
    "--generate-point",
    action="store_true",
)

parser.add_argument(
    "--commune-identifier",
)

parser.add_argument(
    "--candidate-name",
)

parser.add_argument(
    "--probability-threshold",
    type=float
)

args = parser.parse_args()

if args.generate_database:
    Database.generate()
elif args.generate_point:
    print(args.probability_threshold)

    generate_probability_table(args.commune_identifier, args.candidate_name, args.probability_threshold)
    generate_probability_table_json(args.commune_identifier, args.candidate_name, args.probability_threshold)
    generate_probability_point(args.commune_identifier, args.candidate_name, args.probability_threshold)
