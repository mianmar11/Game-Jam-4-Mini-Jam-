import pygame

class Editor:
    def __init__(self, tile_size):
        self.tile_size = tile_size

        self.tiles = {}
    
    def draw(self, draw_surf):
        pass

    def button_control(self, button):
        if button == pygame.BUTTON_LEFT:
            self.add()
        elif button == pygame.BUTTON_RIGHT:
            self.delete()
    
    def add(self):
        pass

    def delete(self):
        pass

    def update(self, camera_offset):
        self.camera_offset = camera_offset
        self.mpos = pygame.mouse.get_pos()
        self.tile_pos = self.mpos[0] // self.tile_size * self.tile_size, self.mpos[1] // self.tile_size * self.tile_size # grid position

