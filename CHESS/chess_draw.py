import pygame
from CHESS import chess_data as cd
from CHESS import Player, Piece

print('loading...')


BLACK, WHITE, grey, red, green, blue, tan = (20, 20, 20), (230, 230, 230), (120, 120, 120), (255, 0, 0), \
                                               (0, 255, 0), (0, 0, 255), (89, 45, 0)

pygame.font.init()

my_font2 = pygame.font.SysFont('Times', 15)
my_font3 = pygame.font.SysFont('comicsans', 40)

black_win = my_font2.render('White wins!', 1, green)
white_win = my_font2.render('Black wins!', 1, green)


board_labels = []

board_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
board_numbers = ['8', '7', '6', '5', '4', '3', '2', '1']

for x in range(8):
    board_labels.append(my_font3.render(board_letters[x], 1, WHITE))
for x in range(8):
    board_labels.append(my_font3.render(board_numbers[x], 1, WHITE))


def update_fps(clock):
    global fps_text
    fps = str(int(clock.get_fps())) + ' fps'
    fps_text = my_font2.render(fps, 1, green)


def draw_chessboard(display, white, black, game_over):
    display.fill(tan)

    chess_squares_upper = list(range(100, 800, cd.block_size * 2))
    chess_squares_lower = list(range(0, 900, cd.block_size * 2))

    for b in chess_squares_upper:
        for c in chess_squares_lower[0:4]:
            pygame.draw.rect(display, (210, 180, 140), (b + 150, c + 50, cd.block_size, cd.block_size))

    for b in chess_squares_lower[1:]:
        for c in chess_squares_upper:
            pygame.draw.rect(display, (210, 180, 140), (b + 150, c + 50, cd.block_size, cd.block_size))

    pygame.draw.rect(display, grey, (200, 0, 50, 900))
    pygame.draw.rect(display, grey, (200, 850, 900, 50))
    pygame.draw.rect(display, grey, (1050, 0, 50, 900))
    pygame.draw.rect(display, grey, (200, 0, 900, 50))
    pygame.draw.rect(display, WHITE, (250, 50, 800, 800), 3)
    pygame.draw.rect(display, WHITE, (200, 0, 900, 900), 3)
    pygame.draw.rect(display, BLACK, (0, 0, 200, 900))
    pygame.draw.rect(display, BLACK, (1100, 0, 200, 900))

    # display.blit(fps_text, (10, 20))


    # display moves on left
    # if Player.info and Player.info_lis:
    #     for x in Player.info_lis[:43]:
    #         display.blit(x[0], (10, (x[1] * 20) + 15))
    #     if len(Player.info_lis) >= 43:
    #         for x in Player.info_lis[43:]:
    #             display.blit(x[0], (110, (x[1] * 20) - 845))




    in_game_text = None

    if game_over:
        if white.mate:
            display.blit(black_win, (10, 10))
        elif black.mate:
            display.blit(white_win, (10, 10))
    else:
        if white.turn:
            in_game_text = my_font2.render('White\'s turn', 1, green)
        elif black.turn:
            in_game_text = my_font2.render('Black\'s turn', 1, green)

        # display.blit(in_game_text, (10, 10))

        # draw board labels
        for x in range(len(board_labels[0:8])):
            display.blit(board_labels[x], ((x * 100) + 292, 855))
        for x in range(8, len(board_labels[8:16]) + 8):
            display.blit(board_labels[x], (225, (x * 100) - 708))


# draws everything
def draw(display, game_over, pieces, white, black):

    draw_chessboard(display, white, black, game_over)

    for x in pieces:
        for y in x[1:]:
            if not y.is_taken:
                y.click_rect = cd.wk[1].get_rect(topleft=(y.position[0], y.position[1]))
                display.blit(y.sprite, y.position)

            else:
                if y.ID[0] == 'W':
                    pieces[0].remove(y)
                elif y.ID[0] == 'B':
                    pieces[1].remove(y)

    white.update(display)
    black.update(display)

    pygame.display.update()
