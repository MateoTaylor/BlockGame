import pygame
from random import choice

#Game Width
COLUMNS = 8
ROWS = 8
CELL_SIZE = 60
GAME_WIDTH, GAME_HEIGHT = COLUMNS*CELL_SIZE,ROWS*CELL_SIZE + 180

#Window Size
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + PADDING * 2
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 8

# Colors 
YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
GRAY = '#1C1C1C'
LINE_COLOR = '#FFFFFF'

BLOCK_OFFSET = pygame.Vector2(0,10*CELL_SIZE)

TETROMINO_WEIGHTS = [64,32,32,16,16,16,16,
                     4,4,4,4,4,4,4,4,4,4,4,4,16,8,8,4,4,4,4,
                     6,6,3,3,3,3,3,3,1]
TETROMINO_POPULATION = ['BS','5x1','1x5','BL','BLU','BJ','BJU',
    'J', 'L','JU','LU','LSW','JSW','LSU','JSU','T','TF','UDT','UDTF','SS','1x4','4x1','S','Z','Sup','Zup',
    '1x3','3x1','LL','LJ','LJU','LLU','2x1','1x2','1x1']

# shapes UD means Upside Down, xUP means turned vertically? idk lol, F means flipped horizontally?
TETROMINOS = {
    #Big Shapes
    'BS': {'shape': [(0,0), (0,-60), (-60,-60), (60,60),(0,60),(-60,0),(60,0), (60,-60),(-60,60)], 'color': YELLOW,
           'right': 60,'top':-60,'left':-60,'bottom':60}, #large shapes
    '5x1':{'shape':[(0,0),(-120,0),(-60,0),(60,0),(120,0)],'color': RED, 'right':120,'top':0,'bottom':0,'left':-120},
    '1x5':{'shape':[(0,0),(0,-120),(0,-60),(0,60),(0,120)],'color':RED,'right':0,'left':0,'top':-120,'bottom':120}, 

    'BL':{'shape':[(0,0),(-120,0),(-60,0),(0,-60),(0,-120)],'color': BLUE,'right':0,'top':-120,'bottom':0,'left':-120},
    'BLU':{'shape':[(0,0),(-120,-120),(-60,-120),(0,-60),(0,-120)],'color': BLUE,'right':0,'top':-120,'bottom':0,'left':-120},
    'BJ':{'shape':[(0,0),(120,0),(60,0),(0,-60),(0,-120)],'color': BLUE,'right':120,'top':-120,'bottom':0,'left':0},
    'BJU':{'shape':[(0,0),(120,-120),(60,-120),(0,-60),(0,-120)],'color': BLUE,'right':120,'top':-120,'bottom':0,'left':0},
    
    #Medium Shapes
    'J': {'shape': [(0,0), (0,-60), (0,60), (-60,60)], 'color': ORANGE, 'right': 0, 'top': -60,'left':-60,'bottom':60}, 
	'L': {'shape': [(0,0), (0,-60), (0,60), (60,60)], 'color': ORANGE,'right':60,'top':-60,'left':0,'bottom':60}, #upright J and S
    'JU':{'shape': [(0,0),(0,-60),(0,60),(-60,-60)],'color':ORANGE,'right':0 ,'top':-60,'bottom':60,'left':-60},
    'LU':{'shape': [(0,0),(0,-60),(0,60),(60,-60)],'color':ORANGE,'right':60,'top':-60,'bottom':60,'left':0},

    'LSW':{'shape': [(0,0),(-60,0),(60,0),(60,60)],'color':ORANGE,'right':60,'top':0,'bottom':60,'left':-60}, #J and S sideways
    'JSW':{'shape': [(0,0),(-60,0),(60,0),(-60,60)],'color':ORANGE,'right':60,'top':0,'bottom':60,'left':-60},
    'LSU':{'shape': [(0,0),(-60,0),(60,0),(60,-60)],'color':ORANGE,'right':60,'top':-60,'bottom':0,'left':-60},
    'JSU':{'shape': [(0,0),(-60,0),(60,0),(-60,-60)],'color':ORANGE,'right':60,'top':-60,'bottom':0,'left':-60},
    
    'T': {'shape': [(0,0), (-60,0), (60,0), (0,-60)], 'color': PURPLE, 'right': 60, 'top':-60,'left':-60,'bottom':0},
    'TF':{'shape': [(0,0),(-60,0),(60,0),(0,60)],'color':PURPLE,'right':60,'top':0,'bottom':60,'left':-60},
    'UDT':{'shape': [(0,0),(0,-60),(0,60),(-60,0)],'color':PURPLE,'right':0,'top':-60,'bottom':60,'left':-60},
    'UDTF': {'shape': [(0,0),(0,-60),(0,60),(60,0)],'color':PURPLE,'right':60,'top':-60,'bottom':60,'left':0},

    'SS':{'shape': [(0,0),(0,-60),(60,-60),(60,0)],'color': BLUE,'right': 60,'top':-60,'left':0,'bottom':0},
    
    '1x4': {'shape': [(0,0), (0,-60), (0,-120), (0,60)], 'color': CYAN,'right':0,'left':0,'bottom':60,'top':-120},
    '4x1': {'shape': [(0,0),(-60,0),(-120,0),(60,0)],'color':CYAN,'right':60,'left':-120,'bottom':0,'top':0},

	'S': {'shape': [(0,0), (-60,0), (0,-60), (60,-60)], 'color': GREEN,'right':60,'left':-60,'bottom':0,'top':-60},
	'Z': {'shape': [(0,0), (60,0), (0,-60), (-60,-60)], 'color': GREEN,'right':60,'left':-60,'bottom':0,'top':-60},
    'Sup':{'shape': [(0,0),(60,0),(0,-60),(60,60)],'color':GREEN,'right':60,'top':-60,'bottom':60,'left':0},
    'Zup':{'shape': [(0,0),(-60,0),(0,-60),(-60,60)],'color':GREEN,'right':0,'top':-60,'bottom':60,'left':-60},

    #Small Shapes
    '1x3': {'shape': [(0,0), (0,-60), (0,60)], 'color': CYAN,'right':0,'left':0,'bottom':60,'top':-60},
    '3x1': {'shape': [(0,0),(-60,0),(60,0)],'color':CYAN,'right':60,'left':-60,'bottom':0,'top':0},

    'LL': {'shape': [(0,0), (0,-60), (60,0)], 'color': RED,'right':60,'left':0,'bottom':0,'top':-60},
    'LJ': {'shape': [(0,0), (0,-60), (-60,0)], 'color': RED,'right':0,'left':-60,'bottom':0,'top':-60},
    'LJU': {'shape': [(0,0), (0,-60), (-60,-60)], 'color': RED,'right':0,'left':-60,'bottom':0,'top':-60},
    'LLU': {'shape': [(0,0), (0,-60), (60,-60)], 'color': RED,'right':60,'left':0,'bottom':0,'top':-60},

    '1x2': {'shape': [(0,0), (0,-60)], 'color': RED,'right':0,'left':0,'bottom':0,'top':-60},
    '2x1': {'shape': [(0,0), (-60,0)], 'color': RED,'right':0,'left':-60,'bottom':0,'top':0},

    '1x1': {'shape': [(0,0)], 'color': YELLOW,'right':0,'left':0,'bottom':0,'top':0}

}