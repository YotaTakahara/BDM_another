#!/bin/bash
import cv2
import datetime
import os
import subprocess
import folium
import requests
import stat
from pathlib import Path
import webbrowser




geo_request_url = 'https://get.geojs.io/v1/ip/geo.json'
data = requests.get(geo_request_url).json()
print(data['latitude'])
print(data['longitude'])
map = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=18)
folium.Marker(location=[data['latitude'], data['longitude']]).add_to(map)

map.save("result.html")


url="file:///home/pi/Desktop/BDM_another/result.html"
webbrowser.open("https://www.google.co.jp")
c=webbrowser.open_new_tab("https://www.google.co.jp")
print(c)





camera = cv2.VideoCapture(0)
ret,frame=camera.read()
# cv2.imshow("Frame", frame)
alochol=datetime.datetime.now()
cv2.imwrite('line_photo/alochol.jpg',frame)
#os.system("xdg-open result.html")
os.system("./linestamp1.sh alochol.jpg")

