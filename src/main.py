import pygame
import pygame_menu
import time
import datetime
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
settings = "pvp"
diff_pvc = 1
diff_cvc_1 = 1
diff_cvc_2 = 1
algo = 1
algo_PC1 = 1
algo_PC2 = 1
mode = 1
order = True
order_PC1 = True
order_PC2 = True


def set_difficulty(value, difficulty):
    global diff_pvc
    diff_pvc = difficulty

def set_difficulty_PC1(value, difficulty):
    global diff_cvc_1
    diff_cvc_1 = difficulty

def set_difficulty_PC2(value, difficulty):
    global diff_cvc_2
    diff_cvc_2 = difficulty

def set_algorithm(value, algorithm):
    global algo
    algo = algorithm

def set_algorithm_PC1(value, algorithm):
    global algo_PC1
    algo_PC1 = algorithm

def set_algorithm_PC2(value, algorithm):
    global algo_PC2 
    algo_PC2 = algorithm

def set_ordering(value, ordering):
    global order
    order = ordering

def set_ordering_PC1(value, ordering):
    global order_PC1
    order_PC1 = ordering

def set_ordering_PC2(value, ordering):
    global order_PC2
    order_PC2 = ordering


def set_gamemode(value, gamemode):
    global settings
    global mode
    menu.remove_widget(quit_button)
    if gamemode == 1 and settings == "pvc":
        settings = "pvp"
        mode = 1
        menu.remove_widget(difficulty_selector)
        menu.remove_widget(algorithm_selector)
        menu.remove_widget(ordering_selector)
    elif gamemode == 1 and settings == "cvc":
        settings = "pvp"
        mode = 1
        menu.remove_widget(difficulty_selector_PC1)
        menu.remove_widget(difficulty_selector_PC2)
        menu.remove_widget(algorithm_selector_PC1)
        menu.remove_widget(algorithm_selector_PC2)
        menu.remove_widget(ordering_selector_PC1)
        menu.remove_widget(ordering_selector_PC2)
    elif gamemode == 2 and settings == "pvp":
        mode = 2
        settings = "pvc"
        menu.add_generic_widget(difficulty_selector)
        menu.add_generic_widget(algorithm_selector)
        menu.add_generic_widget(ordering_selector)
    elif gamemode == 2 and settings == "cvc":
        settings = "pvc"
        mode = 2
        menu.add_generic_widget(difficulty_selector)
        menu.add_generic_widget(algorithm_selector)
        menu.add_generic_widget(ordering_selector)
        menu.remove_widget(difficulty_selector_PC1)
        menu.remove_widget(difficulty_selector_PC2)
        menu.remove_widget(algorithm_selector_PC1)
        menu.remove_widget(algorithm_selector_PC2)
        menu.remove_widget(ordering_selector_PC1)
        menu.remove_widget(ordering_selector_PC2)
    elif gamemode == 3 and settings == "pvp":
        settings = "cvc"
        mode = 3
        menu.add_generic_widget(difficulty_selector_PC1)
        menu.add_generic_widget(difficulty_selector_PC2)
        menu.add_generic_widget(algorithm_selector_PC1)
        menu.add_generic_widget(algorithm_selector_PC2)
        menu.add_generic_widget(ordering_selector_PC1)
        menu.add_generic_widget(ordering_selector_PC2)
    elif  gamemode == 3 and settings == "pvc":
        settings = "cvc"
        mode = 3
        menu.remove_widget(difficulty_selector)
        menu.remove_widget(algorithm_selector)
        menu.remove_widget(ordering_selector)
        menu.add_generic_widget(difficulty_selector_PC1)
        menu.add_generic_widget(difficulty_selector_PC2)
        menu.add_generic_widget(algorithm_selector_PC1)
        menu.add_generic_widget(algorithm_selector_PC2)
        menu.add_generic_widget(ordering_selector_PC1)
        menu.add_generic_widget(ordering_selector_PC2)

    menu.add_generic_widget(quit_button)


def plaverVSPlayer():
    run = True
    finished = False
    game = Game(WINDOW, 1)
    time_elapsed = None
    firstMove = True

    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and finished:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if x <= 800:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row,col)
                    if game.checkWin() != -1:
                        finished = True
                elif game.button.isOver(pos):
                    #Hint for Player vs Player
                    if not firstMove:
                        row, col = game.getLastMove()
                    else:
                        row = 0
                        col = 0
                        firstMove = False
                    game.nodes = 0
                    start_time = time.perf_counter()
                    (m, oldRow , oldCol , finalRow, finalCol) = game.max_with_alpha_beta_cuts(row, col, 6, -2000, 2000, game.getPlayer(), True, 6)
                    end_time = time.perf_counter()
                    
                    time_elapsed = end_time-start_time

                    game.hintSquarePiece = (oldRow, oldCol)
                    game.hintSquareToMove = (finalRow, finalCol)
                
    
        game.update(time_elapsed)
    
   
def pcVSPc():
    global diff_cvc_1
    global diff_cvc_2
    global algo_PC1
    global algo_PC2
    global order_PC1
    global order_PC2

    run = True
    game = Game(WINDOW, 3)
    firstMove = True
    finished = False
    time_elapsed = None
    
    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and finished:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if game.button.isOver(pos) and game.getPlayer() == 1:   
                    if not firstMove:
                        row, col = game.getLastMove()
                    else:
                        row = 0
                        col = 0
                        firstMove = False

                    if algo_PC1 == 1:

                        if diff_cvc_1 == 6:
                            depth = 5
                        else:
                            depth = diff_cvc_1

                        game.nodes = 0
                        start_time = time.perf_counter()
                        (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, depth, game.getPlayer(), order_PC1, diff_cvc_1)
                        end_time = time.perf_counter()

                    elif algo_PC1 == 2:
                        game.nodes = 0
                        start_time = time.perf_counter()
                        (m, oldRow , oldCol , finalRow, finalCol) = game.max_with_alpha_beta_cuts(row, col, diff_cvc_1, -2000, 2000, game.getPlayer(), order_PC1,diff_cvc_1)
                        end_time = time.perf_counter()

                    time_elapsed = end_time-start_time
                    print("Elapsed time: ", time_elapsed)

                    game.selected = oldRow, oldCol
                    game.ai_move(finalRow, finalCol)
                    if game.checkWin() != -1:
                        finished = True
                
                elif game.button.isOver(pos) and game.getPlayer() == 2:
                    row, col = game.getLastMove()
                    
                    if algo_PC2 == 1:

                        if diff_cvc_2 == 6:
                            depth = 5
                        else:
                            depth = diff_cvc_2
                        
                        game.nodes = 0
                        start_time = time.perf_counter()
                        (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, depth, game.getPlayer(), order_PC2, diff_cvc_2)
                        end_time = time.perf_counter()

                    elif algo_PC2 == 2:
                        game.nodes = 0
                        start_time = time.perf_counter()
                        (m, oldRow , oldCol , finalRow, finalCol) = game.max_with_alpha_beta_cuts(row, col, diff_cvc_2, -2000, 2000, game.getPlayer(), order_PC2, diff_cvc_2)
                        end_time = time.perf_counter()


                    time_elapsed = end_time-start_time
                    print("Elapsed time: ", time_elapsed)
                    
                    game.selected = oldRow, oldCol
                    game.ai_move(finalRow, finalCol)
                    if game.checkWin() != -1:
                        finished = True
                
                
    
        game.update(time_elapsed)
    

def playerVSPc():
    global diff_pvc
    global order
    run = True

    game = Game(WINDOW, 2)
    finished = False
    firstMove = True
    time_elapsed = None
    
    while run:
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and finished:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if x <= 800 and game.getPlayer() == 1 and not finished:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row,col)
                    if game.checkWin() != -1:
                        finished = True
                elif game.button.isOver(pos) and game.getPlayer() == 1:
                    #Hint for Player vs PC
                    if not firstMove:
                        row, col = game.getLastMove()
                    else:
                        row = 0
                        col = 0
                        firstMove = False

                    game.nodes = 0
                    start_time = time.perf_counter()
                    (m, oldRow , oldCol , finalRow, finalCol) = game.max_with_alpha_beta_cuts(row, col, 6, -2000, 2000, game.getPlayer(), True, 6)
                    end_time = time.perf_counter()

                    time_elapsed = end_time-start_time
                    game.hintSquarePiece = (oldRow, oldCol)
                    game.hintSquareToMove = (finalRow, finalCol)
                
                elif game.button.isOver(pos) and game.getPlayer() == 2:
                    row, col = game.getLastMove()
                    
                    if algo == 1:
                        if diff_pvc == 6:
                            depth = 5
                        else:
                            depth = diff_pvc
                        game.nodes = 0
                        start_time = time.perf_counter()
                        (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, depth, game.getPlayer(), order, diff_pvc)
                        end_time = time.perf_counter()

                    elif algo == 2:
                        game.nodes = 0
                        start_time = time.perf_counter()
                        (m, oldRow , oldCol , finalRow, finalCol) = game.max_with_alpha_beta_cuts(row, col, diff_pvc, -2000, 2000, game.getPlayer(), order, diff_pvc)
                        end_time = time.perf_counter()

                    time_elapsed = end_time-start_time
                    print("Elapsed time: ", time_elapsed)
                    
                    game.selected = oldRow, oldCol
                    game.ai_move(finalRow, finalCol)
                    if game.checkWin() != -1:
                        finished = True
                
                

        game.update(time_elapsed)


def start_the_game():
    global diff_pvc
    global diff_cvc_1
    global diff_cvc_2
    global mode
    
    if mode == 1:
        plaverVSPlayer()
    elif mode == 2:
        playerVSPc()
    elif mode == 3:
        pcVSPc()


def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row,col


def main():
    run = True

    menu.mainloop(WINDOW)
    
    pygame.quit()


mytheme = pygame_menu.themes.THEME_DEFAULT.copy()

myimage = pygame_menu.baseimage.BaseImage(image_path='assets/bg.png', drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)

mytheme.background_color = myimage
mytheme.widget_font = pygame_menu.font.FONT_NEVIS
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
mytheme.title_background_color = (76,188,228, 100)
mytheme.title_font_size = 70
mytheme.title_font_color = (250,250,250)
mytheme.title_font = pygame_menu.font.FONT_NEVIS
mytheme.widget_font_size = 45
mytheme.widget_margin = (0,30)
mytheme.widget_padding = 10

menu = pygame_menu.Menu(HEIGHT, WIDTH, 'NEUTREEKO', theme=mytheme)
menu.add.button('Play', start_the_game)
menu.add.selector('Game Mode ', [('Player vs Player', 1), ('Player vs Computer', 2), ('Computer vs Computer', 3)], onchange=set_gamemode)
difficulty_selector = menu.add.selector('Computer Difficulty ', [('Easy', 1), ('Medium', 3), ('Hard', 6)], onchange=set_difficulty)
difficulty_selector_PC1 = menu.add.selector('Computer 1 (Black) Difficulty ', [('Easy', 1), ('Medium', 3), ('Hard', 6)], onchange=set_difficulty_PC1)
difficulty_selector_PC2 = menu.add.selector('Computer 2 (White) Difficulty ', [('Easy', 1), ('Medium', 3), ('Hard', 6)], onchange=set_difficulty_PC2)
algorithm_selector = menu.add.selector('Algorithm ', [('Minimax', 1), ('Minimax w/ Alpha/Beta Cuts', 2)], onchange=set_algorithm)
algorithm_selector_PC1 = menu.add.selector('Algo. Comp. 1 ', [('Minimax', 1), ('Minimax w/ Alpha/Beta Cuts', 2)], onchange=set_algorithm_PC1)
algorithm_selector_PC2 = menu.add.selector('Algo. Comp. 2 ', [('Minimax', 1), ('Minimax w/ Alpha/Beta Cuts', 2)], onchange=set_algorithm_PC2)
ordering_selector = menu.add.selector('Ordering ', [('Best', True), ('Worst', False), ('None', None)], onchange=set_ordering)
ordering_selector_PC1 = menu.add.selector('Ordering Computer 1 ', [('Best', True), ('Worst', False), ('None', None)], onchange=set_ordering_PC1)
ordering_selector_PC2 = menu.add.selector('Ordering Computer 2 ', [('Best', True), ('Worst', False), ('None', None)], onchange=set_ordering_PC2)
menu.remove_widget(difficulty_selector)
menu.remove_widget(difficulty_selector_PC1)
menu.remove_widget(difficulty_selector_PC2)
menu.remove_widget(algorithm_selector)
menu.remove_widget(algorithm_selector_PC1)
menu.remove_widget(algorithm_selector_PC2)
menu.remove_widget(ordering_selector)
menu.remove_widget(ordering_selector_PC1)
menu.remove_widget(ordering_selector_PC2)
quit_button = menu.add.button('Quit', pygame_menu.events.EXIT)


if __name__ == "__main__":
    main()