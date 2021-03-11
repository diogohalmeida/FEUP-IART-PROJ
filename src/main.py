import pygame
from constants import WIDTH, HEIGHT
from classes.board import Board

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board()
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        board.draw(WINDOW)
        pygame.display.update()
        
    
    pygame.quit()


main()