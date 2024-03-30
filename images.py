import pygame
def renderplayer():
    player = pygame.image.load("Pygame-Spring-Jam-2024/Graphics/player.png").convert_alpha()
    player = pygame.transform.scale(player, (35,35))
    return player

def renderbullets():
    bullet = pygame.image.load("Pygame-Spring-Jam-2024/Graphics/bullet.png").convert_alpha()
    bullet = pygame.transform.scale(bullet, (10,20))
    bomb = pygame.image.load("Pygame-Spring-Jam-2024/Graphics/coldbomb.png").convert_alpha()
    bomb = pygame.transform.scale(bomb, (50,15))
    return (bullet, bomb)

