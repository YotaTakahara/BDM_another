import folium
import requests
import os
import subprocess
geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
data = requests.get(geo_request_url).json()
print(data['latitude'])
print(data['longitude'])
map = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=18)
folium.Marker(location=[data['latitude'], data['longitude']]).add_to(map)
map.save("result.html")
#os.system("xdg-open result.html")
subprocess.run(['xdg-open'],input='result.html')