#!/bin/bash
# -*- coding: utf-8 -*-
#日付とファイル名
date=$(date +"%Y-%m-%d_%H%M")
photo_file="line_photo/${date}.jpg"
token="RlnKEyvrk8XLX0O5jiojKIThQYkSd94EPDW0T2fmoWs"
#解像度の設定
raspistill -w 1280 -h 1024 -o $photo_file
#写真を撮影してスタンプも送信
curl -X POST -H "Authorization: Bearer ${token}" -F "message = Message from RasPi" -F "stickerPackageId = 6136" -F "stickerId = 10551376" -F "imageFile=@${photo_file}" https://notify-api.line.me/api/notify