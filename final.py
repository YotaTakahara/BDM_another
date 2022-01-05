#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse
import pygame
import time
import os
import subprocess
import cv2 as cv
import numpy as np
import mediapipe as mp
import requests
from bs4 import BeautifulSoup
import datetime
import argparse
import cv2

from utils import CvFpsCalc



departure_station=""
destination_station=""
when=[]
stations=[]

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)
    # parser.add_argument("--width", help='cap width', type=int, default=1200)
    # parser.add_argument("--height", help='cap height', type=int, default=600)

    parser.add_argument("--model_complexity",
                        help='model_complexity(0,1(default))',
                        type=int,
                        default=1)

    parser.add_argument("--max_num_hands", type=int, default=2)
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    parser.add_argument('--use_brect', action='store_true')
    parser.add_argument('--plot_world_landmark', action='store_true')

    args = parser.parse_args()

    return args


def station():
    
    global when
    global departure_station
    global destination_station

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
    global stations
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


def main():
    global when
    global stations
    # 引数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    model_complexity = args.model_complexity

    max_num_hands = args.max_num_hands
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = args.use_brect
    plot_world_landmark = args.plot_world_landmark

    station()
    # カメラ準備 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    

    while True:
        
        dt=datetime.datetime.now()
        l=str(dt).split()
        tmp=l[1].split(':')
       
        
        # カメラキャプチャ #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # ミラー表示
        debug_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        fps=(255,255,255)
        cv2.putText(debug_image,str(stations[0])+"から"+str(stations[len(stations)-1])+"\n"+"現在時刻: "+str(tmp)+"電車の時刻: "+str(when[0])+str(when[1])+str(when[2])+str(when[3])+str(when[3]),(10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, fps, 2, cv2.LINE_AA)
    
        if when[0]==tmp[0][0] and when[1]==tmp[0][1] and when[3]==tmp[1][0] and when[4]==tmp[1][1]:
            print("oke")
        
            break

        # 描画 ################################################################
       
       
        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv.imshow('MediaPipe Hand Demo', debug_image)

    cap.release()
    cv.destroyAllWindows()




if __name__ == '__main__':
    main()
