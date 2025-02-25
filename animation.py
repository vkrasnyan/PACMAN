import pygame


def import_sprite(path):
    img_surface = pygame.image.load(path).convert_alpha()
    return img_surface
