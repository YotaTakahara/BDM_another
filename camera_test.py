import cv2
import datetime
import os
import subprocess
import folium
import requests


geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
data = requests.get(geo_request_url).json()
print(data['latitude'])
print(data['longitude'])
map = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=18)
folium.Marker(location=[data['latitude'], data['longitude']]).add_to(map)

map.save("result.html")





camera = cv2.VideoCapture(0)
ret,frame=camera.read()
# cv2.imshow("Frame", frame)
alochol=datetime.datetime.now()
cv2.imwrite('line_photo/alochol.jpg',frame)


os.system("./linestamp1.sh alochol.jpg")
