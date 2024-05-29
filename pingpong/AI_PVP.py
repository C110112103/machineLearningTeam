import pickle
import os
import pygame
import time
import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib

class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.ball_served = False
        self.side = ai_name
        self.action = []
        self.ball_position = []
        self.x = []
        self.y = []
        self.Log_1P = []
        self.Log_2P = []
        self.collision = 0
        
        all_data = []
        folder_path = "C:\\Users\\gslab\\Desktop\\PAIA\\1P_trainning"
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    all_data.extend(data)
  
        data_array = np.array(all_data)        
        first_4 = data_array[:, :-1]
        last_1 = data_array[:, -1]
        self.knn = KNeighborsClassifier(n_neighbors=2)
        self.knn.fit(first_4, last_1)
        
        all_data = []
        folder_path = "C:\\Users\\gslab\\Desktop\\PAIA\\2P_trainning"
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    all_data.extend(data)
  
        data_array = np.array(all_data)        
        first_4 = data_array[:, :-1]
        last_1 = data_array[:, -1]
        self.knn2P = KNeighborsClassifier(n_neighbors=2)
        self.knn2P.fit(first_4, last_1)        


    def update(self, scene_info, keyboard=[], *args, **kwargs):
        if self.side == '1P':
            if scene_info['status'] != "GAME_ALIVE":
                with open(os.path.join(os.path.dirname(__file__), 'feature.pickle'), 'wb') as f:
                    pickle.dump(self.ball_position, f)
                with open(os.path.join(os.path.dirname(__file__), 'target.pickle'), 'wb') as f:
                    pickle.dump(self.action, f)
                self.Log_1P = []
                return "RESET"
            if not self.ball_served:
                self.Log_1P = []
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else:
                self.Log_1P.append([scene_info["ball"][0], scene_info["ball"][1], scene_info["blocker"][0], scene_info["blocker"][1], scene_info["platform_1P"][0]])
                data_array = np.array(self.Log_1P)
                if data_array.shape[0] == 0:  # 確保有數據進行預測
                    return "MOVE_NONE"
                data_array = data_array[:, :-1]
                predicted_direction = self.knn.predict(data_array)
                if scene_info["platform_1P"][0] > int(predicted_direction[-1]):
                    command = "MOVE_LEFT"
                elif scene_info["platform_1P"][0] < int(predicted_direction[-1]):
                    command = "MOVE_RIGHT"
                else:
                    command = "MOVE_NONE"

                if scene_info['ball'][1] == 415:
                    self.Log_1P = []             
                    self.Log_2P = []      
                return command
        else:
            if scene_info['status'] != "GAME_ALIVE":
                return "RESET"
            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else:
                self.Log_2P.append([scene_info["ball"][0], scene_info["ball"][1], scene_info["blocker"][0], scene_info["blocker"][1], scene_info["platform_2P"][0]])
                data_array = np.array(self.Log_2P)
                if data_array.shape[0] == 0:  # 確保有數據進行預測
                    return "MOVE_NONE"
                data_array = data_array[:, :-1]
                predicted_direction = self.knn2P.predict(data_array)
                if scene_info["platform_2P"][0] > int(predicted_direction[-1]):
                    command = "MOVE_LEFT"
                elif scene_info["platform_2P"][0] < int(predicted_direction[-1]):
                    command = "MOVE_RIGHT"
                else:
                    command = "MOVE_NONE"

                if scene_info['ball'][1] == 80:
                    self.Log_1P = []             
                    self.Log_2P = []                     
                return command

    def reset(self):
        self.ball_served = False
