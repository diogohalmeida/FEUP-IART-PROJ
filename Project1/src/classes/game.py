import pygame
from constants import *
from classes.board import Board
from classes.button import Button
from copy import deepcopy
import random

class Game:

    #Game class constructor
    def __init__(self,window, gamemode):
        self._init()
        self.window = window
        self.lastMove = None
        self.winner = None
        self.gamemode = gamemode
        self.button = None
        self.time = None

    #method to update the game state
    def update(self, time_elapsed):
        if time_elapsed != None:
            self.time = time_elapsed
        
        self.drawBoard()
        self.drawSideBoard()
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    #private method to initialize class attributes
    def _init(self):
        self.selected = None
        self.board = Board()
        self.player = 1
        self.valid_moves = []
        self.lastMove = None
        self.boards = {}
        self.hintSquarePiece = None
        self.hintSquareToMove = None
        self.nodes = 0

    #method to draw the game board on screen
    def drawBoard(self):
        self.window.fill((76,188,228))
        
        for row in range(ROWS):
            for col in range(COLS):
                if (col, row) == self.hintSquarePiece:
                    pygame.draw.rect(self.window, GREEN, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 0)
                else:
                    pygame.draw.rect(self.window, BLUE, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 0)

                pygame.draw.rect(self.window, BLACK, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE), 1)


        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.board[row][col]
                if piece != 0:
                    self.window.blit(color_dic[piece], (SQUARE_SIZE * col - 10, SQUARE_SIZE * row - 10))

    #method to draw the right side of the screen
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
            

        if (self.gamemode == 3 and self.time != None):
            myfont = pygame.font.SysFont('', 40)
            sideboard_title = myfont.render("AI move took: " + str(round(self.time,5)) + " s", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 300))
            self.window.blit(sideboard_title, text_rect)
            sideboard_title = myfont.render("Visited nodes: " + str(self.nodes) + " nodes", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 350))
            self.window.blit(sideboard_title, text_rect)
        elif (self.gamemode == 1 and self.time != None):
            myfont = pygame.font.SysFont('', 40)
            sideboard_title = myfont.render("Hint calc. took: " + str(round(self.time,5)) + " s", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 300))
            self.window.blit(sideboard_title, text_rect)
            sideboard_title = myfont.render("Visited nodes: " + str(self.nodes) + " nodes", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 350))
            self.window.blit(sideboard_title, text_rect)
        elif (self.gamemode == 2 and self.time != None):
            myfont = pygame.font.SysFont('', 40)
            sideboard_title = myfont.render("Calculation took: " + str(round(self.time,5)) + " s", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 300))
            self.window.blit(sideboard_title, text_rect)
            sideboard_title = myfont.render("Visited nodes: " + str(self.nodes) + " nodes", True, BLACK)
            text_rect = sideboard_title.get_rect(center=(1000, 350))
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

    #method to reset the game state
    def reset(self):
       self._init()

    #method to get the current player (turn)
    def getPlayer(self):
        return self.player

    #method to get the last move made
    def getLastMove(self):
        return self.lastMove

    #method to get the current board
    def getBoard(self):
        return self.board

    #method to update the last move made
    def updateLastMove(self,row,col):
        self.lastMove = row,col

    #method that shows to the player what are the possible moves for the selected piece
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

    #method that moves a piece and changes turn
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

    #method that executes the ai move
    def ai_move(self, row, col):
        oldRow, oldCol = self.selected
        self.board.move_piece(oldRow,oldCol, row, col)
        self.updateLastMove(row,col)
        self.change_turn()

    #method that changes the turn
    def change_turn(self):
        self.valid_moves = []
        self.player = 3 - self.player
        self.hintSquarePiece = None
        self.hintSquareToMove = None
        if self.board.board_as_string() in self.boards.keys():
            self.boards[self.board.board_as_string()] += 1
        else:
            self.boards.update({self.board.board_as_string() : 1})

    #method that draws the valid moves on the screen
    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            if (row, col) == self.hintSquareToMove:
                self.window.blit(GREEN_DOT,(SQUARE_SIZE*col+66,SQUARE_SIZE*row+66))
            else:
                self.window.blit(GRAY_DOT,(SQUARE_SIZE*col+66,SQUARE_SIZE*row+66))

    #method that verifies if the game is over or not
    def checkWin(self):
        if self.lastMove == None :
            return -1
        if self.boards[self.board.board_as_string()] == 3:
            self.winner = 0
            return 0   
        row, col = self.lastMove
        self.winner = self.board.threeInRow(row,col, 3-self.player)  
        return self.board.threeInRow(row,col, 3-self.player)

    #method that evaluates the score of the board on easy level
    def easyLevelHeuristics(self, row, col, player):
        if self.board.threeInRow(row, col, player) == player:
            return 1000

        else:
            return 0

    #method that evaluates the score of the board on medium level
    def mediumLevelHeuristics(self, row, col, player):
        if self.board.threeInRow(row, col, player) == player:
            return 1000

        elif self.board.twoInRow(row, col, player) == player:
            return 200

        else:
            return 0

    #method that evaluates the score of the board on hard level (best heuristic)
    def hardLevelHeuristics(self, row, col, player):
        if self.board.threeInRow(row, col, player) == player:
            return 1000

        elif self.board.twoInRow(row, col, player) == player:
            return 200

        elif self.board.twoPiecesClose(row, col, player) == player:
            return 100

        else:
            return 0


    #method that chooses the heuristic according to the level selected in the menu
    def chooseHeuristics(self, level, row, col, player):
        if level == 1:
            return self.easyLevelHeuristics(row, col, player)
        elif level == 3:
            return self.mediumLevelHeuristics(row, col, player)
        elif level == 6:
            return self.hardLevelHeuristics(row, col, player)

    #method that implements the maximum part of the minimax with alpha-beta cuts algorithm 
    def max_with_alpha_beta_cuts(self, lastRow, lastCol, maxDepth, alpha, beta, player, ordering, level):

        maxv = -2000

        depth = maxDepth - 1

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        opponent = 3 - player

        result = self.chooseHeuristics(level, lastRow, lastCol, opponent)
        x = random.randint(0,9)/10

        if result == 1000:
            return (-result - depth - x, 0, 0, 0, 0)

        elif result != 1000 and depth == -1:
            return (-result - depth - x, 0, 0, 0, 0)


        if player == 1:
            pieces = deepcopy(self.board.get_black_pieces())

        else:
            pieces = deepcopy(self.board.get_white_pieces())


        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            orderedMoves = []

            if ordering != None:
                for i in range(0, len(possibleMoves)):
                    moveRow, moveCol = possibleMoves[i]
                    self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                    evaluation = self.chooseHeuristics(level, lastRow, lastCol, player)
                    orderedMoves.append((moveRow, moveCol, evaluation))

                    self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                orderedMoves = sorted(orderedMoves, key = lambda x: x[2], reverse=ordering)

            else:               
                orderedMoves = possibleMoves


            for i in range(0,len(orderedMoves)):
                self.nodes += 1
                if ordering != None:
                    moveRow, moveCol, score = orderedMoves[i]
                else:
                    moveRow, moveCol = orderedMoves[i]

                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, min_old_row, min_old_col, min_row, min_col) = self.min_with_alpha_beta_cuts(moveRow, moveCol, depth, alpha, beta, opponent, ordering, level)

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


    #method that implements the minimum part of the minimax with alpha-beta cuts algorithm 
    def min_with_alpha_beta_cuts(self, lastRow, lastCol, maxDepth, alpha, beta, player, ordering, level):

        minv = 2000

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        depth = maxDepth - 1

        opponent = 3 - player

        result = self.chooseHeuristics(level, lastRow, lastCol, opponent)
        x = random.randint(0,9)/10

        if result == 1000:
            return (result + depth + x, 0, 0, 0, 0)

        elif result != 1000 and depth == -1:
            return (result + depth + x, 0, 0, 0, 0)


        if player == 1:
            pieces = deepcopy(self.board.get_black_pieces())

        else:
            pieces = deepcopy(self.board.get_white_pieces())


        
        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            orderedMoves = []

            if ordering != None:
                for i in range(0, len(possibleMoves)):
                    moveRow, moveCol = possibleMoves[i]
                    self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                    evaluation = self.chooseHeuristics(level, lastRow, lastCol, player)
                    orderedMoves.append((moveRow, moveCol, evaluation))

                    self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                orderedMoves = sorted(orderedMoves, key = lambda x: x[2], reverse=ordering)

            else:               
                orderedMoves = possibleMoves

        
            for i in range(0,len(orderedMoves)):
                self.nodes += 1
                if ordering != None:
                    moveRow, moveCol, score = orderedMoves[i]
                else:
                    moveRow, moveCol = orderedMoves[i]

                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, max_old_row, max_old_col, max_row, max_col) = self.max_with_alpha_beta_cuts(moveRow, moveCol, depth, alpha, beta, opponent, ordering, level)

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


    #method that implements the maximum part of the minimax algorithm 
    def max(self, lastRow, lastCol, maxDepth, player, ordering, level):

        maxv = -2000

        depth = maxDepth - 1

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        opponent = 3 - player

        result = self.chooseHeuristics(level, lastRow, lastCol, opponent)
        x = random.randint(0,9)/10

        if result == 1000:
            return (-result - depth - x, 0, 0, 0, 0)

        elif result != 1000 and depth == -1:
            return (-result - depth - x, 0, 0, 0, 0)


        if player == 1:
            pieces = deepcopy(self.board.get_black_pieces())

        else:
            pieces = deepcopy(self.board.get_white_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            orderedMoves = []

            if ordering != None:
                for i in range(0, len(possibleMoves)):
                    moveRow, moveCol = possibleMoves[i]
                    self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                    evaluation = self.chooseHeuristics(level, lastRow, lastCol, player)
                    orderedMoves.append((moveRow, moveCol, evaluation))

                    self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                orderedMoves = sorted(orderedMoves, key = lambda x: x[2], reverse=ordering)

            else:               
                orderedMoves = possibleMoves 


            for i in range(0,len(orderedMoves)):
                self.nodes += 1
                
                if ordering != None:
                    moveRow, moveCol, score = orderedMoves[i]
                else:
                    moveRow, moveCol = orderedMoves[i]

                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, min_old_row, min_old_col, min_row, min_col) = self.min(moveRow, moveCol, depth, opponent, ordering, level)

                if m > maxv:
                    maxv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)
                

        return (maxv, finalOldRow, finalOldCol, finalRow, finalCol)

                    
    #method that implements the minimum part of the minimax algorithm 
    def min(self, lastRow, lastCol, maxDepth, player, ordering, level):

        minv = 2000

        finalRow = None
        finalCol = None
        finalOldRow = None
        finalOldCol = None

        depth = maxDepth - 1

        opponent = 3 - player

        result = self.chooseHeuristics(level, lastRow, lastCol, opponent)
        x = random.randint(0,9)/10

        if result == 1000:
            return (result + depth + x, 0, 0, 0, 0)

        elif result != 1000 and depth == -1:
            return (result + depth + x, 0, 0, 0, 0)


        if player == 1:
            pieces = deepcopy(self.board.get_black_pieces())

        else:
            pieces = deepcopy(self.board.get_white_pieces())

        for piece in pieces:
            oldRow, oldCol = piece
            possibleMoves = self.board.get_valid_moves(oldRow, oldCol)
            orderedMoves = []

            if ordering != None:
                for i in range(0, len(possibleMoves)):
                    moveRow, moveCol = possibleMoves[i]
                    self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                    evaluation = self.chooseHeuristics(level, lastRow, lastCol, player)
                    orderedMoves.append((moveRow, moveCol, evaluation))

                    self.board.move_piece(moveRow,moveCol, oldRow, oldCol)

                orderedMoves = sorted(orderedMoves, key = lambda x: x[2], reverse=ordering)

            else:               
                orderedMoves = possibleMoves

        
            for i in range(0,len(orderedMoves)):
                self.nodes += 1
                if ordering != None:
                    moveRow, moveCol, score = orderedMoves[i]
                else:
                    moveRow, moveCol = orderedMoves[i]

                self.board.move_piece(oldRow, oldCol, moveRow,moveCol)
                (m, max_old_row, max_old_col, max_row, max_col) = self.max(moveRow, moveCol, depth, opponent, ordering, level)

                if m < minv:
                    minv = m
                    finalRow = moveRow
                    finalCol = moveCol
                    finalOldRow = oldRow
                    finalOldCol = oldCol

                self.board.move_piece(moveRow,moveCol, oldRow, oldCol)


        return (minv, finalOldRow , finalOldCol ,finalRow, finalCol)
