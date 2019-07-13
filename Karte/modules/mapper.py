# -*- coding: utf-8 -*-
import folium.plugins as plugins
import folium
import os

'''
Diese Klasse reimplementiert die Foliumklasse Map.

Hier ein paar Beispiele:

    folium.Marker([45.3311, -121.7113], popup='<b>Timberline Lodge</b>', tooltip=tooltip).add_to(m)
 >>>  m.addMarker([45.3311, -121.7113], popup='<b>Timberline Lodge</b>', tooltip=tooltip)

    folium.Marker(location=[45.3300, -121.6823], popup='Some Other Location', icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
 >>>  m.addMarker(location=[45.3300, -121.6823], popup='Some Other Location', color='red', icon='info-sign')
'''

class Map(object):
    def __init__(self, location, zoom_start=0, tiles=None):
        self.map = folium.Map(location=location, tiles=tiles, zoom_start=zoom_start, detect_retina=True)
        self.feature_groups = {}

    def addMarkerCluster(self, feature_group):
        cluster = self.feature_groups[feature_group] = plugins.MarkerCluster(control=True, name=feature_group)
        self.map.add_child(cluster)

    def addFeatureGroup(self, feature_group):
        self.feature_groups[feature_group] = folium.FeatureGroup(name=feature_group)

    def addFeatureSubGroup(self, feature_group, parent, show=True):
        self.feature_groups[feature_group] = plugins.FeatureGroupSubGroup(self.feature_groups[parent], feature_group, show=show)
        self.map.add_child(self.feature_groups[feature_group])

    # ändert die Startlocation
    def location(self, location):
        self.map.location = location

    # Speichert die Map unter dem angegebenen Pfad
    def save(self, filename):
        self.map.save(filename)

    def addTileLayer(self, tiles, name=None, show=True, control=True, attr=None):
        folium.TileLayer(tiles=tiles, name=name, show=show, control=control, attr=attr).add_to(self.map)

    def activateLayerControl(self, position='topright', collapsed=True, autoZIndex=True):
        folium.LayerControl(position=position, collapsed=collapsed, autoZIndex=autoZIndex).add_to(self.map)

    def addMarker(self, location, tooltip=None, popup=False, icon=None, color='blue', prefix=None):
        marker = folium.Marker(
            location=location,
            tooltip=tooltip,
            popup=None if not popup else folium.Popup(html=popup, max_width='100%')
        )
        if icon != None:
            if prefix == None:
                marker.add_child(folium.Icon(icon=icon, color=color))
            else:
                marker.add_child(folium.Icon(icon=icon, color=color, prefix=prefix))
        marker.add_to(self.map)

    def addMarkerToFeatureGroup(self, feature_group, location, tooltip=None, popup=False, icon=None, color='blue', prefix=None):
        marker = folium.Marker(
            location=location,
            tooltip=tooltip,
            popup=None if not popup else folium.Popup(html=popup, max_width='100%')
        )
        if icon != None:
            if prefix == None:
                marker.add_child(folium.Icon(icon=icon, color=color))
            else:
                marker.add_child(folium.Icon(icon=icon, color=color, prefix=prefix))
        self.feature_groups[feature_group].add_child(marker)

    def addCircle(self, location, radius=50, popup=False, tooltip=None, color='blue', fillcolor=None):
        if color == None:
            print('ERROR: addCircle must define color, not None!')
        else:
            fill = True if fillcolor != None else False
            folium.Circle(
                location=location,
                radius=radius,
                tooltip=tooltip,
                popup=None if not popup else folium.Popup(html=popup, max_width='100%'),
                color=color,
                fill=fill,
                fill_color=fillcolor
            ).add_to(self.map)

    def addGeoJson(self, filename, name, show=True, control=True, tooltip=False, fields=[], aliases=[]):
        tooltip=folium.features.GeoJsonTooltip(fields=fields, aliases=aliases) if tooltip else None
        folium.GeoJson(
            os.path.join(filename),
            name=name,
            tooltip=tooltip,
            show=show,
            control=control
        ).add_to(self.map)
