from settings import *
from random import choice
from timer import Timer
from os.path import join

class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 200

        self.hit_timer = Timer(250)

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def update(self, dt):
        self.hit_timer.update()

        # animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
            
        # move
        self.rect.x += self.direction * self.speed * dt

        # reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1,1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1,1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
           floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
                self.direction *= -1

class Crowd(Tooth):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(pos, frames, groups, collision_sprites)
        self.speed = 100

class Chandelier(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)

        self.frames = frames
        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player

        self.speed = 300
        self.has_fallen = False
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.explosion_timer = Timer(50)

    def state_management(self):
        player_pos, chandelier_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = chandelier_pos.distance_to(player_pos) < 350

        if player_near and self.has_fallen == False:
            self.state = 'fall'
            self.frame_index = 0

    def create_explosion(self):
        self.state = 'explosion'

    def update(self, dt):
        self.state_management()
        self.explosion_timer.update()

        # animation / falling
        self.frame_index += 12 * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # fall
            if self.state == 'fall' and not self.has_fallen:
                self.rect.y += self.speed * dt

        bottom_rect = pygame.FRect(self.rect.bottomleft + vector(-1, 0), (self.rect.width + 2, 1))
        if bottom_rect.collidelist(self.collision_rects) != -1:
            self.create_explosion()
            self.has_fallen = True
