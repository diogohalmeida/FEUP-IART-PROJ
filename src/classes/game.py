import pygame
from constants import *
from classes.board import Board
from copy import deepcopy

class Game:

    def __init__(self,window):
        self._init()
        self.window = window
        self.lastMove = None


    def update(self):
        self.drawBoard()
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.player = 1
        self.valid_moves = []
        self.lastMove = None

    def drawBoard(self):
        self.window.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.window, BLUE, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 0)
                pygame.draw.rect(self.window, BLACK, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 1)


        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.board[row][col]
                if piece != 0:
                    self.window.blit(color_dic[piece], (SQUARE_SIZE * col - 10, SQUARE_SIZE * row - 10))

    def reset(self):
       self._init()

    def getPlayer(self):
        return self.player

    def getLastMove(self):
        return self.lastMove

    def getBoard(self):
        return self.board

    def updateLastMove(self,row,col):
        self.lastMove = row,col

    def select(self,row,col):
        if self.selected:
            result = self.move(row,col)
            if not result:
                self.selected = None
                self.select(row,col)
        
        piece = self.board.get_piece(row,col)
        if piece == self.player:
            self.selected = (row,col)
            self.valid_moves = self.board.get_valid_moves(row, col)
            return True
        
        return False

    def move(self,row,col):
        piece = self.board.get_piece(row,col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            oldRow, oldCol = self.selected
            self.board.move_piece(oldRow,oldCol, row, col)
            self.updateLastMove(row,col)
            self.change_turn()
        else:
            return False
        
        return True

    def ai_move(self, row, col):
        oldRow, oldCol = self.selected
        self.board.move_piece(oldRow,oldCol, row, col)
        self.updateLastMove(row,col)
        self.change_turn()

    def change_turn(self):
        self.valid_moves = []
        self.player = 3 - self.player


    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            self.window.blit(GRAY_DOT,(SQUARE_SIZE*col+66,SQUARE_SIZE*row+66))

    def checkWin(self):
        if self.lastMove == None :
            return -1
        row, col = self.lastMove
        return self.board.threeInRow(row,col, 3-self.player)

    def max(self, lastRow, lastCol, maxDepth, alpha, beta):
        #print("Entrei no max\n")
        maxv = -2

        depth = maxDepth - 1

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        if maxDepth == 0:
            return (0, 0, 0, 0, 0)


        if self.board.threeInRow(lastRow, lastCol, 2) == 2:
            return (1, 0, 0, 0, 0)

        if self.board.threeInRow(lastRow, lastCol, 1) == 1:
            return (-1, 0, 0, 0, 0)


        pieces = deepcopy(self.board.get_white_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, min_old_row, min_old_col, min_row, min_col) = self.min(moveRow, moveCol, depth, alpha, beta)

                if m > maxv:
                    maxv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                if maxv >= beta:
                    return (maxv, finalOldRow, finalOldCol, finalRow, finalCol)

                if maxv > alpha:
                    alpha = maxv
            
                

        return (maxv, finalOldRow, finalOldCol, finalRow, finalCol)


    def min(self, lastRow, lastCol, maxDepth, alpha, beta):
        #print("Entrei no min\n")

        minv = 2

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        depth = maxDepth - 1

        if maxDepth == 0:
            return (0, 0, 0, 0, 0)


        if self.board.threeInRow(lastRow, lastCol, 1) == 1:
            return (-1, 0, 0, 0, 0)

        elif self.board.threeInRow(lastRow, lastCol, 2) == 2:
            return (1, 0, 0, 0, 0)
        

        pieces = deepcopy(self.board.get_black_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, max_old_row, max_old_col, max_row, max_col) = self.max(moveRow, moveCol, depth, alpha, beta)

                if m < minv:
                    minv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finaloldRow = oldRow
                    finaloldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                if minv <= alpha :
                    return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)

                if minv < beta:
                    beta = minv 

        return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)

                    
