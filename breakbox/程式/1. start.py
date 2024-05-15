"""
The template of the main script of the machine learning process
"""
import json
import math
import random
import time
import os
class MLPlay:
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        self.ball_log = []
        self.ball_served = False
        self.x = []
        self.y = []
        self.time = time.time()

    def update(self, scene_info, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"
        else:               
            if len(self.y) < 2:
                if int(time.time() % 2) == 1:
                    command = "MOVE_RIGHT"
                else:
                    command = "MOVE_LEFT"
                self.x.append(scene_info["ball"][0])
                self.y.append(scene_info["ball"][1])
                
            elif self.y[0] >= self.y[1]:
                if int(time.time() % 2) == 1:
                    command = "MOVE_RIGHT"
                else:
                    command = "MOVE_LEFT"
                self.x = self.x[1:]  # 刪除第一個元素
                self.y = self.y[1:]  # 刪除第一個元素
                self.x.append(scene_info["ball"][0])
                self.y.append(scene_info["ball"][1])
            elif len(self.x) == 2:
                command = "MOVE_RIGHT"
                self.x = self.x[1:]  # 刪除第一個元素
                self.y = self.y[1:]  # 刪除第一個元素
                self.x.append(scene_info["ball"][0])
                self.y.append(scene_info["ball"][1])
                
                xx = (400 - float(scene_info["ball"][1])) / (math.sqrt(2) * float((self.y[1] - self.y[0])/(self.x[1] - self.x[0]))) +float(scene_info["ball"][0])
                

                            
                
                if xx > 400:
                    xxx = xx - 400
                elif xx > 200:
                    xxx = 400 - xx
                elif xx < -200:
                    xxx = xx + 400
                elif xx < 0:
                    xxx = -xx
                else:
                    xxx = xx
                if scene_info["platform"][0] + 20 != xxx:
                    if scene_info["platform"][0] + 20 > xxx:
                        command = "MOVE_LEFT"
                    elif scene_info["platform"][0] + 20 < xxx:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_NONE"
            if len(self.y) <= 1 or len(self.x) <= 1 or self.y[0] == self.y[1] or self.x[0] == self.x[1]:
                speed = 0
            else:
                speed = math.sqrt((self.y[1] - self.y[0] ) ** 2+ (self.x[1] - self.x[0]) ** 2)
            self.ball_log.append([scene_info['ball'][0], scene_info['ball'][1], speed, scene_info['platform'][0]])
            if scene_info['ball'][1] == 395 and scene_info['platform'][0] <= scene_info['ball'][0] and scene_info['platform'][0] + 40:

                log_folder = "C:\\Users\\gslab\\AppData\\Local\\paia_desktop\\app-2.6.0\\resources\\app.asar.unpacked\\games\\arkanoid\\log5"
                if not os.path.exists(log_folder):
                    os.makedirs(log_folder)
                    
                log_file_path = os.path.join(log_folder, f"{self.time}.json")

                try:
                    with open(log_file_path, "r", encoding='utf-8') as log_file:
                        log_data = json.load(log_file)
                except FileNotFoundError:
                    log_data = []

                log_data.append(self.ball_log)

                with open(log_file_path, "w", encoding='utf-8') as log_file:
                    json.dump(log_data, log_file, ensure_ascii=False, indent=4)      
                self.ball_log = []

                

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False