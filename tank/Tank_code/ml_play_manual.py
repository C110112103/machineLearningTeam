import pygame
import math



class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        self.side = ai_name
        print(f"Initial Game {ai_name} ml script")
        self.time = 0
        self.ai = None  # 初始化时没有AI对象
        self.P1_pre = None
        self.P2_pre = None

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        
        if self.side == "1P":
            P1 = scene_info['teammate_info'][0]
            P2 = scene_info['oil_stations_info'][1]
            command = []
            if scene_info['power'] > 0:
                if abs(P1['x'] - P2['x']) > 25 or abs(P1['y'] - P2['y']) > 25:
                    if abs(P2['x'] - P1['x']) - abs(P2['y'] - P1['y']) > 0:
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
                                    
                    elif abs(P2['y'] - P1['y']) > 25:    
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
                if abs(P1['x'] - P2['x']) > 25 or abs(P1['y'] - P2['y']) > 25:
                    command.append("FORWARD")                                 
                    
            
            if self.P1_pre == None:
                command = []
                command.append("SHOOT")
                command.append("SHOOT")
                command.append("SHOOT")
                command.append("SHOOT")
                command.append("SHOOT")
                self.P1_pre = True
                
            return command

        elif self.side == "2P":
            command = []
            if pygame.K_d in keyboard:
                command.append("TURN_RIGHT")
            elif pygame.K_a in keyboard:
                command.append("TURN_LEFT")
            elif pygame.K_w in keyboard:
                command.append("FORWARD")
            elif pygame.K_s in keyboard:
                command.append("BACKWARD")

            if pygame.K_f in keyboard:
                command.append("SHOOT")

            if not command:
                command.append("NONE")
            print(command)
            return command

    def reset(self):
        print(f"reset Game {self.side}")
        self.ai = None  # 重置AI对象
