from pygame.math import Vector2 as vec2

class Camera:
    def __init__(self, screen_size):
        self.WIDTH, self.HEIGHT = screen_size

        self.pos = vec2(0, 0)
        self.vel = vec2(0, 0)
    
    def follow_entity(self, entity):
        self.vel.x += (entity.rect.x - self.vel.x) * 0.2 * self.dt
        self.vel.y += (entity.rect.y - self.vel.y) * 0.2 * self.dt

        self.pos.x += self.vel.x * self.dt
        self.pos.y += self.vel.y * self.dt

    def update(self, delta_time):
        self.dt = delta_time