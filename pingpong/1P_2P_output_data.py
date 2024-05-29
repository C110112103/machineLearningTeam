import pickle
import os
import pygame
import time
import json
class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.ball_served = False
        self.side = ai_name
        self.action = []
        self.ball_position = []
        self.x = []
        self.y = []
        self.x_2P = []
        self.y_2P = []
        self.Log_1P = []
        self.Log_2P = []
        self.collision = 0
        
    def update(self, scene_info, keyboard=[], *args, **kwargs):
        if self.side == '1P':
            if scene_info['status'] != "GAME_ALIVE":
                with open(os.path.join(os.path.dirname(__file__), 'feature.pickle'), 'wb') as f:
                    pickle.dump(self.ball_position, f)
                with open(os.path.join(os.path.dirname(__file__), 'target.pickle'), 'wb') as f:
                    pickle.dump(self.action, f)
                self.Log_1P = [] 
                self.Log_2P = [] 
                return "RESET"
            if not self.ball_served:
                self.ball_served = True
                self.Log_1P = [] 
                self.Log_2P = [] 
                return "SERVE_TO_RIGHT"
            else:
                if len(self.y) < 2:
                    if int(time.time() % 2) == 1:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_LEFT"
                    self.x.append(scene_info["ball"][0])
                    self.y.append(scene_info["ball"][1])
                    self.x.append(scene_info["ball"][0])
                    self.y.append(scene_info["ball"][1])
                    
                elif self.y[0] >= self.y[1]:
                    self.Log_1P.append([scene_info["ball"][0], scene_info["ball"][1], scene_info["blocker"][0], scene_info["blocker"][1], scene_info["platform_1P"][0]])
                    
                    if scene_info["platform_1P"][0] + 20 > 100:
                        command = "MOVE_LEFT"
                    elif scene_info["platform_1P"][0] + 20 < 100:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_NONE"
                    self.x = self.x[1:]  # 刪除第一個元素
                    self.y = self.y[1:]  # 刪除第一個元素
                    self.x.append(scene_info["ball"][0])
                    self.y.append(scene_info["ball"][1])
                elif len(self.x) == 2:
                    self.Log_1P.append([scene_info["ball"][0], scene_info["ball"][1], scene_info["blocker"][0], scene_info["blocker"][1], scene_info["platform_1P"][0]])
                    command = "MOVE_RIGHT"
                    self.x = self.x[1:]  # 刪除第一個元素
                    self.y = self.y[1:]  # 刪除第一個元素
                    self.x.append(scene_info["ball"][0])
                    self.y.append(scene_info["ball"][1])
                    
                    # xx = (400 - float(scene_info["ball"][1])) / (math.sqrt(2) * float((self.y[1] - self.y[0])/(self.x[1] - self.x[0]))) +float(scene_info["ball"][0])
                    if self.x[1] == self.x[0] or self.y[1] == self.y[0]:
                        xx = (420 - float(scene_info["ball"][1])) / 1 +float(scene_info["ball"][0])
                    else:
                        xx = (420 - float(scene_info["ball"][1])) / (float((self.y[1] - self.y[0])/(self.x[1] - self.x[0]))) +float(scene_info["ball"][0])
                    

                                
                    
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
                    if scene_info["platform_1P"][0] + 20 != xxx:
                        if scene_info["platform_1P"][0] + 20 > xxx:
                            command = "MOVE_LEFT"
                        elif scene_info["platform_1P"][0] + 20 < xxx:
                            command = "MOVE_RIGHT"
                        else:
                            command = "MOVE_NONE"
                            
                    if scene_info['ball'][1] == 415 and scene_info['platform_1P'][0] <= scene_info['ball'][0] and scene_info['platform_1P'][0] + 80 >= scene_info['ball'][0] and len(self.x) > 1:

                        log_folder = "C:\\Users\\gslab\\Desktop\\PAIA\\1P_trainning"
                        if not os.path.exists(log_folder):
                            os.makedirs(log_folder)
                            
                        log_file_path = os.path.join(log_folder, f"{time.time()}.json")

                        try:
                            with open(log_file_path, "r", encoding='utf-8') as log_file:
                                log_data = json.load(log_file)
                        except FileNotFoundError:
                            log_data = []

                        log_data = self.Log_1P

                        with open(log_file_path, "w", encoding='utf-8') as log_file:
                            json.dump(log_data, log_file, ensure_ascii=False, indent=4)      
                        self.Log_1P = []                                                            
                        self.collision = 1                                                
                return command
        else:
            if scene_info['status'] != "GAME_ALIVE":
                self.Log_1P = []
                self.Log_2P = []
                return "RESET"
            if not self.ball_served:
                self.Log_1P = []
                self.Log_2P = []
                self.ball_served = True
                return "SERVE_TO_RIGHT"
            else:
                if len(self.y_2P) < 2:
                    if int(time.time() % 2) == 1:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_LEFT"
                    self.x_2P.append(scene_info["ball"][0])
                    self.y_2P.append(scene_info["ball"][1])
                    self.x_2P.append(scene_info["ball"][0])
                    self.y_2P.append(scene_info["ball"][1])
                    
                elif self.y_2P[0] <= self.y_2P[1]:
                    self.Log_2P.append([scene_info["ball"][0], scene_info["ball"][1], scene_info["blocker"][0], scene_info["blocker"][1], scene_info["platform_2P"][0]])
                    
                    if scene_info["platform_2P"][0] + 20 > 100:
                        command = "MOVE_LEFT"
                    elif scene_info["platform_2P"][0] + 20 < 100:
                        command = "MOVE_RIGHT"
                    else:
                        command = "MOVE_NONE"
                    self.x_2P = self.x_2P[1:]  # 刪除第一個元素
                    self.y_2P = self.y_2P[1:]  # 刪除第一個元素
                    self.x_2P.append(scene_info["ball"][0])
                    self.y_2P.append(scene_info["ball"][1])
                elif len(self.x_2P) == 2:
                    self.Log_2P.append([scene_info["ball"][0], scene_info["ball"][1], scene_info["blocker"][0], scene_info["blocker"][1], scene_info["platform_2P"][0]])
                    command = "MOVE_RIGHT"
                    self.x_2P = self.x_2P[1:]  # 刪除第一個元素
                    self.y_2P = self.y_2P[1:]  # 刪除第一個元素
                    self.x_2P.append(scene_info["ball"][0])
                    self.y_2P.append(scene_info["ball"][1])
                    
                    # xx = (400 - float(scene_info["ball"][1])) / (math.sqrt(2) * float((self.y[1] - self.y[0])/(self.x[1] - self.x[0]))) +float(scene_info["ball"][0])
                    if self.x_2P[1] == self.x_2P[0] or self.y_2P[1] == self.y_2P[0]:
                        xx = (80 - float(scene_info["ball"][1])) / 1 +float(scene_info["ball"][0])
                    else:
                        xx = (80 - float(scene_info["ball"][1])) / (float((self.y_2P[1] - self.y_2P[0])/(self.x_2P[1] - self.x_2P[0]))) +float(scene_info["ball"][0])
                    

                                
                    
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
                    if scene_info["platform_2P"][0] + 20 != xxx:
                        if scene_info["platform_2P"][0] + 20 > xxx:
                            command = "MOVE_LEFT"
                        elif scene_info["platform_2P"][0] + 20 < xxx:
                            command = "MOVE_RIGHT"
                        else:
                            command = "MOVE_NONE"
                            
                    if scene_info['ball'][1] == 80 and scene_info['platform_2P'][0] <= scene_info['ball'][0] and scene_info['platform_2P'][0] + 80 >= scene_info['ball'][0] and len(self.Log_2P) > 1:

                        log_folder = "C:\\Users\\gslab\\Desktop\\PAIA\\2P_trainning"
                        if not os.path.exists(log_folder):
                            os.makedirs(log_folder)
                            
                        log_file_path = os.path.join(log_folder, f"{time.time()}.json")

                        try:
                            with open(log_file_path, "r", encoding='utf-8') as log_file:
                                log_data = json.load(log_file)
                        except FileNotFoundError:
                            log_data = []

                        log_data = self.Log_2P

                        with open(log_file_path, "w", encoding='utf-8') as log_file:
                            json.dump(log_data, log_file, ensure_ascii=False, indent=4)      
                        self.Log_2P = []                                                            
                return command
    def reset(self):
        self.ball_served = False
