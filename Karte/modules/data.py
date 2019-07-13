# -*- coding: utf-8 -*-
import requests
import json
from datetime import date, datetime
import csv
import pyproj
import modules.mapper as mapper
import geojson
import datetime
import folium as folium

#-----------------------------
# CSV Modul
def read_csv(filename):
    with open(filename, "r+") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        data = []
        for line in csv_reader:
            data.append(line)
        return data

def dump_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)

def create_geojson(fruitname, infile, outfile):
    csv        = read_csv(infile)
    data       = []
    collection = {'features': {}}
    for line in csv:
        if line != None:
            coord = [0, 0]
            try:
                # Definiere Grid für Koordinatenumwandlung
                utm = pyproj.Proj(proj="utm",zone=line[1])
                dec = pyproj.Proj(init = "epsg:4326")
                # Wandle UTM Koordinaten um zu Lat/Long
                coord[1], coord[0] = pyproj.transform(utm, dec, line[2], line[3] )
            except:
                print(fruitname + ": Fehler beim Umwandeln der Koordinaten von UTM zu Lat/Long: ", line[2], line[3] + "\n")

            # Kreiere GeoJson
            properties = {
                "UTM Region":line[1],
                "X_Coord"   :line[2],
                "Y_Coord"   :line[3],
                #"Strschl":line[12],
                #"Straße":line[13],
                #"Hausnummer":line[14],
                #"Kennung":line[18],
                "Pflanzjahr":line[4],
                "Höhe":int(line[12]) if line[12] != "0" else "keine Angabe",
                "Baumumfang":int(line[30]) if line[30] != "0" else "keine Angabe",
                "Alter":int(datetime.datetime.now().year) - int(line[4]),
                "Name":fruitname,
                "Deutsch":line[10],
                "Gattung":line[7],
                "Art":line[8],
                "Sorte":line[9],
                #"Kürzel":line[6],
                "Reifezeit":line[11],
                #"Artenschutz":line[44],
            }
            print(str(properties) + "\n")

            point   = geojson.Point((coord[1], coord[0]))
            feature = geojson.Feature(geometry=point, id=line[0], properties=properties)
            data.append(feature)

        collection = geojson.FeatureCollection(data)

        # speichere in Datei
        dump_file(outfile, str(collection))
    return collection


def create_geojson_markers(geojson, map, feature_group, prefix=None, icon=None, color="blue", tooltip=None, popup=False, recipelink="", infolink="", infofruit="", season="Sommer", show=True):
    data = geojson

    # Kreiire Layer
    map.addFeatureSubGroup(feature_group, season, show=show)

    for feature in data["features"]:
        lon, lat = feature["geometry"]["coordinates"]

        # Popup
        popup  = "<b>~ " + feature["properties"]["Name"] + " ( " + feature["properties"]["Gattung"] + " " + feature["properties"]["Art"] + " " + feature["properties"]["Sorte"] + ") ~</b>" + "<br><br>Pflanzjahr: " + str(feature["properties"]["Pflanzjahr"]) + "<br>Alter: " + str(feature["properties"]["Alter"]) + "<br>Höhe: " + str(feature["properties"]["Höhe"]) + "<br>Baumumfang: " + str(feature["properties"]["Baumumfang"]) + "<br>Reifezeit: " + season + "<br>___________________________________<br><a rel='noopener' target='_blank' href=" + infolink + infofruit + ">" + "Weitere Infos" + "</a> | <a rel='noopener' target='_blank' href=" + recipelink + feature["properties"]["Name"] + ">" + "Rezept" + "</a>"

        try:
            map.addMarkerToFeatureGroup(feature_group, [lat, lon], prefix=prefix, icon=icon, popup=popup, tooltip=feature["properties"]["Name"], color=color)
        except:
            print("Fehler bei der Platzierung des markers zu:\n", feature)
