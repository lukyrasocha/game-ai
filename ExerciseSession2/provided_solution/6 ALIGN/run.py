import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman 
from ghost import Ghost


class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.show_vectors = True


    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
    
    def startGame(self):
        self.setBackground()
        self.ghost = Ghost(self.screen)
        self.pacman = Pacman(self.screen, self.ghost)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.checkEvents()
        self.render()


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    self.show_vectors = not self.show_vectors

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        if self.show_vectors:
            game.pacman.draw_vectors()
            game.ghost.draw_vectors()
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()