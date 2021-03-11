import pygame
from .piece import Piece
from constants import *

class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def draw(self, window):
        window.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(window, BLUE, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 0)
                pygame.draw.rect(window, BLACK, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 1)


        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col == 1 and row == 0) or (col == 3 and row == 0) or (col == 2 and row == 3):
                    self.board[row].append(Piece(WHITE_PIECE, row, col))
                elif (col == 2 and row == 1) or (col == 1 and row == 4) or (col == 3 and row == 4):
                    self.board[row].append(Piece(BLACK_PIECE, row, col))
                else:
                    self.board[row].append(0)


    def move_piece(self,piece,direction):
        print("TODO")