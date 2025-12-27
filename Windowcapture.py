import cv2 as cv
import pyautogui as pag
import pygetwindow as gw
import time
import keyboard
import os

folder_path = "Resources" #Fodlerpath
check = 1

RobloxWindow = gw.getWindowsWithTitle("Roblox")[0]
    
while check == 1:
    if RobloxWindow.isMinimized:#ถ้าย่อให้เด้งมา
        RobloxWindow.restore()
        
    RobloxWindow.activate() #ให้อยู่หน้าสุด

    if keyboard.is_pressed("f"):
        x, y, width, height = RobloxWindow.left, RobloxWindow.top, RobloxWindow.width, RobloxWindow.height
        filename = f"TheForge_{int(time.time())}.png"
        full_path = os.path.join(folder_path, filename)
        screenshot = pag.screenshot(full_path,region=(x,y,width,height))
        cv.imread(full_path)
        cv.imshow("Screenshot",full_path)
        
        print("บันทึกเรียบร้อย")
    
    if keyboard.is_pressed("/"):
        check = 0
        print("ออกโปรเเกรม")
        
        