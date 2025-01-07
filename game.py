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
    
    def print_table(self):
        for i in range(17):
            for j in range(17):
                print(f"[{self.table[i][j].color}]{self.table[i][j].char}[/{self.table[i][j].color}]",end=" ")
            print()

class Player:
    def __init__(self,user_name,x,y,row,player_color):
        self.name = user_name 
        self.pos_x = x 
        self.pos_y = y
        self.target_row = row 
        self.color = player_color
        self.num_wall = 10 
        self.num_wall_per_turn = 128
        
    def change_pos(self,delta_x,delta_y):
        self.pos_x += delta_x
        self.pos_y += delta_y

class Game:
    def __init__(self,game_id,user_1,user_2):
        self.id=game_id
        self.table = Table() 
        self.is_finished = False
        self.first_player = Player(user_1,0,8,16,"bold magenta")
        self.second_player = Player(user_2,16,8,0,"bold bright_cyan")
        self.turn = 0 
        self.time = 0
        self.moves = {'U' : (-2,0) , 'R' : (0,2) , 'D' : (2,0) , 'L' : (0,-2) , 'UU' : (-4,0) , 'RR' : (0,4) , 
        'DD' : (4,0) , 'LL' : (0,-4) , 'UL' : (-2,-2) , 'UR' : (-2,2) , 'DR' : (2,2) , 'DL' : (2,-2)}
        self.is_putting_wall_possilble = True