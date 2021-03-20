import pygame
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
    clock = pygame.time.Clock()

    #board = Board()
    game = Game(WINDOW)
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row,col)
                if game.checkWin(row,col):
                    print("Vitória")
                    run = False

        game.update()
        
    
    pygame.quit()


main()