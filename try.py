#from sys import implementation
import pygame
import os 
import time
import subprocess
import signal


cmd="sudo python3 movie.py"
p=subprocess.Popen(cmd,shell=True,preexc_fn=os.setsid)
time.sleep(2.0)
os.killpg(os.getpid(p.pid),signal.SIGTERM)
#p.terminate()
#os.system("sudo python3 movie.py")
# pygame.mixer.init()
# pygame.mixer.music.load("4428468134896.mp3")
# pygame.mixer.music.play(5)