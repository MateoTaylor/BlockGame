from BGsettings import *
from random import choice
from random import choices
class Game:
    def __init__(self,update_score):

        #general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT-180))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING*4))
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.sprites = pygame.sprite.Group()
        self.fakesprites = pygame.sprite.Group()
        self.endgame = False

        #game connection
        self.update_score = update_score

        #lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(100)

        #tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.create_new_tetromino(self.field_data)
        self.fakeexists = False
        self.pickup = [0,0,0]

        # score
        self.current_score = 0
        self.current_combo = 0
        self.combo_counter = 0

    def calculate_score(self,num_lines):
        self.current_score += num_lines*self.current_combo*10
        self.update_score(self.current_score)
        

    def create_new_tetromino(self,field_data):
        data = [] #creating temporary binary copy of field_data
        for row in field_data:
            r = []
            for s in row:
                if s == 0: r.append(0)
                else: r.append(1)
            data.append(r)
        x = choice([[1,2,3],[3,2,1],[2,1,3],[2,3,1]])

        shape1 = self.tetromino_randomizer(data)
        self.tetromino = Tetromino(shape1[0],self.sprites,False,x[0])
        shape2 = self.tetromino_randomizer(shape1[1])
        self.tetromino2 = Tetromino(shape2[0],self.sprites,False,x[1])
        shape3 = self.tetromino_randomizer(shape2[1])
        self.tetromino3 = Tetromino(shape3[0],self.sprites,False,x[2])

        self.tetromino_list = [self.tetromino,self.tetromino2,self.tetromino3]
        self.pickup = [0,0,0]

    def tetromino_randomizer(self,data):
        tpop = ['BS','5x1','1x5','BL','BLU','BJ','BJU',
    'J', 'L','JU','LU','LSW','JSW','LSU','JSU','T','TF','UDT','UDTF','SS','1x4','4x1','S','Z','Sup','Zup',
    '1x3','3x1','LL','LJ','LJU','LLU','2x1','1x2',
    '1x1']
        tweight = [64,32,32,16,16,16,16,
                     4,4,4,4,4,4,4,4,4,4,4,4,16,8,8,4,4,4,4,
                     6,6,3,3,3,3,3,3,1]
        while True:
            random_shape = choices(tpop,weights=tweight)
            possible_spaces = self.finding_empty_spaces(data,random_shape[0])
            if possible_spaces:
                chosen_space = choice(possible_spaces)
                for block_pos in TETROMINOS[random_shape[0]]['shape']:
                    data[chosen_space[0]+int(block_pos[1]/60)][chosen_space[1]+int(block_pos[0]/60)] = 1
                return [random_shape[0],data]
            else:
                tweight.remove(tweight[tpop.index(random_shape[0])])
                tpop.remove(random_shape[0])


    def finding_empty_spaces(self,field_data,shape):
        empty_spaces = []
        block_positions = TETROMINOS[shape]['shape']
        for row in enumerate(field_data):   
                for empty_space in enumerate(row[1]):              
                    if empty_space[1] == 0: # if i find an empty space
                        c = 0
                        for block_pos in block_positions: #getting all block positions
                            if 7>= row[0]+int(block_pos[1]/60) >= 0 and 7 >= empty_space[0]+int(block_pos[0]/60) >= 0:
                                if field_data[row[0]+int(block_pos[1]/60)][empty_space[0]+int(block_pos[0]/60)] != 0:
                                    break
                                else: c+= 1
                        if c == len(block_positions):
                            empty_spaces.append([row[0],empty_space[0]])
        return empty_spaces
    
    def create_fake_tetromino(self,tetromino):
        self.tetrominofake = Tetromino(tetromino.real_shape,self.fakesprites,self.field_data,0)
        for block in self.tetrominofake.blocks:
            block.image.set_alpha(100)
    
    def draw_grid(self):
        for col in range(1,COLUMNS):
            x = col*CELL_SIZE
            pygame.draw.line(self.line_surface, '#FFFFFF', (x,0),(x,480),1)
        for row in range(1,ROWS):
            x = row*CELL_SIZE
            pygame.draw.line(self.line_surface, '#FFFFFF',(0,x),(self.surface.get_width(),x),1)
        
        self.surface.blit(self.line_surface,(0,0))

    def check_finished_rows (self):
        self.combo_counter += 1
        if self.combo_counter > 3:
            self.current_combo = 0
        delete_rows = []
        delete_columns = []
        for i,row in enumerate(self.field_data):
            if all(row): delete_rows.append(i)
        for column in range(8):
            c = 0
            for row in self.field_data:
                if row[column] == 0: c = 1
            if c == 0: delete_columns.append(column)

        if delete_rows: #clearing the row visually
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()
        if delete_columns:
            for delete_column in delete_columns:
                for row in self.field_data:
                    if row[delete_column]: row[delete_column].kill()        
        if delete_columns or delete_rows:
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            self.current_combo += 1
            self.combo_counter = 0
            self.calculate_score(len(delete_columns)+len(delete_rows))
        c = 0
        for block in self.fakesprites:
            if block.image.get_alpha() == 0:
                block.kill()
            if block.pos.y < 481:
                c +=1
                #print(int((block.pos.x-30)/60),int((block.pos.y-30)/60))
                self.field_data[int((block.pos.y)/60)-1][int((block.pos.x)/60)-1] = block

    def endGame(self):
        for sprite in self.sprites:
            sprite.kill()
        for sprites in self.fakesprites:
            sprites.kill()
        self.gameover_surf = pygame.image.load('BlockGame/graphics/gameover.png')
        self.gameover_rect = self.gameover_surf.get_rect(center = (GAME_WIDTH/2,GAME_HEIGHT/2))
        

    def run(self,mouseup,mousedown):
        mousepos = pygame.mouse.get_pos()
        mouseposreal = (mousepos[0]-20,mousepos[1]-80)
        for tetromino in enumerate(self.tetromino_list):
            if self.pickup[tetromino[0]] == 0 and tetromino[1].blocks[0].z == 60:
                for blocks in tetromino[1].blocks:
                    blocks.z = 30
                    blocks.pos = pygame.Vector2(int(blocks.distance[0]*1/2),int(blocks.distance[1]*1/2)) + BLOCK_OFFSET + pygame.Vector2(60*2*blocks.startpos,0)
                    blocks.image = pygame.Surface((blocks.z,blocks.z))
                    blocks.image.fill(blocks.color)
            if sum(self.pickup)==1 and self.pickup[tetromino[0]] == 0 or self.endgame == True:
                pass
            else:
                if mouseup == True: # when mouse picks up
                    if self.fakeexists == True:
                        if self.tetrominofake.blocks[0].image.get_alpha() > 0: # (if on board and if not colliding with other blocks)
                            for block in tetromino[1].blocks:      # kill main block
                                block.kill()
                            self.tetromino_list.remove(tetromino[1])       #remove from list of tetrominos
                            for block in self.tetrominofake.blocks:
                                block.image.set_alpha(255)              #place fake on board
                                self.field_data[int((block.pos.y)/60)-1][int((block.pos.x)/60)-1] = block
                            if not self.tetromino_list:                 #if list empty= make 3 new tets
                                self.create_new_tetromino(self.field_data)
                            self.check_finished_rows()                  #check rows and all that
                            if self.space_checker(self.field_data,self.tetromino_list) == False: #checking endgame
                                self.endgame = True
                                self.endGame()
                            else:
                                self.pickup = [0,0,0]
                        else:
                            for blocks in self.tetrominofake.blocks:
                                blocks.kill()
                    else: 
                        pass
                    self.fakeexists = False
                    self.pickup = [0,0,0]
                if mousedown == True:
                    for block in tetromino[1].blocks:
                        if block.rect.collidepoint(mouseposreal):
                            self.pickup[tetromino[0]] = 1
                        if self.pickup[tetromino[0]]==1:
                            if tetromino[1].blocks[0].z == 30:
                                for blocks in tetromino[1].blocks:
                                    blocks.z = 60
                                    blocks.pos = pygame.Vector2(blocks.distance) + BLOCK_OFFSET + pygame.Vector2(60*2*blocks.startpos,0)
                                    blocks.image = pygame.Surface((blocks.z,blocks.z))
                                    blocks.image.fill(blocks.color)
                            tetromino[1].movement(False,mouseposreal) 
                            if self.fakeexists==False:
                                print('making a fake')
                                self.create_fake_tetromino(tetromino[1])
                                self.fakeexists = True
                            self.tetrominofake.movement(True,mouseposreal)

        
        if self.endgame == True:
            self.surface.fill(GRAY)
            self.surface.blit(self.gameover_surf,self.gameover_rect)       
        else:
            #update 
            self.sprites.update()
            self.fakesprites.update()

            #drawing
            self.surface.fill(GRAY)
            self.fakesprites.draw(self.surface)
            self.sprites.draw(self.surface)

            self.draw_grid()
            

        self.display_surface.blit(self.surface, (PADDING,PADDING*4))
        if self.endgame == False:
            pygame.draw.rect(self.display_surface,'#FFFFFF',self.rect,2,2)
        else:
            if self.gameover_rect.top < mouseposreal[1]< self.gameover_rect.bottom and self.gameover_rect.left < mouseposreal[0] < self.gameover_rect.right:
                self.gameover_surf = pygame.image.load('BlockGame/graphics/gameover_selected.png')
                if mousedown == True:
                    self.endgame = False
                    self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
                    self.create_new_tetromino(self.field_data)
                    self.fakeexists = False
                    self.pickup = [0,0,0]
                    self.update_score(0)
            else:
                self.gameover_surf = pygame.image.load('BlockGame/graphics/gameover.png')


    def space_checker(self,field_data,tetromino_list):
        for tetromino in tetromino_list:
            for row in enumerate(field_data):   
                for empty_space in enumerate(row[1]):              
                    if empty_space[1] == 0: # if i find an empty space
                        c = 0
                        for block_pos in tetromino.block_positions: #checking all x - y values:
                            if 7>= row[0]+int(block_pos[1]/60) >= 0 and 7 >= empty_space[0]+int(block_pos[0]/60) >= 0:
                                if field_data[row[0]+int(block_pos[1]/60)][empty_space[0]+int(block_pos[0]/60)] != 0:
                                    break
                                else: c+= 1
                        if c == len(tetromino.block_positions):
                            return True
        return False                    

        


class Tetromino:
    def __init__(self,shape,group,field_data,tetromino_number):

        #setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.real_shape = shape
        self.field_data = field_data
        self.number = tetromino_number
        self.top = TETROMINOS[shape]['top']
        self.bottom = TETROMINOS[shape]['bottom']
        self.left = TETROMINOS[shape]['left']
        self.right = TETROMINOS[shape]['right']

        #create blocks
        self.blocks = [Block(group, pos, self.color,tetromino_number) for pos in self.block_positions]
        
    # collisions
    def movement(self,fakeornot:bool,mouseposreal):

        if fakeornot == False:
            if self.blocks[0].rect.top + self.top < 1: #collisions for top side
                for b in self.blocks:
                    if mouseposreal[1] < 60 - self.top:
                        b.pos.y = 60-self.top + ((self.block_positions[self.blocks.index(b)][1]))
                    else: b.pos.y = mouseposreal[1] + (self.block_positions[self.blocks.index(b)][1])

            elif self.blocks[0].rect.bottom + self.bottom > 659 - self.bottom: #collisions for bottom side
                for b in self.blocks:
                    if mouseposreal[1] > 659-self.bottom:
                        b.pos.y = 660-self.bottom + ((self.block_positions[self.blocks.index(b)][1]))
                    else: b.pos.y = mouseposreal[1] + (self.block_positions[self.blocks.index(b)][1])
            else: 
                for b in self.blocks: b.pos.y = mouseposreal[1] + (self.block_positions[self.blocks.index(b)][1])

            if self.blocks[0].rect.left + self.left < 1: #collisions for left side
                for b in self.blocks:
                    if mouseposreal[0] < 61-self.left:
                        b.pos.x = 60-self.left + ((self.block_positions[self.blocks.index(b)][0]))
                    else: b.pos.x = mouseposreal[0] + (self.block_positions[self.blocks.index(b)][0])
            elif self.blocks[0].rect.right + self.right > 479: #collisions for right side
                for b in self.blocks:
                    if mouseposreal[0] > 479-self.right:
                        b.pos.x = 480-self.right + ((self.block_positions[self.blocks.index(b)][0]))
                    else: b.pos.x = mouseposreal[0] + (self.block_positions[self.blocks.index(b)][0])
            else: 
                for b in self.blocks: b.pos.x = mouseposreal[0] + (self.block_positions[self.blocks.index(b)][0])

        else: # fake block - must be placed
            colliding = False
            for row in self.field_data:
                if colliding == False: 
                    for b in row:
                        if b != 0: 
                            for blocks in self.blocks:
                                if b.rect.colliderect(blocks.rect):
                                    colliding = True
                            if colliding == True:
                                for block in self.blocks:
                                    block.image.set_alpha(0)
                                break
            if self.blocks[0].rect.top + self.top < 1: #collisions for top side
                for b in self.blocks:
                    if mouseposreal[1] < 61 - self.top:
                        b.pos.y = 60-self.top + ((self.block_positions[self.blocks.index(b)][1]))
                    else: b.pos.y = CELL_SIZE*round(mouseposreal[1]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][1])

            elif self.blocks[0].rect.bottom + self.bottom > 494: #collisions for bottom side
                for b in self.blocks:
                    if mouseposreal[1] > 494-self.bottom:
                        b.image.set_alpha(0)
                    else: 
                        b.pos.y = CELL_SIZE*round(mouseposreal[1]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][1])
            else: 
                for b in self.blocks: 
                    if colliding == False: b.image.set_alpha(100)
                    b.pos.y = CELL_SIZE*round(mouseposreal[1]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][1])

            if self.blocks[0].rect.left + self.left < 1: #collisions for left side
                for b in self.blocks:
                    if mouseposreal[0] < 61-self.left:
                        b.pos.x = 60-self.left + ((self.block_positions[self.blocks.index(b)][0]))
                    else: b.pos.x = CELL_SIZE*round(mouseposreal[0]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][0])


            elif self.blocks[0].rect.right + self.right > 479: #collisions for right side
                for b in self.blocks:
                    if mouseposreal[0] > 479-self.right:
                        b.pos.x = 480-self.right + ((self.block_positions[self.blocks.index(b)][0]))
                    else: 
                        b.pos.x = CELL_SIZE*round(mouseposreal[0]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][0])
            else: 
                for b in self.blocks: 
                    b.pos.x = CELL_SIZE*round(mouseposreal[0]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][0])
            for b in self.blocks:
                if colliding == False and mouseposreal[1] < 494-self.bottom:
                    b.image.set_alpha(100)

                
class Block(pygame.sprite.Sprite):
    def __init__(self,group,pos,color,startpos):

        self.z = 60
        self.distance = pos
        self.startpos = startpos
        self.color = color

        #general
        super().__init__(group)
        self.image = pygame.Surface((self.z,self.z))
        self.image.fill(color)
        


        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET + pygame.Vector2(60*2*startpos,0)

        x = self.pos.x
        y = self.pos.y
        self.rect = self.image.get_rect(bottomright = (x,y))
    

    def update(self):
        self.rect = self.image.get_rect(bottomright = self.pos)# * CELL_SIZE)