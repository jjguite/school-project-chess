# this is not the final version of my chess project, which is why it includes a lot of commented out code that I haven't yet deleted.

import pygame
import time
import random
import numpy as np

from CHESS import Piece, Player
from CHESS import chess_data as cd
from CHESS import chess_draw as cw
from CHESS import chess_board as cb

from matplotlib import style
import matplotlib.pyplot as plt
import pickle
import os

# style.use('ggplot')


Piece.game_over = False
Piece.MOVE_COUNT = 0


def main():

    Piece.MOVE_COUNT = 0
    cd.render = True

    win_count = 0

    # inits pieces
    pieces = Player.reset()

    PlayerWhite = Player.Player('minimax', 'white', 'W', True, pieces)
    PlayerBlack = Player.Player('random', 'black', 'B', False, pieces)

    pieces_list = []
    for x in pieces:
        for y in x[1:]:
            pieces_list.append(y)

    time.sleep(5)

    board = cb.ChessBoard()
    board.update_board(pieces_list)

    if cd.render:
        pygame.init()

        game_display = pygame.display.set_mode((1300, 900))

        pygame.display.set_caption('Chess')

        clock = pygame.time.Clock()


    # if cd.GAME_MODE != 0:
    #     print('White\'s turn')
    #     print('Drag & Drop the piece you want to move!')


    cd.game_over = False
    while not cd.game_over:
        def remove():
            for x in pieces_list:
                if x.is_taken:
                    pieces_list.remove(x)


        # white's turn
        if PlayerWhite.turn:
            print('WHITE MOVE')
            # time.sleep(3)

            if not cd.render:
                PlayerWhite.move(pieces, PlayerWhite, PlayerBlack, True, pieces_list, board=board)
                remove()

            else:
                cw.draw(game_display, cd.game_over, pieces, PlayerWhite, PlayerBlack)

                # cw.update_fps(clock)

                # mx, my = pygame.mouse.get_pos()

                ev = pygame.event.get()

                for event in ev:
                    if event.type == pygame.QUIT:
                        break

                start = time.process_time()

                PlayerWhite.move(pieces, PlayerWhite, PlayerBlack, True, pieces_list, ev=ev, board=board)
                remove()

                print(time.process_time() - start, 'sec')
                print('END WHITE MOVE')
                print()

            PlayerWhite.check_for_win()
            PlayerBlack.check_for_win()


        # black turn
        elif PlayerBlack.turn:
            print('BLACK MOVE')
            # time.sleep(3)

            if not cd.render:
                PlayerBlack.move(pieces, PlayerWhite, PlayerBlack, True, pieces_list, board=board)
                remove()

            else:
                cw.draw(game_display, cd.game_over, pieces, PlayerWhite, PlayerBlack)

                # cw.update_fps(clock)

                # mx, my = pygame.mouse.get_pos()

                ev = pygame.event.get()

                for event in ev:
                    if event.type == pygame.QUIT:
                        break

                start = time.process_time()

                PlayerBlack.move(pieces, PlayerWhite, PlayerBlack, True, pieces_list, ev=ev, board=board)
                remove()

                print(time.process_time() - start, 'sec')
                print('END BLACK MOVE')
                print()

            PlayerWhite.check_for_win()
            PlayerBlack.check_for_win()

        else:
            pygame.display.update()

        print(cd.MOVE_COUNT + 1)

        cw.draw(game_display, cd.game_over, pieces, PlayerWhite, PlayerBlack)

        pygame.display.update()

    while cd.game_over:

        cw.draw(game_display, cd.game_over, pieces, PlayerWhite, PlayerBlack)

        pygame.display.update()

        # print()
        # print("type 'quit' to close the game")

        # if input().lower().strip() == 'quit':
        #     pygame.quit()

        # time.sleep(20)

        # pygame.display.quit()


main()


pygame.quit()

quit()


