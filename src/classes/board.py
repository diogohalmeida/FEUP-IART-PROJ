from constants import *

class Board:

    #Board class constructor
    def __init__(self):
        self.board = []
        self.blackPieces = []
        self.whitePieces = []
        self.create_board()

    #method that creates a list of lists to represent the board in the initial state
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col == 1 and row == 0) or (col == 3 and row == 0) or (col == 2 and row == 3):
                    self.board[row].append(2)
                    self.whitePieces.append((row,col))
                elif (col == 2 and row == 1) or (col == 1 and row == 4) or (col == 3 and row == 4):
                    self.board[row].append(1)
                    self.blackPieces.append((row,col))
                else:
                    self.board[row].append(0)

    #method that converts the list of lists into a string to be easier to verify if there is a tie in the game
    def board_as_string(self):
        result = ""
        for i in range(0,5):
            for j in range(0,5):
                result += str(self.board[i][j])

        return result

    #method to get the black pieces
    def get_black_pieces(self):
        return self.blackPieces

    #method to get the white pieces
    def get_white_pieces(self):
        return self.whitePieces

    #method that moves the piece in the position (oldRow, oldCol) to the new position (newRow, newCol)
    def move_piece(self,oldRow, oldCol, newRow, newCol):
        piece = self.board[oldRow][oldCol]
        
        if piece == 1:
            self.blackPieces.remove((oldRow,oldCol))
            self.blackPieces.append((newRow,newCol))

        else:
            self.whitePieces.remove((oldRow,oldCol))
            self.whitePieces.append((newRow,newCol))
       
        self.board[oldRow][oldCol] = 0
        self.board[newRow][newCol] = piece

    #method to get the piece in the position (row, col)    
    def get_piece(self,row,col):
        return self.board[row][col]
    
    #method that calculates the valid moves for a piece in the position (row,col)
    def get_valid_moves(self, row, col):
        moves = []
        #Left
        for c in range(col-1,-1,-1):
            if self.board[row][c] != 0:
                break

            elif c == 0:
                moves.append((row,c))
                break

            elif self.board[row][c-1] != 0:
                moves.append((row,c))
                break
        #Right
        for c in range(col+1,5):
            if(self.board[row][c] != 0):
                break

            elif c == 4:
                moves.append((row,c))
                break

            elif self.board[row][c+1] != 0:
                moves.append((row,c))
                break
        #Top
        for r in range(row-1,-1,-1):
            if self.board[r][col] != 0:
                break

            elif r == 0:
                moves.append((r,col))
                break

            elif self.board[r-1][col] != 0:
                moves.append((r,col))
                break

        #Bottom
        for r in range(row+1,5):
            if self.board[r][col] != 0:
                break

            elif r == 4:
                moves.append((r,col))
                break

            elif self.board[r+1][col] != 0:
                moves.append((r,col))
                break

        #TopLeft
        c = col-1
        r = row-1
        while c != -1 and r != -1:

            if self.board[r][c] != 0:
                break

            elif c == 0 or r == 0:
                moves.append((r,c))
                break

            elif self.board[r-1][c-1] != 0:
                moves.append((r,c))
                break

            c -= 1
            r -= 1

        #BottomLeft
        c = col-1
        r = row+1
        while c != -1 and r != 5:

            if self.board[r][c] != 0:
                break

            elif c == 0 or r == 4:
                moves.append((r,c))
                break

            elif self.board[r+1][c-1] != 0:
                moves.append((r,c))
                break

            c -= 1
            r += 1

        
        #TopRight
        c = col+1
        r = row-1
        while c != 5 and r != -1:

            if self.board[r][c] != 0:
                break

            elif c == 4 or r == 0:
                moves.append((r,c))
                break

            elif self.board[r-1][c+1] != 0:
                moves.append((r,c))
                break

            c += 1
            r -= 1
        
        #BottomRight
        c = col+1
        r = row+1
        while c != 5 and r != 5:

            if self.board[r][c] != 0:
                break

            elif c == 4 or r == 4:
                moves.append((r,c))
                break

            elif self.board[r+1][c+1] != 0:
                moves.append((r,c))
                break

            c += 1
            r += 1

        return moves

    #method that verifies if there is a three in a row given the last move made (row,col) by the player (piece)
    def threeInRow(self,row,col,piece):
        
        #TopLeft
        if row > 0 and col > 0:
            if self.board[row-1][col-1] == piece:
                if row > 1 and col > 1 and self.board[row-2][col-2] == piece:
                    return piece
                elif row < 4 and col < 4 and self.board[row+1][col+1] == piece:
                    return piece
        
        #Top
        if row > 0:
            if self.board[row-1][col] == piece:
                if row > 1 and self.board[row-2][col] == piece:
                    return piece
                elif row < 4 and self.board[row+1][col] == piece:
                    return piece

        #TopRight
        if row > 0 and col < 4:
            if self.board[row-1][col+1] == piece:
                if row > 1 and col < 3 and self.board[row-2][col+2] == piece:
                    return piece
                elif row < 4 and col > 0 and self.board[row+1][col-1] == piece:
                    return piece
        
        #Right
        if col < 4:
            if self.board[row][col+1] == piece:
                if col < 3 and self.board[row][col+2] == piece:
                    return piece
                elif col > 0 and self.board[row][col-1] == piece:
                    return piece

        #BottomRight
        if row < 4 and col < 4:
            if self.board[row+1][col+1] == piece:
                if row < 3 and col < 3 and self.board[row+2][col+2] == piece:
                    return piece
                elif row > 0 and col > 0 and self.board[row-1][col-1] == piece:
                    return piece

        #Bottom
        if row < 4:
            if self.board[row+1][col] == piece:
                if row < 3 and self.board[row+2][col] == piece:
                    return piece
                elif row > 0 and self.board[row-1][col] == piece:
                    return piece

        #BottomLeft
        if row < 4 and col > 0:
            if self.board[row+1][col-1] == piece:
                if row < 3 and col > 1 and self.board[row+2][col-2] == piece:
                    return piece
                elif row > 0 and col < 4 and self.board[row-1][col+1] == piece:
                    return piece


        #Left
        if col > 0:
            if self.board[row][col-1] == piece:
                if col > 1 and self.board[row][col-2] == piece:
                    return piece
                elif col < 4 and self.board[row][col+1] == piece:
                    return piece

        return -1

    #method that verifies if there is a two in a row given the last move made (row,col) by the player (piece)
    def twoInRow(self,row,col,piece):
        #TopLeft
        if row > 0 and col > 0:
            if self.board[row-1][col-1] == piece:
                return piece

        
        #Top
        if row > 0:
            if self.board[row-1][col] == piece:
                return piece

        #TopRight
        if row > 0 and col < 4:
            if self.board[row-1][col+1] == piece:
                return piece
        
        #Right
        if col < 4:
            if self.board[row][col+1] == piece:
                return piece

        #BottomRight
        if row < 4 and col < 4:
            if self.board[row+1][col+1] == piece:
                return piece

        #Bottom
        if row < 4:
            if self.board[row+1][col] == piece:
                return piece

        #BottomLeft
        if row < 4 and col > 0:
            if self.board[row+1][col-1] == piece:
                return piece


        #Left
        if col > 0:
            if self.board[row][col-1] == piece:
                return piece

        return -1

    #method that verifies if there is a space between two pieces in a row given the last move made (row,col) by the player (piece)
    def twoPiecesClose(self, row, col, piece):
        
        #TopLeft
        if row > 0 and col > 0:
            if self.board[row-1][col-1] == 0:
                if row > 1 and col > 1 and self.board[row-2][col-2] == piece:
                    return piece
        
        #Top
        if row > 0:
            if self.board[row-1][col] == 0:
                if row > 1 and self.board[row-2][col] == piece:
                    return piece


        #TopRight
        if row > 0 and col < 4:
            if self.board[row-1][col+1] == 0:
                if row > 1 and col < 3 and self.board[row-2][col+2] == piece:
                    return piece
                
        
        #Right
        if col < 4:
            if self.board[row][col+1] == 0:
                if col < 3 and self.board[row][col+2] == piece:
                    return piece
                

        #BottomRight
        if row < 4 and col < 4:
            if self.board[row+1][col+1] == 0:
                if row < 3 and col < 3 and self.board[row+2][col+2] == piece:
                    return piece
                

        #Bottom
        if row < 4:
            if self.board[row+1][col] == 0:
                if row < 3 and self.board[row+2][col] == piece:
                    return piece
        

        #BottomLeft
        if row < 4 and col > 0:
            if self.board[row+1][col-1] == 0:
                if row < 3 and col > 1 and self.board[row+2][col-2] == piece:
                    return piece


        #Left
        if col > 0:
            if self.board[row][col-1] == 0:
                if col > 1 and self.board[row][col-2] == piece:
                    return piece


        return -1