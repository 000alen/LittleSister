from argparse import ArgumentParser

import LittleSister.Database as Database
from LittleSister.Database.DeputiesProbabilityTable import DeputiesProbabilityTable
from LittleSister.Database.DeputiesProbabilityPoint import DeputiesProbabilityPoint

parser = ArgumentParser(
    "LittleSister",
    description="A framework to analyze chilean elections' data"
)

parser.add_argument(
    "--initialize-database",
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
    Database.initialize()
elif args.generate_point:
    DeputiesProbabilityTable.generate(args.commune_identifier, args.candidate_name, args.probability_threshold)
    DeputiesProbabilityPoint.generate(args.commune_identifier, args.candidate_name, args.probability_threshold)
