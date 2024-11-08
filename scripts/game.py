import pygame

from scripts.entity.entity import *
from scripts.camera import Camera

class Game:
    def __init__(self, screen):
        self.screen = screen

        self.tile_size = 32

        self.camera = Camera(self.screen.get_size())
        self.player = Player(self.tile_size, (5, 5))
        
    def event_controls(self, event):
        self.player.update_directions(event)

        if event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.KEYUP:
            pass
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
    
    def render(self):
        self.player.draw(self.screen, self.camera.pos)

    def update(self, delta_time):
        self.dt = delta_time

        self.player.update(self.dt)
        self.render()
