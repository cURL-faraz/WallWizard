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
    
    def clear_terminal(self,time):
        sleep(time)
        os.system('clear')

    def valid_moves(self,player,x,y):
        self.clear_terminal(1)
        self.table.print_table()
        print(f"[bold green]{player.name} please choose one of the valid moves below ![/bold green]")
        valid_moves=[]
        for move in self.table.table[x][y].neighbors.keys():
            if self.table.table[x][y].neighbors[move]:
                valid_moves.append(move)
                print(f"[bold green]{move}[/bold green]",end=" ")
        print()
        move = input()
        if move in valid_moves:
            return move
        else:
            print("[bold red1]oops ! invalid move is chosen .[/bold red1]")
            return self.valid_moves(player,x,y)
        
    def is_terminated(self,player):
        if player.pos_x == player.target_row:
            print(f"[bold green]{player.name} won the game ![/bold green]")
            return True
        else:
            return False 

    def update_position_ball_elimination(self,current_x,current_y,direction):
        lower_bound = 0 
        upper_bound = 16
        up_wall = (-1,0)
        down_wall = (1,0)
        right_wall = (0,1)
        left_wall = (0,-1)
        if direction in set(['U','D']):
            if direction == 'U':
                up_neighbor = (-2,0)
                if current_x > lower_bound and not self.table.table[current_x+up_wall[0]][current_y].is_blocking and self.table.table[current_x+up_neighbor[0]][current_y+up_neighbor[1]].containing_ball:
                    if current_x+up_neighbor[0] == lower_bound or self.table.table[current_x+up_neighbor[0]+up_wall[0]][current_y].is_blocking:
                        if current_y < upper_bound and not self.table.table[current_x+up_neighbor[0]][current_y+right_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction+'R')
                        if current_y > lower_bound and not self.table.table[current_x+up_neighbor[0]][current_y+left_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction+'L') 
                    else:
                        self.table.table[current_x][current_y].add_limit(direction*2)
            else:
                down_neighbor = (2,0) 
                if current_x < upper_bound and not self.table.table[current_x+down_wall[0]][current_y].is_blocking and self.table.table[current_x+down_neighbor[0]][current_y+down_neighbor[1]].containing_ball:
                    if current_x+down_neighbor[0] == upper_bound or self.table.table[current_x+down_neighbor[0]+down_wall[0]][current_y].is_blocking:
                        if current_y < upper_bound and not self.table.table[current_x+down_neighbor[0]][current_y+right_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction+'R')
                        if current_y > lower_bound and not self.table.table[current_x+down_neighbor[0]][current_y+left_wall[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit(direction+'L') 
                    else:
                        self.table.table[current_x][current_y].add_limit(direction*2)
        else:
            if direction == 'R':
                right_neighbor = (0,2)
                if current_y < upper_bound and not self.table.table[current_x][current_y+right_wall[1]].is_blocking and self.table.table[current_x+right_neighbor[0]][current_y+right_neighbor[1]].containing_ball:
                    if current_y+right_neighbor[1] == upper_bound or self.table.table[current_x][current_y+right_neighbor[1]+right_wall[1]].is_blocking:
                        if current_x > lower_bound and not self.table.table[current_x+up_wall[0]][current_y+right_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('U'+direction)
                        if current_x < upper_bound and not self.table.table[current_x+down_wall[0]][current_y+right_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('D'+direction) 
                    else:
                        self.table.table[current_x][current_y].add_limit(direction*2)
            else:
                left_neighbor = (0,-2)
                if current_y > lower_bound and not self.table.table[current_x][current_y+left_wall[1]].is_blocking and self.table.table[current_x+left_neighbor[0]][current_y+left_neighbor[1]].containing_ball:
                    if current_y+left_neighbor[1] == lower_bound or self.table.table[current_x][current_y+left_neighbor[1]+left_wall[1]]:
                        if current_x > lower_bound and not self.table.table[current_x+up_wall[0]][current_y+left_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('U'+direction)
                        if current_x < upper_bound and not self.table.table[current_x+down_wall[0]][current_y+left_neighbor[1]].is_blocking:
                            self.table.table[current_x][current_y].add_limit('D'+direction)
                    else:
                        self.table.table[current_x][current_y].add_limit(direction*2)