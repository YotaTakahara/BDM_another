#!/bin/bash
#トークンを記述
token="RlnKEyvrk8XLX0O5jiojKIThQYkSd94EPDW0T2fmoWs"
#メッセージを送信
curl -X POST -H "Authorization: Bearer ${token}" -F "message = bakayarou" https://notify-api.line.me/api/notify