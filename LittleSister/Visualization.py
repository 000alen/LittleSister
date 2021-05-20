import pandas
import geopandas
import folium
import folium.plugins
import json
import flask
import re

from LittleSister.Database import districts_path
from LittleSister.Database.ProbabilityPoint import ProbabilityPoint


def view(district, candidate_name, probability_threshold):
    app = flask.Flask(__name__)

    @app.route('/')
    def index():
        return folium_map._repr_html_()

    districts = json.load(open(districts_path, encoding="utf-8"))
    communes_identifiers = districts[str(district)]

    files_paths = [
        ProbabilityPoint.path / ProbabilityPoint.name_format.format(commune_identifier, re.sub(r" +", "_", candidate_name), probability_threshold)
        for commune_identifier in communes_identifiers
    ]

    dataframe = None
    for file_path in files_paths:
        if dataframe is None:
            dataframe = pandas.read_csv(file_path)
        else:
            dataframe = dataframe.append(pandas.read_csv(file_path))

    dataframe = dataframe[dataframe["probability"] != 0]
    geometry = geopandas.points_from_xy(dataframe.longitude, dataframe.latitude)
    geo_dataframe = geopandas.GeoDataFrame(dataframe["probability"], geometry=geometry)

    folium_map = folium.Map(location=[-33.4, -70.6], zoom_start=11)
    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in geo_dataframe.geometry]
    folium.plugins.HeatMap(heat_data, radius=10).add_to(folium_map)
    folium.plugins.FastMarkerCluster(heat_data).add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    # view.save("index.html")
    app.run()
