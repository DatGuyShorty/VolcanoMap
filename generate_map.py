from bs4 import BeautifulSoup
import requests
import pandas
import folium
from folium import plugins

html = """
<b>Volcano name:</b><br>
<a href="https://www.google.com/search?q=%s" target="_blank">%s</a><br> 
<a href="https://en.wikipedia.org/wiki/%s" target="_blank">%s</a><br>
%s
<b>Height: </b> %s m
<b>Type:</b> %s
<b>Status:</b> %s
"""
# https://www.google.com/search?q=%Valles%20Caldera%
#color deciding function
def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    elif 3000 < elevation :
        return "red"

def get_volcano_image_html(volcano_name):
    wiki_url = f"https://en.wikipedia.org/wiki/{volcano_name.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    res = requests.get(wiki_url, headers=headers)
    soup =  BeautifulSoup(res.text, "html.parser")
    #print("Wiki link: ", wiki_url) # prints wiki link 
        # Look for the infobox table
    infobox = soup.find("table", class_="infobox")
    if infobox is None:
        # No infobox → no image available
        return f"NO INFOBOX FOUND"
    
    img = soup.find("table", class_="infobox").find("img")
    if img:
        img_url = "https:" + img["src"]
        html = f'''
        <img src="{img_url}" alt="{volcano_name}" style="max-width:400px;"><br>
        '''
        return html
    else:
        return f'NO IMAGE FOUND'
    

    
map = folium.Map(location=[47.116386, -101.299591], zoom_start=4)
fg1 = folium.FeatureGroup(name="Low Volcanoes")
fg2 = folium.FeatureGroup(name="Medium Volcanoes")
fg3 = folium.FeatureGroup(name="High Volcanoes")
#variables
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])
vtype = list(data["TYPE"])
status = list(data["STATUS"])

total_entries = len(lat)
print("Num. volcanoes to process: ",total_entries)

#for each entry in zip() add marker to the fg group
for i, (lt, ln, nm, el, tp, st) in enumerate(zip(lat, lon, name, elev, vtype, status), start=1):

    img_src = get_volcano_image_html(nm)
    progress = (i / total_entries) * 100
    print("\033c")  # clear terminal
    print("Currently processing: ", nm) # Print volcano name
    print(i, "/", total_entries,"processed.",f"{progress:.2f}% done.") #Print progress
    # print("Img link: ", img_src) #Print img link

    #create iframe with html
    iframe = folium.IFrame(html=html % (nm, nm, nm, nm, img_src, el, tp, st), width=400, height=600)

    #create marker with location, popup and icon
    if el < 1000:    #Green markers
        fg1.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(
            iframe), icon=folium.Icon(color=color_producer(el),)))
    elif 1000 <= el < 3000:  #Orange markers
        fg2.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(
            iframe), icon=folium.Icon(color=color_producer(el),))) 
    elif 3000 <= el:  #Red markers
        fg3.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(
            iframe), icon=folium.Icon(color=color_producer(el),))) 
    
print("\033c")  # clear terminal
print(i, "/", total_entries,"processed.",f"{progress:.2f}% done.") #Print progress
#add_child to map
map.add_child(fg1) #add low volcanoes feature group
map.add_child(fg2) #add medium volcanoes feature group
map.add_child(fg3) #add high volcanoes feature group  
#minimap inicialization 
minimap = plugins.MiniMap()
map.add_child(minimap)
map.add_child(folium.LayerControl()) 

#save the map
map_name = "volcano_map.html"
map.save(map_name)
print("Processing finished!")
print("Map saved as:",map_name)
input("Finished! Press enter to close...")