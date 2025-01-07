import os 
from rich import print
from time import sleep
import copy 

class Wall:
    def __init__(self,direction):
        self.is_blocking = False
        if direction == 'H':
            self.char = '-'
        elif direction == 'V':
            self.char = '|'
        self.color = "bold bright_white"
    def wall_activation(self):
        self.is_blocking = True
        self.color = "bold bright_yellow"

class Center:
    def __init__(self):
        self.is_activated = False 
        self.char = "o"
        self.direction = None
        self.color = "bold bright_white"
    def center_activation(self,direction):
        self.is_activated = True
        self.color = "bold bright_yellow"
        self.direction = direction

class Entry:
    def __init__(self):
        self.containing_ball = False 
        self.char = ' '
        self.color = "unknown"
        self.neighbors = {'U': True , 'R' : True , 'D' : True , 'L' : True , 'UU' : False , 'RR' : False , 'DD' : False , 'LL' : False ,
        'UL' : False , 'UR' : False , 'DR' : False , 'DL' : False }
    
    def moving_ball_to(self,player_color):
        self.containing_ball = True
        self.char = 'O'
        self.color = player_color
    
    def moving_ball_from(self):
        self.containing_ball = False 
        self.char = ' '
        self.color = "unknown"
    
    def add_limit(self,key):
        self.neighbors[key] = False 
    
    def del_limit(self,key):
        self.neighbors[key] = True

class Table:
    def __init__(self):
        self.table=[["" for _ in range(17)] for _ in range(17)] 
        for i in range(17):
            for j in range(17):
                if i%2 == 0 and j%2 == 0 :
                    self.table[i][j]=Entry()
                    if i == 0:
                        self.table[i][j].add_limit('U')
                    elif i == 16:
                        self.table[i][j].add_limit('D')
                    if j == 0 :
                        self.table[i][j].add_limit('L')
                    elif j == 16:
                        self.table[i][j].add_limit('R')
                elif i%2 == 0 and j%2 != 0:
                    self.table[i][j] = Wall('V')
                elif i%2 != 0 and j%2 == 0:
                    self.table[i][j] = Wall('H')
                else:
                    self.table[i][j] = Center()
        self.centers = set([(x,y) for x in range(1,16,2) for y in range(1,16,2)])