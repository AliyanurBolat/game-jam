from settings import *
from math import sin, cos, radians
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)

class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type 
        self.data = data
    
    def activate(self):
        if self.item_type == 'gold':
            self.data.coins += 5
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.coins += 12
        if self.item_type == 'skull':
            self.data.coins += 50
        if self.item_type == 'potion':
            self.data.health += 1
        if self.item_type == 'jacket':
            self.data.jacket_collected = True
        if self.item_type == 'backpack':
            self.data.backpack_collected = True

class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.z = Z_LAYERS['fg']
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class MovingSprite(AnimatedSprite):
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip = False):
        super().__init__(start_pos, frames, groups)
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
       

        # movement
        self.moving = True
        self.speed = speed
        self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
        self.move_dir = move_dir

        self.flip = flip
        self.reverse = {'x': False, 'y': False}

    def check_border(self):
        if self.move_dir == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            self.reverse['x'] = True if self.direction.x < 0 else False
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            self.reverse['y'] = True if self.direction.y > 0 else False

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()

        self.animate(dt)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

class Spike(Sprite):
    def __init__(self, pos, radius, surf, groups, speed, start_angle, end_angle, z = Z_LAYERS['main']):
        self.center = pos
        self.radius = radius
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1
        self.full_circle = True if self.angle == -1 else False
        
        # trigonometry
        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius

        super().__init__((x,y), surf, groups, z)

    def update(self, dt):
        self.angle += self.direction * self.speed * dt

        if not self.full_circle:
            if self.angle >= self.end_angle:
                self.direction = -1
            if self.angle < self.start_angle:
                self.direction = 1

        y = self.center[1] + sin(radians(self.angle)) * self.radius
        x = self.center[0] + cos(radians(self.angle)) * self.radius
        self.rect.center = (x,y)

class Cloud(Sprite):
    def __init__(self, pos, surf, groups, z = Z_LAYERS['clouds']):
        super().__init__(pos, surf, groups, z)
        self.speed = randint(50, 120)
        self.direction = -1
        self.rect.midbottom = pos

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

        if self.rect.right <= 0:
            self.kill()



