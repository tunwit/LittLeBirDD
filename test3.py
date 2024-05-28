import subprocess
from PIL import Image , ImageDraw
import pystray
import numpy as np
import ctypes
import asyncio
import os 
import sys
import winsound
import time

BOT_SCRIPT = 'main.py'
img=Image.open('profile\default.png').convert("RGB")
npImage=np.array(img)
h,w=img.size

alpha = Image.new('L', img.size,0)
draw = ImageDraw.Draw(alpha)
draw.pieslice([0,0,h,w],0,360,fill=255)

npAlpha=np.array(alpha)

npImage=np.dstack((npImage,npAlpha))

iconimage = Image.fromarray(npImage)

bot_thread = None

async def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def handleclick(icon,event):
    global bot_thread
    if str(event) == "Exit":
        if bot_thread:
            bot_thread.terminate()
        icon.stop()
    elif str(event) == "Start":
        bot_thread = subprocess.Popen([sys.executable, BOT_SCRIPT])
        icon.menu = started_menu
        winsound.PlaySound('audio\starting.wav',winsound.SND_FILENAME)
    elif str(event) == "Close":
        bot_thread.terminate()
        icon.menu = closed_menu
        winsound.PlaySound('audio\closing.wav',winsound.SND_FILENAME)
    elif str(event) == "Restart":
        bot_thread.terminate()
        time.sleep(1) #wait to make sure
        bot_thread = subprocess.Popen([sys.executable, BOT_SCRIPT])
        icon.menu = started_menu
        winsound.PlaySound('audio/restarting.wav',winsound.SND_FILENAME)
        
closed_menu = pystray.Menu(
    pystray.MenuItem("Start",handleclick),
    pystray.MenuItem("Exit",handleclick)
)

started_menu = pystray.Menu(
    pystray.MenuItem("Restart",handleclick),
    pystray.MenuItem("Close",handleclick),
    pystray.MenuItem("Exit",handleclick)
)

icon = pystray.Icon(name="LittLeBirDD",icon=iconimage,title="Example",menu=closed_menu)

icon.run()

