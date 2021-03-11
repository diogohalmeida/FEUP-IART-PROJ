import pygame
from constants import BLACK, WHITE, SQUARE_SIZE

class Piece:
    PADDING = 10
    BORDER = 2

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

        self.x = 0 
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col - 10
        self.y = SQUARE_SIZE * self.row - 10

    def draw(self, window):
       window.blit(self.color, (self.x, self.y))
        

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
