import pygame

WIDTH, HEIGHT = 1200, 800
ROWS, COLS = 5, 5
SQUARE_SIZE = 160

#rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

#images
BLACK_PIECE = pygame.image.load('assets/black.png')
WHITE_PIECE = pygame.image.load('assets/white.png')
GRAY_DOT = pygame.image.load('assets/circle.png')
RED_DOT = pygame.image.load('assets/red_circle.png')

color_dic = {1 : BLACK_PIECE, 2 : WHITE_PIECE}

