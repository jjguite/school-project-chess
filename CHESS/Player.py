import pygame
import pygame.gfxdraw
import random
import time
from CHESS import chess_data as cd
from CHESS import Piece
from CHESS import chess_board as cb
from copy import deepcopy

# import tensorflow as tf
# import keras as ks
import numpy as np

pygame.font.init()

info_font = pygame.font.SysFont('Times', 20)

info = None
info_lis = []
display_move = None
all_display_moves = []

all_game_states = None


""" 2 player game set up below """
# # # game_mode = 0
# # # white_player = False
# # # black_player = False
# # #
# # # let player decide which color to be
# # # if game_mode == 1:
# # #     P1_player_type = input('Which player do you want to be? (W or B): ').upper()
# # #     while P1_player_type != 'W' and P1_player_type != 'B':
# # #         ('invalid response, try again')
# # #         P1_player_type = input('Which player do you want to be? (W or B): ').upper()
# # # else:
# # #     P1_player_type = 'W'
# # #
# # # if P1_player_type == 'W':
# # #     P1_player_type = 'White'
# # #     white_player = True
# # # elif P1_player_type == 'B':
# # #     P1_player_type = 'Black'
# # #     black_player = True
# # #
# # # let player select game mode
# # # game_mode = int(input('Select game mode (0, 1, 2): '))
# # # while game_mode != 0 and game_mode != 1 and game_mode != 2:
# # #     print('invalid response, try again')
# # #     game_mode = input('Select game mode (0, 1, 2): ')
# # #
# # # if game_mode == 1:
# # #     print(game_mode, 'human player')
# # # else:
# # #     print(game_mode, 'human players')

All_ID = ['WK', 'WQ', 'WR', 'WB', 'WKN', 'WP', 'BK', 'BQ', 'BR', 'BB', 'BKN', 'BP']



class Player:
    def __init__(self, player_type, color, pieceID, turn, pieces):
        self.player_type = player_type
        self.color = color
        self.pieceID = pieceID
        self.turn = turn
        self.castled = False
        self.in_check = False
        self.mate = False


        for x in pieces:
            if x[0] == self.pieceID:
                self.pieces = x[1:]
            else:
                self.not_pieces = x[1:]

    def switch_turns(self):
        if self.turn:
            self.turn = False
            return
        if not self.turn:
            self.turn = True
            # print(f'{self.color}\'s turn')

    def check_for_win(self):
        if self.pieces[4].is_taken:
            self.mate = True

        if self.mate:
            cd.game_over = True
            if self.color == 'white':
                print('game over, black won,', self.color, 'lost')
            elif self.color == 'black':
                print('game over, white won,', self.color, 'lost')

    def update(self, display):
        pass
        # drawing valid moves FOR CURRENT TURN ONLY
        # if self.turn:
        #     for y in self.pieces:
        #         for x in y.valid_moves:
        #             if 250 < x[0] < 1050 and 50 < x[1] < 850:
        #                 pygame.draw.rect(display, (255, 234, 0), (x[0] - 10, x[1] - 10, 100, 100), 3)
                        # pygame.gfxdraw() ???

        # # pawn promotion
        # for x in self.pieces[8:]:
        #     if self.pieceID == 'W':
        #         if x.position[1] == 60:
        #             x.ID = f'{self.pieceID}Q'
        #             x.sprite = self.pieces[3].sprite
        #     elif self.pieceID == 'B':
        #         if x.position[1] == 760:
        #             x.ID = f'{self.pieceID}Q'
        #             x.sprite = self.pieces[3].sprite

    def move(self, pieces, white, black, max_player, pieces_list, ev=None, board=None):
        if not cd.game_over:
            if self.turn:
                if self.player_type == 'minimax':
                    value, new_board = self.minimax(pieces, board, cd.DEPTH, max_player, board, self.pieceID[0], pieces_list)
                    print('VALUE:', value)
                    print('BOARD:')
                    for x in new_board.board:
                        print(x)

                    self.minimax_move(board, new_board, white, black, pieces_list)


                elif self.player_type == 'random':
                    # self.check_for_check(pieces, board, 'W', pieces_list)
                    self.random_move(pieces, white, black, board, pieces_list)


                elif self.player_type == 'human':
                    for x in self.pieces:
                        x.human_piece_movement(ev)


            if not self.castled:
                if self.pieces[4].init_position:
                    if self.pieces[0].move_count == 0:
                        if 150 < self.pieces[4].init_position[0] - self.pieces[4].position[0] < 250:
                            self.pieces[0].position[0] += 300
                            self.castled = True

                    if self.pieces[7].move_count == 0:
                        if -250 < self.pieces[4].init_position[0] - self.pieces[4] < -150:
                            self.pieces[7].position[0] -= 200
                            self.castled = True


    def random_move(self, pieces, white, black, board, pieces_list):
        global info, display_move, all_display_moves

        valid_keys = []

        # get list of all valid moves
        for piece in self.pieces:
            if not piece.is_taken:
                piece.find_valid_moves(pieces=pieces)
                for move in piece.valid_moves:
                    if move != [10000, 10000]:
                        valid_keys.append([move[0], move[1], piece.key])

        # if self.in_check is True:
        #     print('IN CHECK')
        #     time.sleep(10)
        #
        # # if self.in_check is True:
        #
        # bruh = [self.check_for_check(pieces, board, 'W', pieces_list)]
        # print('BRUH:')
        # print(bruh)
        # for x in bruh:
        #     if isinstance(x, cb.ChessBoard):
        #         for y in x.board:
        #             print(y)
        #         valid_keys = []
        #
        # for x in bruh:
        #     if isinstance(x, cb.ChessBoard):
        #         valid_keys.append(x)


        action = random.choice(valid_keys)

        # if isinstance(action, cb.ChessBoard):
        #     for w in self.pieces:
        #         for x in action.board:
        #             for y in x:
        #                 if y[1] == w.key:
        #                     action = y



        # if isinstance(bruh[0], cb.ChessBoard):
        #     valid_keys = []
        #
        #     for q in bruh:
        #         for x in range(len(board.board)):
        #             for y in range(len(board.board[x])):
        #                 if y != q.board[x][y]:
        #                     if q.board[x][y] != 0:
        #                         print('MOVED PIECE:')
        #                         print(q.board[x][y])
        #                         valid_keys.append(q.board[x][y])


        # choose a random move


        print('ACTION:', action)

        # if not isinstance(bruh[0], cb.ChessBoard):
        #     print('NOT BRUH')
        print(f'{action[2]}, action: {action[0:2]}')

        time.sleep(2)
        # update individual piece move count and position
        for x in self.pieces:
            if x.key == action[2]:
                x.move_count += 1
                x.position[0] = action[0]
                x.position[1] = action[1]
        # else:
        #     print('BRUH')
        #     print(f'{action[1]}, action: {action[0]}')
        #     for x in self.pieces:
        #         if x.key == action[1]:
        #             x.move_count += 1
        #             x.position[0] = action[0][0]
        #             x.position[1] = action[0][1]


        # reset valid moves and make sure taken pieces are off the board
        for piece in self.pieces:
            piece.valid_moves = []
        for piece in self.not_pieces:
            piece.valid_moves = []
            if piece.position == action[0:2]:
                piece.is_taken = True

        # check for check
        # none

        white.switch_turns()
        black.switch_turns()

        cd.MOVE_COUNT += 1

        bruh = []

        # time between turns
        # if Piece.MOVE_COUNT > 1:
        #     time.sleep(3)
        # if Piece.MOVE_COUNT > 8:
        #     time.sleep(600)
        # time.sleep(0.1)

    def simulate_move(self, piece, move, board):
        board.move(piece, move[0], move[1], board)

        return board


    def get_all_valid(self, pieces, board, color, pieces_list):
        # print('start get_all_valid')
        # moves will store board, piece pair?
        moves = []

        for x in pieces_list:
            if x.is_taken:
                pieces_list.remove(x)

        for piece in self.get_all_pieces(board, color, pieces_list):
            # if not piece:
            #     for x in self.get_all_pieces(board, color, pieces_list):
            #         print(x)
            #     print('PIECE:', piece)
            #     print('BOARD:')
            #     for x in board.board:
            #         print(x)
                # time.sleep(1000)
            if not piece.is_taken:

                valid_moves = piece.find_valid_moves(board=board, pieces_list=pieces_list)
                # print('PIECE:', piece.key, valid_moves)
                for x in valid_moves:
                    if x == [10000, 10000]:
                        valid_moves.remove(x)

                # print('VALID MOVES:', piece.key, valid_moves)

                for move in valid_moves:
                    if move != [10000, 10000]:
                        temp_board = deepcopy(board)
                        temp_piece = temp_board.get_piece(piece.key)

                        # simulate_move makes a move and returns a board
                        new_board = self.simulate_move(temp_piece, move, temp_board)
                        moves.append(new_board)
            piece.valid_moves = []


        # print('end get_all_valid')
        # print()

        return moves

    def minimax(self, pieces, position, depth, max_player, board, color, pieces_list):
        if depth == 0 or cd.game_over:
            if max_player:
                return position.evaluate('B'), position
            else:
                return position.evaluate('W'), position


        if max_player:
            maxEval = float('-inf')
            best_move = None

            for move in self.get_all_valid(pieces, board, 'W', pieces_list):
                # print('WHITE evaluating move:')
                # for x in move.board:
                #     print(x)
                # print()
                # # time.sleep(10)
                evaluation = self.minimax(pieces, move, depth - 1, False, move, color, pieces_list)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move

            return maxEval, best_move

        else:
            minEval = float('inf')
            best_move = None

            for move in self.get_all_valid(pieces, board, 'B', pieces_list):
                # print('BLACK evaluating move:')
                # for x in move.board:
                #     print(x)
                # print()
                # # time.sleep(10)
                evaluation = self.minimax(pieces, move, depth - 1, True, move, color, pieces_list)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move

            return minEval, best_move

    def minimax_move(self, board, new_board, white, black, pieces_list):
        for x in pieces_list:
            if x.is_taken:
                pieces_list.remove(x)

        board.update_board(pieces_list)
        board.board = new_board.board

        for x in board.board:
            for y in x:
                if y != 0:
                    for z in pieces_list:
                        temp_pos = z.position.copy()
                        if y[1] == z.key:
                            z.position = y[0]
                            z.valid_moves = []

                            # if the position changed, increase move count
                            if z.position != temp_pos:
                                z.move_count += 1
                                print(f'{z.key}, action: {z.position} ')

                            if z in self.pieces:

                                for x in self.not_pieces:
                                    if x.position == z.position:
                                        x.is_taken = True

        white.switch_turns()
        black.switch_turns()

        cd.MOVE_COUNT += 1

    # gets all pieces for specific player
    def get_all_pieces(self, board, color, pieces_list):
        # print('start get_all_pieces')

        # for x in board.board:
        #     print(x)
        # for x in pieces_list:
        #     print(x.key, x.position)

        pieces = []
        not_pieces = []

        # gets pieces in list form from the TEMP UPDATED BOARD
        for row in board.board:
            for piece in row:
                if piece != 0:
                    if piece[1][0] == self.pieceID:
                        pieces.append(piece)
                    elif piece[1][0] != self.pieceID:
                        not_pieces.append(piece)

        # print('ERROR INFO:')
        # print(pieces)
        # print(not_pieces)
        # converts lists into Piece objects

        pieces = [self.get_piece(board, x[0][0], x[0][1], pieces, pieces_list) for x in pieces]
        not_pieces = [self.get_piece(board, x[0][0], x[0][1], not_pieces, pieces_list) for x in not_pieces]
        # for x in pieces:
        #     if x:
        #         print(x.key, x.position)
        # for x in not_pieces:
        #     if x:
        #         print(x.key, x.position)

        if color == self.pieceID:
            # print('end get_all_pieces')
            # print()
            return pieces
        else:
            # print('end get_all_pieces')
            # print()
            return not_pieces

    # gets an actual Piece object
    def get_piece(self, board, row, col, pieces, pieces_list):
        row = (row - 260) // 100
        col = (col - 60) // 100

        pos = board.board[col][row]

        for x in pieces:
            if pos != 0:
                if x[0] == pos[0]:
                    for y in pieces_list:
                        if pos[1] == y.key:
                            return y

    def check_for_check(self, pieces, board, color, pieces_list):
        check_move = None
        valid_moves = []
        list1 = []
        extra_list = []

        for y in self.get_all_valid(pieces, board, color, pieces_list):
            if y.evaluate(self.pieceID[0]) < -9000:
                self.in_check = True
                for x in y.board:
                    print(x)
                print(self.pieces[4].key, self.pieces[4].position)
                print('PIECES:', pieces)
                print('PIECES_LIST:', pieces_list)
                print('KEY:', self.get_piece(y, self.pieces[4].position[0], self.pieces[4].position[1], pieces, pieces_list))
                check_move = y
                print('IN CHECK')
                # time.sleep(1000)
                # return self.get_piece(board, self.pieces[4].position[0], self.pieces[4].position[1], pieces, pieces_list)

        if check_move:
            # for each move black can make WHILE IN CHECK:
            for z in self.get_all_valid(pieces, board, 'B', pieces_list):
                list1 = self.get_all_valid(pieces, z, 'W', pieces_list)

                for x in list1:
                    for y in x.board:
                        for q in y:
                            if q[1] == 'BK':
                                extra_list.append(y)

                    if extra_list:
                        if z not in valid_moves:
                            valid_moves.append(z)
                        extra_list = []




                # if any(all(y[1] != 'BK' for x in k.board for y in x if y != 0) for k in self.get_all_valid(pieces, z, 'W', pieces_list)):
                #     pass
                # else:
                #     valid_moves.append(z)

            print('VALID MOVES:')
            for x in valid_moves:
                for y in x.board:
                    print(y)
                print()
            print('LEN:', len(valid_moves))
            time.sleep(10)
            return valid_moves



def reset():
    # piece objects
    WR1 = Piece.Piece('WR', [260, 760], 'WR1', 8)
    WKN1 = Piece.Piece('WKN', [360, 760], 'WN1', 6)
    WB1 = Piece.Piece('WB', [460, 760], 'WDB', 6)
    WQ = Piece.Piece('WQ', [560, 760], 'WQ', 18)
    WK = Piece.Piece('WK', [660, 760], 'WK', 10000)
    WB2 = Piece.Piece('WB', [760, 760], 'WLB', 6)
    WKN2 = Piece.Piece('WKN', [860, 760], 'WN2', 6)
    WR2 = Piece.Piece('WR', [960, 760], 'WR2', 8)

    WP1 = Piece.Piece('WP', [260, 660], 'WP1', 3)
    WP2 = Piece.Piece('WP', [360, 660], 'WP2', 3)
    WP3 = Piece.Piece('WP', [460, 660], 'WP3', 3)
    WP4 = Piece.Piece('WP', [560, 660], 'WP4', 3)
    WP5 = Piece.Piece('WP', [660, 660], 'WP5', 3)
    WP6 = Piece.Piece('WP', [760, 660], 'WP6', 3)
    WP7 = Piece.Piece('WP', [860, 660], 'WP7', 3)
    WP8 = Piece.Piece('WP', [960, 660], 'WP8', 3)

    BR1 = Piece.Piece('BR', [260, 60], 'BR1', 8)
    BKN1 = Piece.Piece('BKN', [360, 60], 'BN1', 6)
    BB1 = Piece.Piece('BB', [460, 60], 'BLB', 6)
    BQ = Piece.Piece('BQ', [560, 60], 'BQ', 18)
    BK = Piece.Piece('BK', [660, 60], 'BK', 10000)
    BB2 = Piece.Piece('BB', [760, 60], 'BDB', 6)
    BKN2 = Piece.Piece('BKN', [860, 60], 'BN2', 6)
    BR2 = Piece.Piece('BR', [960, 60], 'BR2', 8)

    BP1 = Piece.Piece('BP', [260, 160], 'BP1', 3)
    BP2 = Piece.Piece('BP', [360, 160], 'BP2', 3)
    BP3 = Piece.Piece('BP', [460, 160], 'BP3', 3)
    BP4 = Piece.Piece('BP', [560, 160], 'BP4', 3)
    BP5 = Piece.Piece('BP', [660, 160], 'BP5', 3)
    BP6 = Piece.Piece('BP', [760, 160], 'BP6', 3)
    BP7 = Piece.Piece('BP', [860, 160], 'BP7', 3)
    BP8 = Piece.Piece('BP', [960, 160], 'BP8', 3)

    pieces = [['W', WR1, WKN1, WB1, WQ, WK, WB2, WKN2, WR2, WP1, WP2, WP3, WP4, WP5, WP6, WP7, WP8],
              ['B', BR1, BKN1, BB1, BQ, BK, BB2, BKN2, BR2, BP1, BP2, BP3, BP4, BP5, BP6, BP7, BP8]]


    # assigning sprites to pieces
    for x in pieces:
        for y in x[1:]:
            for z in cd.sprites:
                if y.ID == z[0]:
                    y.sprite = z[1]

    # extra variable for valid moves func
    for a in pieces:
        for b in a[1:17]:
            Piece.pieces_pos.append(b.position)

    return pieces

# old stuff
# old stuff
# self.collect_data(pieces)
# piece = random.choice(self.pieces)
#
# piece.find_valid_moves(pieces)
#
# choice = random.choice(piece.valid_moves)
#
# while choice == [10000, 10000]:
#     piece.valid_moves = []
#     piece = random.choice(self.pieces)
#     piece.find_valid_moves(pieces)
#     choice = random.choice(piece.valid_moves)
#
# init_pos = piece.position
# piece.position = choice
#
# # PlayerWhite.check = False
# # PlayerBlack.check = False
#
# if piece.position != [10000, 10000]:
#     display_move = f'{Piece.MOVE_COUNT + 1}: {piece.ID} {cd.board_labels_dict[str(init_pos)]}' \
#                    f'{cd.board_labels_dict[str(piece.position)]} '
#
#     if Piece.MOVE_COUNT == 0:
#         all_display_moves.append('\n')
#     all_display_moves.append(display_move)
#
#
#     print(display_move)
#     print()
#
#
#     # info = info_font.render(f'{Piece.MOVE_COUNT + 1}: {piece.ID} {cd.board_labels_dict[str(init_pos)]}'
#     #                         f'{cd.board_labels_dict[str(piece.position)]}', 1, (230, 230, 230))
#     #
#     # info_lis.append([info, Piece.MOVE_COUNT + 1])

# def collect_data(self, pieces):
    #     global all_game_states
    #
    #     # finds current game state
    #     cd.game_state_update(pieces)
    #
    #     # takes out current game state
    #     current_game_state = cd.game_state.copy()
    #
    #     # create bitboards
    #     all_game_states = np.zeros((12, 8, 8))
    #
    #     for x in range(len(All_ID)):
    #         for y in range(len(current_game_state)):
    #             for z in range(len(current_game_state[y])):
    #                 if current_game_state[y][z] == All_ID[x]:
    #                     all_game_states[x][y][z] = 1
    #
    #     print(all_game_states)
    #
    #     self.find_all_moves(pieces)
    #
    # def find_all_moves(self, pieces):
    #     valid = []
    #     for x in self.pieces:
    #         valid.append([x.ID, x.position])
    #
    #     for x in range(len(self.pieces)):
    #
    #         self.pieces[x].find_valid_moves(pieces)
    #         for y in self.pieces[x].valid_moves:
    #             if [10000, 10000] not in self.pieces[x].valid_moves:
    #                 valid[x].append(y)
    #             else:
    #                 valid[x].append(None)
    #
    #     for x in valid:
    #         if None in x:
    #             x.remove(x[1])
    #
    #     # print()
    #     # for x in valid:
    #     #     print(x)
    #     # print()
    #
    #
    #
    #     # for x in valid:
    #     #     if None not in x:
    #     #         for y in x[2:]:
    #     #             if y == self.not_pieces[4].position:
    #
    #
    #
    #     for x in self.pieces:
    #         x.valid_moves = []
    #
    #     valid = []
