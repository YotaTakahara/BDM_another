# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import argparse
import cv2
# import strip




#出発駅の入力
departure_station = input("出発駅を入力してください：")
#到着駅の入力
destination_station = input("到着駅を入力してください：")

#経路の取得先URL
route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station
print(route_url)
#Requestsを利用してWebページを取得する
route_response = requests.get(route_url)

# BeautifulSoupを利用してWebページを解析する
route_soup = BeautifulSoup(route_response.text, 'html.parser')

#経路のサマリーを取得
route_summary = route_soup.find("div",class_ = "routeSummary")
#所要時間を取得
required_time = route_summary.find("li",class_ = "time").get_text()
#乗り換え回数を取得
transfer_count = route_summary.find("li", class_ = "transfer").get_text()
#料金を取得
fare = route_summary.find("li", class_ = "fare").get_text()

print("======"+departure_station+"から"+destination_station+"=======")
print("所要時間："+required_time)
print(transfer_count)
print("料金："+fare)

#乗り換えの詳細情報を取得
route_detail = route_soup.find("div",class_ = "routeDetail")

#乗換駅の取得
stations = []
stations_tmp = route_detail.find_all("div", class_="station")
for station in stations_tmp:
    stations.append(station.get_text().strip())

#乗り換え路線の取得
lines = []
lines_tmp = route_detail.find_all("li", class_="transport")
for line in lines_tmp:
    line = line.find("div").get_text().strip()
    lines.append(line)

#路線ごとの所要時間を取得
estimated_times = []
estimated_times_tmp = route_detail.find_all("li", class_="estimatedTime")
for estimated_time in estimated_times_tmp:
    estimated_times.append(estimated_time.get_text())

print(estimated_times)

#路線ごとの料金を取得
fars = []
fars_tmp = route_detail.find_all("p", class_="fare")
for fare in fars_tmp:
    fars.append(fare.get_text().strip())


#乗り換え詳細情報の出力
print("======乗り換え情報======")
for station,line,estimated_time,fare in zip(stations,lines,estimated_times,fars):
    print(station)
    print( " | " + line + " " + estimated_time + " " + fare)



print(stations[0])
when=[]
for i in range(5):
    when.append(stations[0][i])
print(when)


dt=datetime.datetime.now()
l=str(dt).split()
tmp=l[1].split(':')
print(tmp)
check=0
print(stations)
print(stations[len(stations)-1])



cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
while True:
    ret,image=cap.read()
    # ミラー表示
    fps=(255,255,255)
    cv2.putText(image,'deisui',(10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, fps, 2, cv2.LINE_AA)
    cv2.imshow('camera',image)
    if when[0]==tmp[0][0] and when[1]==tmp[0][1] and when[3]==tmp[1][0] and when[4]==tmp[1][1]:
        print("oke")
        
        break
    # else:
        # print(when[0]==tmp[0][0])
        
        # print(when[1])
        # print(tmp[0][1])
        # print(when[3])
        # print(tmp[1][0])
        # print(when[4])
        # print(tmp[1][1])
        #print("no")    
    
    
