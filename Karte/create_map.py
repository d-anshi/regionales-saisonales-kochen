# -*- coding: utf-8 -*-
import modules.data as data
import modules.mapper as mapper
from modules.data import *

#-----------------------------
# Grundvariablen
infolink   = "https://server/info.html?link="
recipelink = "https://server/rezepte.html?link="

# ------- Erstelle Map -------
# >>>>> Alle Früchte
map = mapper.Map([51.21068269320044, 6.744983196258545], zoom_start=13) # wenn du TileLayer hinzufügst, kannst du hier den tiles Param entfernen

# Füge Tiles hinzu (Anzeigevarianten)
map.addTileLayer('stamenwatercolor',   'Wasserfarbe')
map.addTileLayer('openstreetmap',      'Karte')
map.addTileLayer('stamentoner',        'Raster')

# Füge Stadtteile von Düsseldorf hinzu
# Datensatz von Open Data Düsseldorf
#map.addGeoJson('..\\data\\geojson\\Stadtteile_WGS84_4326.geojson', 'Stadtteile Düsseldorf', tooltip=True, fields=['Name'], aliases=['Name:'], show=True, control=False)

# Erzeuge Jahreszeiten Cluster
# >>>>> Hier nur Sommer und Herbst, da wir keine Früchte für Frühling oder Winter haben
#map.addMarkerCluster("Frühling")
map.addMarkerCluster("Sommer")
map.addMarkerCluster("Herbst")
#map.addMarkerCluster("Winter")

# ------- Datensätze -------
# var = create_geojson(name, source, destination)
template = create_geojson("Frucht X", "..\\Daten\\source\\Template.csv", '..\\data\\geojson\\template.geojson')

# Füge Fruchtdaten hinzu
# Farben: 'lightred', 'white', 'lightgrayblack', 'lightblue',
#         'darkblue', 'orange', 'gray', 'red', 'lightgreen',
#         'darkred', 'purple', 'beige', 'cadetblue', 'blue',
#         'darkpurple', 'darkgreen', 'pink', 'green'}
create_geojson_markers(template, map, 'Frucht_X', 'fa', 'leaf', 'green', recipelink=recipelink, infolink=infolink, infofruit="Frucht X", season="Sommer", show=True)

# Aktiviere das Kontrollmenü
map.activateLayerControl()

# Speichere Map
map.save('output/saisonales-regionales-kochen.html')
