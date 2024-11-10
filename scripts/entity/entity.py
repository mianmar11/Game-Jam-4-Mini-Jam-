import pygame 
from pygame.math import Vector2 as vec2

from scripts.utility import *

class Entity:
    def __init__(self, size, pos):
        self.ori_pos = pos # original pos 
        self.size = size # size
        
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.fill('blue')
        
        '''
        Here original position is multiplied with size to get real world position.
        original position could be (0, 1), (0, 2) and to convert it into real world position,
        gotta multiply with size of the object or standard size to get actual world position
        '''
        self.rect = self.image.get_rect(topleft=(self.ori_pos[0]*self.size, self.ori_pos[1]*self.size))
    
    def draw(self, draw_surf, camera_offset):
        # projected positions
        render_x, render_y = self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))
    
    def update(self, delta_time):
        self.dt = delta_time

class Player(Entity):
    def __init__(self, size, pos):
        super().__init__(size, pos)

        self.image.fill('green')

        # movement settings
        self.x, self.y = self.rect.topleft
        self.directions = {
            'left': False,
            'right': False,
            'up': False, 
            'down': False,
        }
        self.frictions = {
            'standard': 1,
        }
        self.vel = vec2(0, 0)
        self.speed = 5 # for all directions

        # animation settings
        self.facing_left = False
        self.facing_up = False
        self.state = 'standing'
        self.frame = 0
        self.frame_speed = 0.2

    def update_directions(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            # vertical movement
            if key == pygame.K_w:
                self.directions['up'] = True
            elif key == pygame.K_s:
                self.directions['down'] = True
            
            # horizontal movement
            if key == pygame.K_a:
                self.directions['left'] = True
            elif key == pygame.K_d:
                self.directions['right'] = True
        
        if event.type == pygame.KEYUP:
            key = event.key
            # vertical movement
            if key == pygame.K_w:
                self.directions['up'] = False
            elif key == pygame.K_s:
                self.directions['down'] = False
            
            # horizontal movement
            if key == pygame.K_a:
                self.directions['left'] = False
            elif key == pygame.K_d:
                self.directions['right'] = False
    
    def movement(self):
        # gain momentum
        if self.directions['left']: 
            self.vel.x -= 1 * self.speed * self.dt
        elif self.directions['right']:
            self.vel.x += 1 * self.speed * self.dt
        else:
            if self.vel.x > 0:
                self.vel.x = max(self.vel.x - self.frictions['standard'] * self.dt, 0)
            elif self.vel.x < 0:
                self.vel.x = min(self.vel.x + self.frictions['standard'] * self.dt, 0)
        
        if self.directions['up']:
            self.vel.y -= 1 * self.speed * self.dt
        elif self.directions['down']:
            self.vel.y += 1 * self.speed * self.dt
        else:
            if self.vel.y > 0:
                self.vel.y = max(self.vel.y - self.frictions['standard'] * self.dt, 0)
            elif self.vel.y < 0:
                self.vel.y = min(self.vel.y + self.frictions['standard'] * self.dt, 0)
        
        if self.vel.length() > 1 * self.speed:
            self.vel.scale_to_length(1 * self.speed)

        # update position
        self.x += self.vel.x * self.dt
        self.y += self.vel.y * self.dt
        self.rect.topleft = self.x, self.y

    def set_state(self):
        if self.vel.length() != 0:
            self.state = 'walking'
        else:
            self.state = 'standing'  
        
        if self.vel.x > 0:
            self.facing_left = False
        elif self.vel.x < 0:
            self.facing_left = True
        
        if self.vel.y > 0:
            self.facing_up = False
        elif self.vel.y < 0:
            self.facing_up = True
        
    def draw(self, draw_surf, camera_offset):
        return super().draw(draw_surf, camera_offset)

    def update(self, delta_time):
        super().update(delta_time)

        self.movement()
        self.set_state()
        