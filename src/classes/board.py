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
        print(self.board)


    def move_piece(self,piece,row,col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row,col)

    def get_piece(self,row,col):
        return self.board[row][col]


    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win)

    
    def get_valid_moves(self,piece):
        moves = []
        #Left
        for col in range(piece.col-1,-1,-1):
            if self.board[piece.row][col] != 0:
                break

            elif col == 0:
                moves.append((piece.row,col))
                break

            elif self.board[piece.row][col-1] != 0:
                moves.append((piece.row,col))
                break
        #Right
        for col in range(piece.col+1,5):
            if(self.board[piece.row][col] != 0):
                break

            elif col == 4:
                moves.append((piece.row,col))
                break

            elif self.board[piece.row][col+1] != 0:
                moves.append((piece.row,col))
                break
        #Top
        for row in range(piece.row-1,-1,-1):
            if self.board[row][piece.col] != 0:
                break

            elif row == 0:
                moves.append((row,piece.col))
                break

            elif self.board[row-1][piece.col] != 0:
                moves.append((row,piece.col))
                break

        #Bottom
        for row in range(piece.row+1,5):
            if self.board[row][piece.col] != 0:
                break

            elif row == 4:
                moves.append((row,piece.col))
                break

            elif self.board[row+1][piece.col] != 0:
                moves.append((row,piece.col))
                break

        #TopLeft
        col = piece.col-1
        row = piece.row-1
        while col != -1 and row != -1:

            if self.board[row][col] != 0:
                break

            elif col == 0 or row == 0:
                moves.append((row,col))
                break

            elif self.board[row-1][col-1] != 0:
                moves.append((row,col))
                break

            col -= 1
            row -= 1

        #BottomLeft
        col = piece.col-1
        row = piece.row+1
        while col != -1 and row != 5:

            if self.board[row][col] != 0:
                break

            elif col == 0 or row == 4:
                moves.append((row,col))
                break

            elif self.board[row+1][col-1] != 0:
                moves.append((row,col))
                break

            col -= 1
            row += 1

        
        #TopRight
        col = piece.col+1
        row = piece.row-1
        while col != 5 and row != -1:

            if self.board[row][col] != 0:
                break

            elif col == 4 or row == 0:
                moves.append((row,col))
                break

            elif self.board[row-1][col+1] != 0:
                moves.append((row,col))
                break

            col += 1
            row -= 1
        
        #BottomRight
        col = piece.col+1
        row = piece.row+1
        while col != 5 and row != 5:

            if self.board[row][col] != 0:
                break

            elif col == 4 or row == 4:
                moves.append((row,col))
                break

            elif self.board[row+1][col+1] != 0:
                moves.append((row,col))
                break

            col += 1
            row += 1

        return moves

    def threeInRow(self,row,col,piece):

        #TopLeft
        if row > 0 and col > 0:
            if self.board[row-1][col-1] != 0 and self.board[row-1][col-1].color == piece:
                if row > 1 and col > 1 and self.board[row-2][col-2] != 0 and self.board[row-2][col-2].color == piece:
                    return True
                elif row < 4 and col < 4 and self.board[row+1][col+1] != 0 and self.board[row+1][col+1].color == piece:
                    return True
        
        #Top
        if row > 0:
            if self.board[row-1][col] != 0 and self.board[row-1][col].color == piece:
                if row > 1 and self.board[row-2][col] != 0 and self.board[row-2][col].color == piece:
                    return True
                elif row < 4 and self.board[row+1][col] != 0 and self.board[row+1][col].color == piece:
                    return True

        #TopRight
        if row > 0 and col < 4:
            if self.board[row-1][col+1] != 0 and self.board[row-1][col+1].color == piece:
                if row > 1 and col < 3 and self.board[row-2][col+2] != 0 and self.board[row-2][col+2].color == piece:
                    return True
                elif row < 4 and col > 0  and self.board[row+1][col-1] != 0 and self.board[row+1][col-1].color == piece:
                    return True
        
        #Right
        if col < 4:
            if self.board[row][col+1] != 0 and self.board[row][col+1].color == piece:
                if col < 3 and self.board[row][col+2] != 0 and self.board[row][col+2].color == piece:
                    return True
                elif col > 0 and self.board[row][col-1] != 0 and self.board[row][col-1].color == piece:
                    return True

        #BottomLeft
        if row < 4 and col < 4:
            if self.board[row+1][col+1] != 0 and self.board[row+1][col+1].color == piece:
                if row < 3 and col < 3 and self.board[row+2][col+2] != 0 and self.board[row+2][col+2].color == piece:
                    return True
                elif row > 0 and col > 0 and self.board[row-1][col-1] != 0 and self.board[row-1][col-1].color == piece:
                    return True

        #Bottom
        if row < 4:
            if self.board[row+1][col] != 0 and self.board[row+1][col].color == piece:
                if row < 3 and self.board[row+2][col] !=0 and self.board[row+2][col].color == piece:
                    return True
                elif row > 0 and self.board[row-1][col] !=0 and self.board[row-1][col].color == piece:
                    return True

        #BottomRight
        if row < 4 and col > 0:
            if self.board[row+1][col-1] != 0 and self.board[row+1][col-1].color == piece:
                if row < 3 and col > 1 and self.board[row+2][col-2] != 0 and self.board[row+2][col-2].color == piece:
                    return True
                elif row > 0 and col < 4 and self.board[row-1][col+1] != 0 and self.board[row-1][col+1].color == piece:
                    return True


        #Left
        if col > 0:
            if self.board[row][col-1] != 0 and self.board[row][col-1].color == piece:
                if col > 1 and self.board[row][col-2] != 0 and self.board[row][col-2].color == piece:
                    return True
                elif col < 4 and self.board[row][col+1] != 0 and self.board[row][col+1].color == piece:
                    return True

        return False