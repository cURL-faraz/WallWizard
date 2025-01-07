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