from BGsettings import *

class Score: 
    def __init__(self):

        #general 
        self.surface = pygame.Surface((GAME_WIDTH,PADDING*2))
        self.rect = self.surface.get_rect(midtop = (WINDOW_WIDTH*0.5,PADDING))
        self.display_surface = pygame.display.get_surface()

        #font
        self.font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 30)

        #data
        self.score = 0 
        

    def run(self):
        self.surface.fill(GRAY)

        text_surface = self.font.render(f'Score: {self.score}', True, 'white')
        text_rect = text_surface.get_rect(center = (self.surface.get_width()/2,self.surface.get_height()/2))
        self.surface.blit(text_surface,text_rect)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface,'#FFFFFF',self.rect,2,2)
