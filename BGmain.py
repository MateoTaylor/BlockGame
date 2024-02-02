from BGsettings import *
from sys import exit

#components
from BGgame import Game
from BGscore import Score

class Main:
    def __init__(self):
        
        #general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Block Game')
        self.clock = pygame.time.Clock()

        #components
        self.game = Game(self.update_score)
        self.score = Score()

        self.mdown = False
        self.mup = False
    
    def update_score(self, score):
        self.score.score = score


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mdown = True
                    self.mup = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mup = True
                    self.mdown = False

            #display
            self.display_surface.fill(GRAY)

            #components
            self.game.run(self.mup,self.mdown)
            self.score.run()

            #updating the game
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    main = Main()
    main.run()  