#!/bin/bash
# -*- coding: utf-8 -*-
#日付とファイル名
date_photo=$1
photo_file="line_photo/${date_photo}"
token="RlnKEyvrk8XLX0O5jiojKIThQYkSd94EPDW0T2fmoWs"
#解像度の設定
#raspistill -w 1280 -h 1024 -o $photo_file
#写真を撮影してスタンプも送信
curl -X POST -H "Authorization: Bearer ${token}" -F "message = I'm drunk!! Pick me up!!! " -F "stickerPackageId = 6136" -F "stickerId = 10551376" -F "imageFile=@${photo_file}"  -F "imageFile=@${photo_file}" https://notify-api.line.me/api/notify
#xdg-open result.html
check="line_photo/file_name.jpg"

scrot  line_photo/file_name.jpg -d 5

curl -X POST -H "Authorization: Bearer ${token}" -F "message = I'm here !!!!!!!!! "  -F "imageFile=@${check}" https://notify-api.line.me/api/notify
#curl -X POST -H "Authorization: Bearer ${token}"  -F "imageFile=@${photo_file}" https://notify-api.line.me/api/notify