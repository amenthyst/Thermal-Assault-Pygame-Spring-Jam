import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, playertuple, position, speed, bullet, bomb, particle, bullet_group, enemygrp):
        super().__init__()
        self.state = "cold"

        self.firesprite = playertuple[0]
        self.icesprite = playertuple[1]

        self.checktexture()
        self.rect = self.image.get_rect(center=position)

        self.velocity = pygame.math.Vector2()

        self.recoilvelocity = pygame.math.Vector2()

        self.controls = {pygame.K_w: (0, -1),
                         pygame.K_s: (0, 1),
                         pygame.K_a: (-1, 0),
                         pygame.K_d: (1, 0)}
        self.friction = 0.845
        self.maxvelocity = 20
        self.acceleration = speed
        self.bulletlastframe = False

        self.bullet = bullet
        self.bomb = bomb
        self.particle = particle

        self.shoot_force = 20
        self.bulletgrp = bullet_group
        self.enemygrp = enemygrp
        self.shoot_cooldown = 0.33
        self.bomb_cooldown = 0.33
        self.bomb_timer = 0
        self.shoot_timer = 0



        self.changing = False

    def get_pos(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.rect.x, self.rect.y)
    def get_centre(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.rect.centerx, self.rect.centery)

    def move(self):
        pressed = pygame.key.get_pressed()


        for vec in (self.controls[k] for k in self.controls if pressed[k]):

            self.velocity += pygame.math.Vector2(vec) * self.acceleration

        if self.velocity.magnitude() > self.maxvelocity:
            self.velocity = self.velocity.normalize() * self.maxvelocity


        self.velocity *= self.friction


        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def shoot(self, dt):
        self.shoot_timer += dt
        if not pygame.mouse.get_pressed(3)[0]:
            return
        if self.shoot_timer < self.shoot_cooldown:
            return
        self.shoot_timer = 0
        mouse_pos = pygame.mouse.get_pos()
        bullet_dir = pygame.math.Vector2(mouse_pos) - self.get_centre()
        bullet_dir = bullet_dir.normalize()
        bullet = self.bullet(self.get_centre(), bullet_dir * self.shoot_force, self.enemygrp, self.state)
        self.bulletgrp.add(bullet)
    def shootbomb(self, dt):
        self.bomb_timer += dt
        if not pygame.mouse.get_pressed(3)[2]:
            return
        if self.bomb_timer < self.bomb_cooldown:
            return
        self.bomb_timer = 0
        mouse_pos = pygame.mouse.get_pos()
        bombdir = pygame.math.Vector2(mouse_pos) - self.get_centre()
        bombdir = bombdir.normalize()
        bomb = self.bomb(self.get_centre(), bombdir * self.shoot_force, self.bulletgrp, self.enemygrp, self.state)
        self.bulletgrp.add(bomb)


    def thrower(self):
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_f]:
            return
        for _ in range(0,3):
            particledir = -(pygame.math.Vector2(pygame.mouse.get_pos()) - self.get_centre())
            particle = self.particle(self.state, "cone", self.enemygrp, self.bulletgrp, 5, self.get_centre(), particledir, 300, 0.6, 0.02)
            self.bulletgrp.add(particle)


    def update(self, dt):
        self.checktexture()
        self.rotimage = pygame.transform.rotate(self.image, self.getangle())
        self.rotrect = self.rotimage.get_rect(center=tuple(self.get_centre()))
        self.move()
        self.shoot(dt)
        self.shootbomb(dt)
        self.thrower()



    def recoil(self):
        # most annoying thing known to man
        particledir = self.get_centre() - pygame.mouse.get_pos()
        self.recoilvelocity += particledir * self.acceleration/20

        if self.recoilvelocity.length():
            self.recoilvelocity.normalize_ip()

        if self.recoilvelocity.magnitude() > self.maxvelocity/20:
            self.recoilvelocity = self.recoilvelocity.normalize() * self.maxvelocity/20

        self.recoilvelocity *= self.friction

        self.rect.x += self.recoilvelocity[0]
        self.rect.y += self.recoilvelocity[1]

    def getangle(self):
        direction = pygame.math.Vector2(pygame.mouse.get_pos()) - self.get_centre()
        return math.degrees(math.atan2(direction.x, direction.y)) + 180

    def draw(self, screen):
        screen.blit(self.rotimage, self.rotrect)

    def checktexture(self):
        if self.state == "hot":
            self.image = self.firesprite
        elif self.state == "cold":
            self.image = self.icesprite