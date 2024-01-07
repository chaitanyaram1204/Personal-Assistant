# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 11:13:52 2023

@author: CHAITANYA
"""

import pyautogui
import os
import time

def play_song(song):
    os.system("spotify")
    time.sleep(5)
    pyautogui.hotkey('Ctrl', 'l')
    time.sleep(1)
    pyautogui.write(song, interval=0.1)
    
    for key in ['enter', 'pagedown', 'tab', 'enter', 'enter']:
        time.sleep(1.5)
        pyautogui.press(key)    
        
    