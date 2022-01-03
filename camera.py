import datetime
from picamera import PiCamera
from time import sleep


camera=PiCamera()
camera.start_preview()
sleep(5)
camera.capture('line_photo/new.jpg')
camera.stop_preview()
