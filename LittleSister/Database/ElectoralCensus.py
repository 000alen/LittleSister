import LittleSister.Database as Database


class ElectoralCensus(Database.Database):
    path = Database.path / "ElectoralCensus/"
    json_path = path / "ElectoralCensus.json"

    header = [
        "RUT",
        "DV",
        "Proper RUT",
        "Nombre completo",
        "Primer nombre",
        "Segundo nombre",
        "Primer apellido",
        "Segundo apellido",
        "Sexo",
        "Domicilio",
        "Circunscripcion",
        "Local?",
        "Mesa",
        "Pueblo",
    ]
