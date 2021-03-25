import pygame
import pygame_menu
from constants import WHITE_PIECE, BLACK_PIECE
from copy import deepcopy
import sys
sys.setrecursionlimit(1000)
pygame.init()

from constants import WIDTH, HEIGHT, SQUARE_SIZE
from classes.game import Game

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')


def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row,col

def main():
    run = True
    
    #clock = pygame.time.Clock()
    #board = Board()
    game = Game(WINDOW)
    
    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row,col)
                game.update()
                continue
                '''if game.checkWin() != -1:
                    print("Vitória")'''

        if game.getPlayer() == 2:
            row, col = game.getLastMove()
            (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, 6, -2000, 2000)
            game.selected = oldRow, oldCol
            game.ai_move(finalRow, finalCol)

        
        '''if game.checkWin():
            print("Vitória")
            run = False'''

        game.update()
        
    
    pygame.quit()


if __name__ == "__main__":
    main()