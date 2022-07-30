
import pandas
import geopy
import folium
from folium import plugins



html = """
<b>Volcano name:</b><br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
<img src="https://www.google.com/search?tbm=isch&q=%s">
<b>Height: </b> %s m
<b>Type:</b> %s
"""

#color deciding function
def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    elif 3000 <= elevation < 5000:
        return "red"


map = folium.Map(location=[47.116386, -101.299591], zoom_start=4)
fg = folium.FeatureGroup(name="Volcanoes") 
#variables
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])
vtype = list(data["TYPE"])

#for each entry in zip() add marker to the fg group
for lt, ln, nm, el, tp in zip(lat, lon, name, elev, vtype):
    iframe = folium.IFrame(html=html % (nm, nm,nm, el, tp), width=200, height=100)
    fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(
        iframe), icon=folium.Icon(color=color_producer(el),)))

#add_child to map
map.add_child(fg)
#minimap inicialization 
minimap = plugins.MiniMap()
map.add_child(minimap)
map.add_child(folium.LayerControl()) 
#save the map
map.save("map1.html")
