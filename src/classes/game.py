import pygame
from constants import WHITE_PIECE, BLACK_PIECE, DARKBLUE, SQUARE_SIZE, GRAY_DOT
from classes.board import Board

class Game:

    def __init__(self,window):
        self._init()
        self.window = window


    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK_PIECE
        self.valid_moves = []

    def reset(self):
       self._init()

    def select(self,row,col):
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row,col)
        
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False

    def _move(self,row,col):
        piece = self.board.get_piece(row,col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            self.board.move_piece(self.selected, row, col)
            self.change_turn()
        else:
            return False
        
        return True

    def change_turn(self):
        self.valid_moves = []
        if self.turn == BLACK_PIECE:
            self.turn = WHITE_PIECE
        else:
            self.turn = BLACK_PIECE


    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            self.window.blit(GRAY_DOT,(SQUARE_SIZE*col+66,SQUARE_SIZE*row+66))
