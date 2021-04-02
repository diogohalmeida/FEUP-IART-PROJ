# NEUTREEKO

## How to compile
1. You will need to install [Python3](https://www.python.org/downloads/) (we used Python 3.9.2)
2. You will need the [pygame](https://www.pygame.org/wiki/GettingStarted) and [pygame-menu](https://pygame-menu.readthedocs.io/en/4.0.1/) modules  

## How ro run
- In a Python IDE:
    -  press run.  

- In the command line, for windows, in the src directory:
```shell
python main.py
```  

- In the command line, for linux, in the src directory:
```shell
python3 main.py
```  

## How to use
1. Choose the game mode (player vs player, player vs computer, computer vs computer).
2. If you choose to play with at least one computer you can:
    - choose the difficulty level of the computer (easy, medium or hard)
    - choose the algorithm of the computer (Minimax or Minimax with alpha-beta cuts)
    - choose the node ordering system of the computer (best, worst or none)
3. Select play.
4. To make a move, if it's your turn, you can click on one of your pieces and click the dot in the position you want your piece to go.
5. For the computer to make a move, click the button on the right. After a computer play, some statistics will appear on the right, showing the number of nodes explored and the time it took to pick a move.
6. If you need a hint, click the button on the right and the right move will appear in green.
