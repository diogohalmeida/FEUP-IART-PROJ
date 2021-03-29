import pygame
from constants import *
from classes.board import Board
from classes.button import Button
from copy import deepcopy
import random

class Game:

    def __init__(self,window, gamemode):
        self._init()
        self.window = window
        self.lastMove = None
        self.winner = None
        self.gamemode = gamemode
        self.button = None
        self.time = None


    def update(self, time_elapsed):
        if time_elapsed != None:
            self.time = time_elapsed
        
        self.drawBoard()
        self.drawSideBoard()
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.player = 1
        self.valid_moves = []
        self.lastMove = None
        self.boards = {}

    def drawBoard(self):
        self.window.fill((76,188,228))
        
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.window, BLUE, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 0)
                pygame.draw.rect(self.window, BLACK, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 1)


        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.board[row][col]
                if piece != 0:
                    self.window.blit(color_dic[piece], (SQUARE_SIZE * col - 10, SQUARE_SIZE * row - 10))


    def drawSideBoard(self):
        if self.player == 1:
            myfont = pygame.font.SysFont('', 60)
            sideboard_title = myfont.render('BLACK TURN', True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 50))
            self.window.blit(sideboard_title, text_rect)
        elif self.player == 2:
            myfont = pygame.font.SysFont('', 60)
            sideboard_title = myfont.render('WHITE TURN', True, WHITE)
            text_rect = sideboard_title.get_rect(center=(1000, 50))
            self.window.blit(sideboard_title, text_rect)

        if self.gamemode == 1 or (self.gamemode == 2 and self.player == 1):
            self.button = Button(BLUE, 850, 150, 300, 100, 'Press for a hint')
            self.button.draw(self.window, True)
        elif self.gamemode == 3 or (self.gamemode == 2 and self.player == 2):
            self.button = Button(BLUE, 825, 150, 350, 100, 'Press for computer play')
            self.button.draw(self.window, True)
            


        if self.gamemode != 1 and self.time != None:
            myfont = pygame.font.SysFont('', 40)
            sideboard_title = myfont.render("AI Move took: " + str(round(self.time,3)) + " s", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 300))
            self.window.blit(sideboard_title, text_rect)

        if self.winner != None and self.winner != -1:
            myfont = pygame.font.SysFont('', 60)
            if self.winner == 1:
                sideboard_title = myfont.render('BLACK WINS!', True, (0,0,0))
                text_rect = sideboard_title.get_rect(center=(1000, 700))
                self.window.blit(sideboard_title, text_rect)
            elif self.winner == 2:
                sideboard_title = myfont.render('WHITE WINS!', True, (255,255,255))
                text_rect = sideboard_title.get_rect(center=(1000, 700))
                self.window.blit(sideboard_title, text_rect)
            elif self.winner == 0:
                sideboard_title = myfont.render('TIE!', True, (72,68,68))
                text_rect = sideboard_title.get_rect(center=(1000, 650))
                self.window.blit(sideboard_title, text_rect)
            
            myfont = pygame.font.SysFont('', 40)
            sideboard_title = myfont.render('Press ENTER to continue', True, (72,68,68))
            text_rect = sideboard_title.get_rect(center=(1000, 750))
            self.window.blit(sideboard_title, text_rect)

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
        if self.board.board_as_string() in self.boards.keys():
            self.boards[self.board.board_as_string()] += 1
        else:
            self.boards.update({self.board.board_as_string() : 1})


    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            self.window.blit(GRAY_DOT,(SQUARE_SIZE*col+66,SQUARE_SIZE*row+66))

    def checkWin(self):
        if self.lastMove == None :
            return -1
        if self.boards[self.board.board_as_string()] == 3:
            self.winner = 0
            return 0   
        row, col = self.lastMove
        self.winner = self.board.threeInRow(row,col, 3-self.player)  
        return self.board.threeInRow(row,col, 3-self.player)

    def max_with_alpha_beta_cuts(self, lastRow, lastCol, maxDepth, alpha, beta, player):

        maxv = -2000

        depth = maxDepth - 1

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None


        result = self.board.threeInRow(lastRow, lastCol, player)
        x = random.randint(0,9)/10

        if result == player:
            return (-1000 - depth - x, 0, 0, 0, 0)

        if self.board.twoInRow(lastRow, lastCol, player) == player and depth == -1:
            #print("Entrei no max 2")
            #x = random.randint(0,9)/10
            return (-200 - depth - x, 0, 0, 0, 0)

        if self.board.twoPiecesClose(lastRow, lastCol, player) == player and depth == -1:
            #print("Entrei no max 3")
            #x = random.randint(0,9)/10
            return (-100 - depth - x, 0, 0, 0, 0)


        if depth == -1:
            return (0, 0, 0, 0, 0)

        if player == 1:
            pieces = deepcopy(self.board.get_white_pieces())

        else:
            pieces = deepcopy(self.board.get_black_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, min_old_row, min_old_col, min_row, min_col) = self.min_with_alpha_beta_cuts(moveRow, moveCol, depth, alpha, beta, 3 - player)

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


    def min_with_alpha_beta_cuts(self, lastRow, lastCol, maxDepth, alpha, beta, player):

        minv = 2000

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        depth = maxDepth - 1


        result = self.board.threeInRow(lastRow, lastCol, player)
        x = random.randint(0,9)/10

        if result == player:
            return (1000 + depth + x, 0, 0, 0, 0)

        if self.board.twoInRow(lastRow, lastCol, player) == player and depth == -1:
            #print("Entrei no min 2")
            #x = random.randint(0,9)/10
            return (200 + depth + x, 0, 0, 0, 0)

        if self.board.twoPiecesClose(lastRow, lastCol, player) == player and depth == -1:
            #print("Entrei no min 3")
            #x = random.randint(0,9)/10
            return (100 + depth + x, 0, 0, 0, 0)

        if depth == -1:
            return (0, 0, 0, 0, 0)


        if player == 1:
            pieces = deepcopy(self.board.get_white_pieces())

        else:
            pieces = deepcopy(self.board.get_black_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, max_old_row, max_old_col, max_row, max_col) = self.max_with_alpha_beta_cuts(moveRow, moveCol, depth, alpha, beta, 3- player)

                if m < minv:
                    minv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                if minv <= alpha :
                    return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)

                if minv < beta:
                    beta = minv

        return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)


    def max(self, lastRow, lastCol, maxDepth, player):

        maxv = -2000

        depth = maxDepth - 1

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None


        result = self.board.threeInRow(lastRow, lastCol, player)
        x = random.randint(0,9)/10

        if result == player:
            return (-1000 - depth - x, 0, 0, 0, 0)

        if self.board.twoInRow(lastRow, lastCol, player) == player and depth == -1:
            #x = random.randint(0,9)/10
            return (-100 - depth - x, 0, 0, 0, 0)


        if depth == -1:
            return (0, 0, 0, 0, 0)

        if player == 1:
            pieces = deepcopy(self.board.get_white_pieces())

        else:
            pieces = deepcopy(self.board.get_black_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, min_old_row, min_old_col, min_row, min_col) = self.min(moveRow, moveCol, depth, 3 - player)

                if m > maxv:
                    maxv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)
                

        return (maxv, finalOldRow, finalOldCol, finalRow, finalCol)

                    

    def min(self, lastRow, lastCol, maxDepth, player):

        minv = 2000

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        depth = maxDepth - 1


        result = self.board.threeInRow(lastRow, lastCol, player)
        x = random.randint(0,9)/10

        if result == player:
            return (1000 + depth + x, 0, 0, 0, 0)

        if self.board.twoInRow(lastRow, lastCol, player) == player and depth == -1:
            #x = random.randint(0,9)/10
            return (100 + depth + x, 0, 0, 0, 0)

        if depth == -1:
            return (0, 0, 0, 0, 0)


        if player == 1:
            pieces = deepcopy(self.board.get_white_pieces())

        else:
            pieces = deepcopy(self.board.get_black_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, max_old_row, max_old_col, max_row, max_col) = self.max_with_alpha_beta_cuts(moveRow, moveCol, depth, 3 - player)

                if m < minv:
                    minv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)


        return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)

    #negamax not working
    def max_for_negamax(self, lastRow, lastCol, maxDepth, alpha, beta, player, signal):
        
        maxv = -2000
        minv = 2000

        depth = maxDepth - 1

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None


        result = self.board.threeInRow(lastRow, lastCol, player)

        if result == player:
            x = random.randint(0,9)/10
            return (signal*1000 + signal*depth + signal*x, 0, 0, 0, 0)

        if self.board.twoInRow(lastRow, lastCol, player) == player and depth == -1:
            x = random.randint(0,9)/10
            return (signal*100 + signal*depth + signal*x, 0, 0, 0, 0)


        if depth == -1:
            return (0, 0, 0, 0, 0)

        if player == 1:
            pieces = deepcopy(self.board.get_white_pieces())

        else:
            pieces = deepcopy(self.board.get_black_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            for i in range(0,len(possibleMoves)):
                moveRow, moveCol = possibleMoves[i]
                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, min_old_row, min_old_col, min_row, min_col) = self.max_for_negamax(moveRow, moveCol, depth, alpha, beta, 3 - player, -signal)

                if m > maxv and signal > 0:
                    maxv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                if m < minv and signal < 0:
                    minv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol


                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                if maxv >= beta and signal > 0:
                    return (maxv, finalOldRow, finalOldCol, finalRow, finalCol)

                if maxv > alpha and signal > 0:
                    alpha = maxv

                if minv <= alpha and signal < 0:
                    return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)

                if minv < beta and signal < 0:
                    beta = minv
            
        if signal > 0:     
            return (maxv, finalOldRow, finalOldCol, finalRow, finalCol)

        elif signal < 0:
            return (minv, finalOldRow, finalOldCol, finalRow, finalCol)



    def negamax(self, lastRow, lastCol, maxDepth, alpha, beta, player):

        return self.max_for_negamax(lastRow, lastCol, maxDepth, alpha, beta, player, 1)
