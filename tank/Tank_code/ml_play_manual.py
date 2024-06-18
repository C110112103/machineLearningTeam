import pygame
import math
import numpy as np
import os
import json
import time

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.side = ai_name
        print(f"Initial Game {ai_name} ml script")
        self.time = 0
        self.ai = None  # 初始化时没有AI对象
        self.P1_pre = None
        self.P2_pre = None
        self.P1_log = []
        self.P2_log = []

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        if scene_info["status"] != "GAME_ALIVE":
            print("exnd")
            if len(self.P1_log) != 0:
                log_folder = r"C:\Users\gslab\AppData\Local\paia_desktop\app-2.6.0\resources\app.asar.unpacked\games\TankMan\LOG"
                if not os.path.exists(log_folder):
                    os.makedirs(log_folder)
                    
                log_file_path = os.path.join(log_folder, f"{time.time()}.json")

                try:
                    with open(log_file_path, "r", encoding='utf-8') as log_file:
                        log_data = json.load(log_file)
                except FileNotFoundError:
                    log_data = []

                log_data = self.P1_log

                with open(log_file_path, "w", encoding='utf-8') as log_file:
                    json.dump(log_data, log_file, ensure_ascii=False, indent=4)
                self.P1_log = []
            return "RESET"
        
        if self.side == "1P":
            P1 = scene_info['teammate_info'][0]
            data = scene_info['oil_stations_info']

            max_x = data[0]
            for item in data:
                if item['x'] > max_x['x']:
                    max_x = item  
            
            P2 = max_x  

            if P1['oil'] < 30:
                data = scene_info['oil_stations_info']

                max_x = data[0]
                for item in data:
                    if item['x'] > max_x['x']:
                        max_x = item  
                        
                action = "oil"

                P2 = max_x  

            elif P1['power'] == 5:
                data = scene_info['bullet_stations_info']

                max_x = data[0]
                for item in data:
                    if item['x'] > max_x['x']:
                        max_x = item  

                action = "power"

                P2 = max_x      


            command = []
            if scene_info['power'] > 0:
                if abs(P1['x'] - P2['x']) > 5 or abs(P1['y'] - P2['y']) > 5:
                    if abs(P2['x'] - P1['x'])> 10:
                        # command = []
                        if P2['x'] - P1['x'] < 0:
                            turn = int((0 - P1['angle']) / 45)
                            if turn >= -4 and turn <= -1:
                                    command.append("TURN_RIGHT")
                            elif turn != 0:
                                    command.append("TURN_LEFT")
                            
                        elif P2['x'] - P1['x'] > 0:
                            turn = int((180 - P1['angle']) / 45)
                            if turn >= 1 and turn <= 4:
                                    command.append("TURN_LEFT")
                            elif turn != 0:
                                    command.append("TURN_RIGHT")
                                    
                        # if abs(P2['x'] - P1['x']) > 10:
                        #     command.append("FORWARD")
                                    
                    elif abs(P2['y'] - P1['y']) > 10:    
                        # command = []
                        if P2['y'] - P1['y'] < 0:
                            turn = int((270 - P1['angle']) / 45)
                            if turn >= 1 and turn <= 4:
                                    command.append("TURN_LEFT")
                            elif turn != 0:
                                    command.append("TURN_RIGHT")                      
                
                        elif P2['y'] - P1['y'] > 0:
                            turn = int((90 - P1['angle']) / 45)
                            if turn >= -4 and turn <= -1:
                                    command.append("TURN_RIGHT")
                            elif turn != 0:
                                    command.append("TURN_LEFT")     
                                    
                        # if abs(P2['y'] - P1['y']) > 10:              
                if (abs(P1['x'] - P2['x']) > 5 or abs(P1['y'] - P2['y']) > 5) and len(command) == 0:
                    command.append("FORWARD")  
                # if len(command) == 2:
                #     del command[1]                        
            if P1['power'] > 5:
                command.append("SHOOT")
                
            action = np.array(command)
            action = action[-1]
            # print([[P1['x'], P1['y']], action, [P2['x'], P2['y']], P1['power']])
            self.P1_log.append([[P1['x'], P1['y']], action, [P2['x'], P2['y']], P1['power']])
            return command

        elif self.side == "2P":
            P2 = scene_info['teammate_info'][0]
            data = scene_info['oil_stations_info']

            max_x = data[0]
            for item in data:
                if item['x'] < max_x['x']:
                    max_x = item  

            P1 = max_x  

            if P2['oil'] < 30:
                data = scene_info['oil_stations_info']

                max_x = data[0]
                for item in data:
                    if item['x'] < max_x['x']:
                        max_x = item  

                P1 = max_x  

            elif P2['power'] == 5:
                data = scene_info['bullet_stations_info']

                max_x = data[0]
                for item in data:
                    if item['x'] < max_x['x']:
                        max_x = item  

                P1 = max_x      

            command = []
            if scene_info['power'] > 0:
                if abs(P2['x'] - P1['x']) > 5 or abs(P2['y'] - P1['y']) > 5:
                    if abs(P1['x'] - P2['x'])> 10:
                        # command = []
                        if P1['x'] - P2['x'] < 0:
                            turn = int((0 - P2['angle']) / 45)
                            if turn >= -4 and turn <= -1:
                                    command.append("TURN_RIGHT")
                            elif turn != 0:
                                    command.append("TURN_LEFT")
                            
                        elif P1['x'] - P2['x'] > 0:
                            turn = int((180 - P2['angle']) / 45)
                            if turn >= 1 and turn <= 4:
                                    command.append("TURN_LEFT")
                            elif turn != 0:
                                    command.append("TURN_RIGHT")
                                    
                        # if abs(P2['x'] - P1['x']) > 10:
                        #     command.append("FORWARD")
                                    
                    elif abs(P1['y'] - P2['y']) > 10:    
                        # command = []
                        if P1['y'] - P2['y'] < 0:
                            turn = int((270 - P2['angle']) / 45)
                            if turn >= 1 and turn <= 4:
                                    command.append("TURN_LEFT")
                            elif turn != 0:
                                    command.append("TURN_RIGHT")                      
                
                        elif P1['y'] - P2['y'] > 0:
                            turn = int((90 - P2['angle']) / 45)
                            if turn >= -4 and turn <= -1:
                                    command.append("TURN_RIGHT")
                            elif turn != 0:
                                    command.append("TURN_LEFT")     
                                    
                        # if abs(P2['y'] - P1['y']) > 10:              
                if (abs(P2['x'] - P1['x']) > 5 or abs(P2['y'] - P1['y']) > 5) and len(command) == 0:
                    command.append("FORWARD")  
                # if len(command) == 2:
                #     del command[1]                        
            if P2['power'] > 5:
                command.append("SHOOT")
            return command

    def reset(self):
        print(f"reset Game {self.side}")
        self.ai = None  # 重置AI对象
