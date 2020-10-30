import pygame
import time

from CHESS import chess_data as cd
from CHESS import chess_draw as cw
# from CHESS import chess_board as cb



rem = []
pieces_pos = []


class Piece(object):
    def __init__(self, ID, position, key, value):

        self.ID = ID
        self.position = position
        self.key = key
        self.value = value
        self.is_taken = False
        self.sprite = None

        # for collecting valid moves
        self.uncut_valid_moves = []
        self.valid_moves = []

        # variables for human movement
        self.click = False
        self.move_count = 0
        self.init_position = []
        self.click_rect = cd.wk[1].get_rect(topleft=(self.position[0], self.position[1]))

    # not using anymore
    def human_piece_movement(self, ev, pieces):  # allows HUMAN piece movement

        global mx, my, MOVE_COUNT, SWITCH

        if not self.is_taken:
            if not cd.game_over:
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.click_rect.collidepoint(event.pos):
                            if self.click_rect[0] == self.position[0]:
                                if self.click_rect[1] == self.position[1]:
                                    self.init_position = self.position.copy()
                                    self.click = True
                                    self.find_valid_moves(pieces)


                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.click = False

                        adj0, adj1 = 0, 0
                        if [10000, 10000] not in self.valid_moves:
                            if round(self.position[0] / 100) * 100 > self.position[0]:
                                adj0 = -40
                            else:
                                adj0 = 60

                            if round(self.position[1] / 100) * 100 > self.position[1]:
                                adj1 = -40
                            else:
                                adj1 = 60

                        self.position = [((round(self.position[0] / 100)) * 100) + adj0,
                                         ((round(self.position[1] / 100)) * 100) + adj1]
                        # if move is valid:
                        if self.position in self.valid_moves:

                            print(f'{MOVE_COUNT + 1}: {self.ID}, {cd.board_labels_dict[str(self.init_position)]} ---> '
                                  f'{cd.board_labels_dict[str(self.position)]}')
                            print()
                            self.valid_moves = []

                            # check for check

                            for colors in pieces:
                                for piece in colors[1:]:
                                    if self.position == piece.position:
                                        if self.ID[0] != piece.ID[0]:
                                            piece.is_taken = True
                                            self.move_count += 1
                                            SWITCH = True

                                        else:
                                            if self.ID != piece.ID:
                                                print('invalid move')
                                                self.position = self.init_position.copy()

                                    else:
                                        self.move_count += 1
                                        SWITCH = True


                        else:
                            # move piece back to original position
                            if self.valid_moves:
                                print('invalid move')
                                self.position = self.init_position.copy()
                                self.valid_moves = []

                    if event.type == pygame.MOUSEMOTION:
                        if self.click:
                            self.position = [mx - 40, my - 40]
                            self.click_rect[0], self.click_rect[1] = self.position[0], self.position[1]

    def find_valid_moves(self, board=None, pieces=None, pieces_list=None):
        possible_positions = []

        if pieces:
            def bishop_valid():
                global possible_positions

                def valid():
                    for x in sorted(self.uncut_valid_moves,
                                    key=lambda x: abs(self.position[0] - x[0]) + abs(self.position[1] - x[1])):

                        self.valid_moves.append(x)

                        for y in pieces:
                            for z in y[1:]:
                                if x == z.position:
                                    return

                for x in range(-8, 0):
                    if 200 < self.position[0] + (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] + (100 * x), self.position[1]] != self.position:
                            possible_positions.append([self.position[0] + (100 * x), self.position[1] + (100 * x)])
                            self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1] + (100 * x)])
                for x in range(-8, 0):
                    if 200 < self.position[0] + (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] + (100 * x), self.position[1]] != self.position:
                            if all(b.position != n for n in possible_positions for a in pieces for b in a[1:]):
                                self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

                # bottom right
                for x in range(9):
                    if 200 < self.position[0] + (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] + (100 * x), self.position[1] + (100 * x)] != self.position:
                            possible_positions.append([self.position[0] + (100 * x), self.position[1] + (100 * x)])
                            self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1] + (100 * x)])

                for x in range(9):
                    if 200 < self.position[0] + (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] + (100 * x), self.position[1] + (100 * x)] != self.position:
                            if all(b.position != n for n in possible_positions for a in pieces for b in a[1:]):
                                self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

                # positive slope
                # top right
                for x in range(-8, 0):
                    if 200 < self.position[0] - (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] - (100 * x), self.position[1] + (100 * x)] != self.position:
                            possible_positions.append([self.position[0] - (100 * x), self.position[1] + (100 * x)])
                            self.uncut_valid_moves.append([self.position[0] - (100 * x), self.position[1] + (100 * x)])

                for x in range(-8, 0):
                    if 200 < self.position[0] - (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] - (100 * x), self.position[1] + (100 * x)] != self.position:
                            if all(b.position != n for n in possible_positions for a in pieces for b in a[1:]):
                                self.uncut_valid_moves.append([self.position[0] - (100 * x), self.position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

                # bottom left
                for x in range(9):
                    if 200 < self.position[0] - (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] - (100 * x), self.position[1] + (100 * x)] != self.position:
                            possible_positions.append([self.position[0] - (100 * x), self.position[1] + (100 * x)])
                            self.uncut_valid_moves.append([self.position[0] - (100 * x), self.position[1] + (100 * x)])
                for x in range(9):
                    if 200 < self.position[0] - (100 * x) < 1000 and 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0] - (100 * x), self.position[1] + (100 * x)] != self.position:
                            if all(b.position != n for n in possible_positions for a in pieces for b in a[1:]):
                                self.uncut_valid_moves.append([self.position[0] - (100 * x), self.position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

            def rook_valid():
                global possible_positions

                def valid_horizontal():
                    for x in sorted(self.uncut_valid_moves, key=lambda x: abs(self.position[0] - x[0])):

                        self.valid_moves.append(x)

                        for y in pieces:
                            for z in y[1:]:
                                if x == z.position:
                                    return

                def valid_vertical():
                    for x in sorted(self.uncut_valid_moves, key=lambda x: abs(self.position[1] - x[1])):

                        self.valid_moves.append(x)

                        for y in pieces:
                            for z in y[1:]:
                                if x == z.position:
                                    return

                # rook

                # horizontal
                # left
                for x in range(-8, 0):
                    if 200 < self.position[0] + (100 * x) < 1000:
                        if [self.position[0] + (100 * x), self.position[1]] != self.position:
                            possible_positions.append([self.position[0] + (100 * x), self.position[1]])
                            self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1]])
                for x in range(-8, 0):
                    if 200 < self.position[0] + (100 * x) < 1000:
                        if [self.position[0] + (100 * x), self.position[1]] != self.position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1]])

                valid_horizontal()

                possible_positions = []
                self.uncut_valid_moves = []

                # right
                for x in range(9):
                    if 200 < self.position[0] + (100 * x) < 1000:
                        if [self.position[0] + (100 * x), self.position[1]] != self.position:
                            possible_positions.append([self.position[0] + (100 * x), self.position[1]])
                            self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1]])
                for x in range(9):
                    if 200 < self.position[0] + (100 * x) < 1000:
                        if [self.position[0] + (100 * x), self.position[1]] != self.position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([self.position[0] + (100 * x), self.position[1]])

                valid_horizontal()

                possible_positions = []
                self.uncut_valid_moves = []

                # vertical
                # up
                for x in range(-8, 0):
                    if 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0], self.position[1] + (100 * x)] != self.position:
                            possible_positions.append([self.position[0], self.position[1] + (100 * x)])
                            self.uncut_valid_moves.append([self.position[0], self.position[1] + (100 * x)])
                for x in range(-8, 0):
                    if 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0], self.position[1] + (100 * x)] != self.position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([self.position[0], self.position[1] + (100 * x)])

                valid_vertical()

                possible_positions = []
                self.uncut_valid_moves = []

                # down
                for x in range(8):
                    if 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0], self.position[1] + (100 * x)] != self.position:
                            possible_positions.append([self.position[0], self.position[1] + (100 * x)])
                            self.uncut_valid_moves.append([self.position[0], self.position[1] + (100 * x)])
                for x in range(8):
                    if 0 < self.position[1] + (100 * x) < 800:
                        if [self.position[0], self.position[1] + (100 * x)] != self.position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([self.position[0], self.position[1] + (100 * x)])

                valid_vertical()

                possible_positions = []
                self.uncut_valid_moves = []

            # knight movement rules
            if len(self.ID) == 3:
                for x in [-2, 2]:
                    for y in [-1, 1]:
                        if 200 <= self.position[0] + (x * 100) <= 1000:
                            self.valid_moves.append([self.position[0] + (x * 100), self.position[1] + (y * 100)])
                        if 200 <= self.position[0] + (y * 100) <= 1000:
                            self.valid_moves.append([self.position[0] + (y * 100), self.position[1] + (x * 100)])

            else:
                # king movement rules
                if self.ID[1] == 'K':
                    for c in range(-1, 2):
                        for d in range(-1, 2):
                            if 0 <= self.position[1] + (d * 100) <= 800:
                                if 200 <= self.position[0] + (c * 100) <= 1000:
                                    if [self.position[0] + (c * 100), self.position[1] + (d * 100)] != self.position:
                                        self.valid_moves.append(
                                            [self.position[0] + (c * 100), self.position[1] + (d * 100)])

                                        # castling
                                        # if self.move_count == 0:
                                        #     self.valid_moves.append([self.position[0] + 200, self.position[1]])
                                        #     self.valid_moves.append([self.position[0] - 200, self.position[1]])

                # bishop movement rules
                if self.ID[1] == 'B':
                    bishop_valid()

                # rook movement rules
                if self.ID[1] == 'R':
                    rook_valid()

                # queen movement rules
                if self.ID[1] == 'Q':
                    bishop_valid()
                    rook_valid()

                # pawn movement rules
                if self.ID[1] == 'P':

                    if self.ID[0] == 'W':
                        for colors in pieces:
                            for piece in colors[1:]:
                                if self.ID[0] != piece.ID[0]:
                                    if [self.position[0] + 100, self.position[1] - 100] == piece.position:
                                        self.valid_moves.append(piece.position)
                                    elif [self.position[0] - 100, self.position[1] - 100] == piece.position:
                                        self.valid_moves.append(piece.position)

                        if all([self.position[0], self.position[1] - 100] != piece.position for colors in pieces for piece
                               in colors[1:]):
                            self.valid_moves.append([self.position[0], self.position[1] - 100])
                            if all([self.position[0], self.position[1] - 200] != piece.position for colors in pieces for
                                   piece in colors[1:]):
                                if self.move_count == 0:
                                    self.valid_moves.append([self.position[0], self.position[1] - 200])

                    elif self.ID[0] == 'B':
                        for colors in pieces:
                            for piece in colors[1:]:
                                if self.ID[0] != piece.ID[0]:
                                    if [self.position[0] + 100, self.position[1] + 100] == piece.position:
                                        self.valid_moves.append(piece.position)
                                    if [self.position[0] - 100, self.position[1] + 100] == piece.position:
                                        self.valid_moves.append(piece.position)

                        if all([self.position[0], self.position[1] + 100] != piece.position for colors in pieces for piece
                               in colors[1:]):
                            self.valid_moves.append([self.position[0], self.position[1] + 100])
                            if all([self.position[0], self.position[1] + 200] != piece.position for colors in pieces for
                                   piece in colors[1:]):
                                if self.move_count == 0:
                                    self.valid_moves.append([self.position[0], self.position[1] + 200])

        elif pieces_list:
            # for x in board.board:
            #     print(x)
            # print('get_piece:', board.get_piece(self.key))
            position = board.get_piece(self.key)[0]

            # time.sleep(1000)

            def bishop_valid():
                global possible_positions

                def valid():
                    for x in sorted(self.uncut_valid_moves,
                                    key=lambda x: abs(position[0] - x[0]) + abs(position[1] - x[1])):

                        self.valid_moves.append(x)

                        for y in pieces_list:
                            if x == y.position:
                                return

                for x in range(-8, 0):
                    if 200 < position[0] + (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] + (100 * x), position[1]] != position:
                            possible_positions.append([position[0] + (100 * x), position[1] + (100 * x)])
                            self.uncut_valid_moves.append([position[0] + (100 * x), position[1] + (100 * x)])
                for x in range(-8, 0):
                    if 200 < position[0] + (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] + (100 * x), position[1]] != position:
                            if all(a.position != n for n in possible_positions for a in pieces_list):
                                self.uncut_valid_moves.append(
                                    [position[0] + (100 * x), position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

                # bottom right
                for x in range(9):
                    if 200 < position[0] + (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] + (100 * x), position[1] + (100 * x)] != position:
                            possible_positions.append([position[0] + (100 * x), position[1] + (100 * x)])
                            self.uncut_valid_moves.append([position[0] + (100 * x), position[1] + (100 * x)])

                for x in range(9):
                    if 200 < position[0] + (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] + (100 * x), position[1] + (100 * x)] != position:
                            if all(a.position != n for n in possible_positions for a in pieces_list):
                                self.uncut_valid_moves.append(
                                    [position[0] + (100 * x), position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

                # positive slope
                # top right
                for x in range(-8, 0):
                    if 200 < position[0] - (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] - (100 * x), position[1] + (100 * x)] != position:
                            possible_positions.append([position[0] - (100 * x), position[1] + (100 * x)])
                            self.uncut_valid_moves.append([position[0] - (100 * x), position[1] + (100 * x)])

                for x in range(-8, 0):
                    if 200 < position[0] - (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] - (100 * x), position[1] + (100 * x)] != position:
                            if all(a.position != n for n in possible_positions for a in pieces_list):
                                self.uncut_valid_moves.append(
                                    [position[0] - (100 * x), position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

                # bottom left
                for x in range(9):
                    if 200 < position[0] - (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] - (100 * x), position[1] + (100 * x)] != position:
                            possible_positions.append([position[0] - (100 * x), position[1] + (100 * x)])
                            self.uncut_valid_moves.append([position[0] - (100 * x), position[1] + (100 * x)])
                for x in range(9):
                    if 200 < position[0] - (100 * x) < 1000 and 0 < position[1] + (100 * x) < 800:
                        if [position[0] - (100 * x), position[1] + (100 * x)] != position:
                            if all(a.position != n for n in possible_positions for a in pieces_list):
                                self.uncut_valid_moves.append(
                                    [position[0] - (100 * x), position[1] + (100 * x)])

                valid()

                possible_positions = []
                self.uncut_valid_moves = []

            def rook_valid():
                global possible_positions

                def valid_horizontal():
                    for x in sorted(self.uncut_valid_moves, key=lambda x: abs(position[0] - x[0])):

                        self.valid_moves.append(x)

                        for y in pieces_list:
                            if x == y.position:
                                return

                def valid_vertical():
                    for x in sorted(self.uncut_valid_moves, key=lambda x: abs(position[1] - x[1])):

                        self.valid_moves.append(x)

                        for y in pieces_list:
                            if x == y.position:
                                return

                # rook

                # horizontal
                # left
                for x in range(-8, 0):
                    if 200 < position[0] + (100 * x) < 1000:
                        if [position[0] + (100 * x), position[1]] != position:
                            possible_positions.append([position[0] + (100 * x), position[1]])
                            self.uncut_valid_moves.append([position[0] + (100 * x), position[1]])
                for x in range(-8, 0):
                    if 200 < position[0] + (100 * x) < 1000:
                        if [position[0] + (100 * x), position[1]] != position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([position[0] + (100 * x), position[1]])

                valid_horizontal()

                possible_positions = []
                self.uncut_valid_moves = []

                # right
                for x in range(9):
                    if 200 < position[0] + (100 * x) < 1000:
                        if [position[0] + (100 * x), position[1]] != position:
                            possible_positions.append([position[0] + (100 * x), position[1]])
                            self.uncut_valid_moves.append([position[0] + (100 * x), position[1]])
                for x in range(9):
                    if 200 < position[0] + (100 * x) < 1000:
                        if [position[0] + (100 * x), position[1]] != position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([position[0] + (100 * x), position[1]])

                valid_horizontal()

                possible_positions = []
                self.uncut_valid_moves = []

                # vertical
                # up
                for x in range(-8, 0):
                    if 0 < position[1] + (100 * x) < 800:
                        if [position[0], position[1] + (100 * x)] != position:
                            possible_positions.append([position[0], position[1] + (100 * x)])
                            self.uncut_valid_moves.append([position[0], position[1] + (100 * x)])
                for x in range(-8, 0):
                    if 0 < position[1] + (100 * x) < 800:
                        if [position[0], position[1] + (100 * x)] != position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([position[0], position[1] + (100 * x)])

                valid_vertical()

                possible_positions = []
                self.uncut_valid_moves = []

                # down
                for x in range(8):
                    if 0 < position[1] + (100 * x) < 800:
                        if [position[0], position[1] + (100 * x)] != position:
                            possible_positions.append([position[0], position[1] + (100 * x)])
                            self.uncut_valid_moves.append([position[0], position[1] + (100 * x)])
                for x in range(8):
                    if 0 < position[1] + (100 * x) < 800:
                        if [position[0], position[1] + (100 * x)] != position:
                            if all(z != n for n in possible_positions for z in pieces_pos):
                                self.uncut_valid_moves.append([position[0], position[1] + (100 * x)])

                valid_vertical()

                possible_positions = []
                self.uncut_valid_moves = []

            # knight movement rules
            if len(self.ID) == 3:
                for x in [-2, 2]:
                    for y in [-1, 1]:
                        if 200 <= position[0] + (x * 100) <= 1000:
                            self.valid_moves.append([position[0] + (x * 100), position[1] + (y * 100)])
                        if 200 <= position[0] + (y * 100) <= 1000:
                            self.valid_moves.append([position[0] + (y * 100), position[1] + (x * 100)])

            else:
                # king movement rules
                if self.ID[1] == 'K':
                    for c in range(-1, 2):
                        for d in range(-1, 2):
                            if 0 <= position[1] + (d * 100) <= 800:
                                if 200 <= position[0] + (c * 100) <= 1000:
                                    if [position[0] + (c * 100), position[1] + (d * 100)] != position:
                                        self.valid_moves.append(
                                            [position[0] + (c * 100), position[1] + (d * 100)])

                                        # castling
                                        # if self.move_count == 0:
                                        #     self.valid_moves.append([position[0] + 200, position[1]])
                                        #     self.valid_moves.append([position[0] - 200, position[1]])

                # bishop movement rules
                if self.ID[1] == 'B':
                    bishop_valid()

                # rook movement rules
                if self.ID[1] == 'R':
                    rook_valid()

                # queen movement rules
                if self.ID[1] == 'Q':
                    bishop_valid()
                    rook_valid()

                # pawn movement rules
                if self.ID[1] == 'P':

                    if self.ID[0] == 'W':
                        for piece in pieces_list:
                            if self.ID[0] != piece.ID[0]:
                                if [position[0] + 100, position[1] - 100] == piece.position:
                                    self.valid_moves.append(piece.position)
                                elif [position[0] - 100, position[1] - 100] == piece.position:
                                    self.valid_moves.append(piece.position)

                        if all([position[0], position[1] - 100] != piece.position for piece in pieces_list):
                            self.valid_moves.append([position[0], position[1] - 100])
                            if all([position[0], position[1] - 200] != piece.position for piece in pieces_list):
                                if self.move_count == 0:
                                    self.valid_moves.append([position[0], position[1] - 200])

                    elif self.ID[0] == 'B':
                        for piece in pieces_list:
                            if self.ID[0] != piece.ID[0]:
                                if [position[0] + 100, position[1] + 100] == piece.position:
                                    self.valid_moves.append(piece.position)
                                if [position[0] - 100, position[1] + 100] == piece.position:
                                    self.valid_moves.append(piece.position)

                        if all([position[0], position[1] + 100] != piece.position for piece in pieces_list):
                            self.valid_moves.append([position[0], position[1] + 100])
                            if all([position[0], position[1] + 200] != piece.position for piece in pieces_list):
                                if self.move_count == 0:
                                    self.valid_moves.append([position[0], position[1] + 200])

        rem = []

        # removing duplicates
        self.valid_moves = list(set(tuple(k) for k in self.valid_moves))
        self.valid_moves = list(list(k) for k in self.valid_moves)



        # removing moves out of range
        for move in self.valid_moves:
            if move[0] < 250 or move[0] > 1050 or move[1] < 50 or move[1] > 850:
                if move != [10000, 10000]:
                    rem.append(move)

        if pieces_list:
            # removing moves occupied by other pieces
            for move in self.valid_moves:
                for piece in pieces_list:
                    if move == piece.position and piece.ID[0] == self.ID[0]:
                        rem.append(move)
        elif pieces:
            for move in self.valid_moves:
                for colors in pieces:
                    for piece in colors[1:]:
                        if move == piece.position and piece.ID[0] == self.ID[0]:
                            rem.append(move)

        if board:
            for move in self.valid_moves:
                for x in board.board:
                    for y in x:
                        if y != 0 and y[0] == move:
                            if y[1][0] == self.ID[0]:
                                rem.append(move)



        # remove items in rem
        for x in rem:
            if x in self.valid_moves:
                self.valid_moves.remove(x)

        rem = []

        # fail safe if no valid moves
        if not self.valid_moves:
            self.valid_moves.append([10000, 10000])

        # print(self.key)
        # for x, y in self.valid_moves:
        #     print(x - self.position[0], y - self.position[1])

        return self.valid_moves


