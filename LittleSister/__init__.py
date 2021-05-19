from pathlib import Path

database_path = Path("./database/")

communes_path = database_path / "communes.json"
districts_path = database_path / "districts.json"
pacts_path = database_path / "pacts.json"
parties_path = database_path / "parties.json"
candidates_per_district_path = database_path / "candidates_per_district.json"

census_path = database_path / "census/"
census_json_path = census_path / "census.json"

deputies_path = database_path / "deputies.csv"

if not database_path.is_dir():
    raise Exception("The database/ folder does not exist")

if not communes_path.is_file():
    raise Exception("The database/communes.json file does not exist")

if not districts_path.is_file():
    raise Exception("The database/districts.json file does not exist")

if not pacts_path.is_file():
    raise Exception("The database/pacts.json file does not exist")

if not parties_path.is_file():
    raise Exception("The database/parties.json file does not exist")

if not candidates_per_district_path.is_file():
    raise Exception(
        "The database/candidates_per_district.json file does not exist")

if not census_path.is_dir():
    raise Exception("The database/census/ folder does not exist")

if not census_json_path.is_file():
    raise Exception("The database/census/census.json file does not exist")

if not deputies_path.is_file():
    raise Exception("The database/deputies.csv file does not exist")
