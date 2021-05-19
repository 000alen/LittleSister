import argparse

from LittleSister.Database import setup

parser = argparse.ArgumentParser(
    "LittleSister",
    description="A framework to analyze chilean elections' data"
)

parser.add_argument(
    "--setup-database", 
    action="store_true",
    help="starts the setup proccess for the database"
)

args = parser.parse_args()

if args.setup_database:
    setup()
