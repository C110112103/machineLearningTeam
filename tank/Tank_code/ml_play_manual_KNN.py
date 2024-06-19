import pygame
import math
import numpy as np
import os
import json
import time
import joblib

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
        self.scaler = joblib.load('scaler_model0619_1P.pkl')
        self.knn = joblib.load('knn_model_0619_1P.pkl')
        self.scaler2 = joblib.load('scaler_model0619_2P.pkl')
        self.knn2 = joblib.load('knn_model_0619_2P.pkl')

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        if scene_info["status"] != "GAME_ALIVE":
            print("exnd")

            self.P1_log = []
            self.P2_log = []
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
                
            self.P1_log = []
            self.P1_log.append([P1['x'], P1['y']] + [P2['x'], P2['y']] + [P1['power']])

            X_test = np.array(self.P1_log)

            # 特徵縮放
            X_test_scaled = self.scaler.transform(X_test)

            # 使用模型進行預測
            y_pred = self.knn.predict(X_test_scaled)                                              
            command.append(y_pred[-1])
            print(y_pred)
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
       
            self.P2_log = []
            self.P2_log.append([P2['x'], P2['y']] + [P1['x'], P1['y']] + [P2['power']])
            
            X_test = np.array(self.P2_log)

            # 特徵縮放
            X_test_scaled = self.scaler.transform(X_test)

            # 使用模型進行預測
            y_pred = self.knn.predict(X_test_scaled)                                              
            command.append(y_pred[-1])                 
            
            return command

    def reset(self):
        print(f"reset Game {self.side}")
        self.ai = None  # 重置AI对象