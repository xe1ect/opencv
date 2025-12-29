from mss import mss
from ultralytics import YOLO
import numpy as np
import cv2 as cv
import pydirectinput as pydirect
import time


class TheForge:
    def __init__(self,model_path):
        self.model = YOLO(model_path)
        self.sct = mss()
        self.monitor = {"top": 100, "left": 100, "width": 800, "height": 600}
        self.center_x =  self.monitor["width"] //2
        
        pydirect.PAUSE = 0.0
        pydirect.FAILSAFE = False
        
        self.is_mining = False
        self.minining_start = 0
        self.minining_duration = 5  
        
        
    def capture_screen(self):
        screenshot = np.array(self.sct.grab(self.monitor))
        return cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)
    
    def move_to_target(self,target_x):
        if target_x < self.center_x - 50:#ไปซ้าย
            pydirect.keyDown('a')
            pydirect.keyUp('d')
        elif target_x > self.center_x + 50:#ไปขวา
            pydirect.keyDown('d')
            pydirect.keyUp('a')
        else:
            pydirect.keyUp('a')
            pydirect.keyUp('d')
            
    def stop(self):
        pydirect.keyUp('a')
        pydirect.keyUp('d')
        pydirect.keyUp('w')
        
    def run(self):
        try:
            while True:
                frame = self.capture_screen()
                if self.is_mining:
                    elasepased_time = time.time() - self.minining_start
                    time_left = self.minining_duration - elasepased_time
                    if elasepased_time < self.minining_duration:
                        cv.putText(frame, f"MINING... {time_left:.1f}", (50, 50), 
                                   cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    else:
                        pydirect.mouseUp()
                        self.is_mining = False
                        self.stop()
                        
                results = self.model(frame,verbose=False,conf=0.5)
                result = results[0]
                best_box = None
                max_confidence = 0.0
            
                found = False
                for box in result.boxes:
                    
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])
                    if class_name == "rock":
                        found = True
                        x1, y1, x2, y2 = map(int,box.xyxy[0])

                        cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,255),2)
                        cv.putText(frame,f"{class_name} {confidence:.2f}",(x1,y1-10),cv.FONT_HERSHEY_SIMPLEX,0.9,(0,255,255),2)
                        
                        if confidence >= max_confidence:
                            max_confidence = confidence
                            best_box = box
                            
                        
                if best_box is not None:
                    x1, y1, x2, y2 = map(int,best_box.xyxy[0])

                    best_cls = int(best_box.cls[0])
                    best_name = self.model.names[best_cls]
                    best_conf = float(best_box.conf[0])
                    
                    cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv.putText(frame,f"{class_name} {confidence:.2f}",(x1,y1-10),cv.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
                    
                    target_x = (x1 + x2) // 2
                    box_height = y2 - y1
                    if box_height < 150:
                        self.move_to_target(target_x)
                        pydirect.keyDown('w')
                    else:
                        pydirect.keyUp('w')
                        self.move_to_target(target_x)
                        self.stop()
                        
                        pydirect.mouseDown()
                        
                        self.is_mining = True
                        self.minining_start = time.time()
    
                if not found:
                    self.stop()
                
                cv.imshow("The Forge",frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            self.stop()
            cv.destroyAllWindows()
            
bot = TheForge('runs/detect/TheForgeV12/weights/best.pt')

bot.run()