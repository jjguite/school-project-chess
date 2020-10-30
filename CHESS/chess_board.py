import time
import random

from CHESS.chess_data import MOVE_COUNT
from CHESS import Piece

# chess board class
class ChessBoard:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(0)

        return self.board

    def update_board(self, pieces):
        self.board = []
        self.create_board()

        for piece in pieces:
            if isinstance(piece, Piece.Piece):
                row = (piece.position[1] - 60) // 100
                col = (piece.position[0] - 260) // 100
                self.board[row][col] = [piece.position, piece.key, piece.value]
            else:
                row = (piece[0][1] - 60) // 100
                col = (piece[0][0] - 260) // 100
                self.board[row][col] = piece

        return self.board

    def get_piece(self, key):
        for x in self.board:
            for y in x:
                if y != 0:
                    if y[1] == key:
                        return y

    def evaluate(self, ID):
        adj = 1 + (MOVE_COUNT / 20)
        value = 0

        for x in self.board:
            for y in x:
                if y != 0:
                    if y[1][0] == ID:
                        value += y[2]
                    else:
                        value -= y[2]

                    if y[2] == 10000:
                        if self.board.index(x) == 7:
                            value += 5

                        elif self.board.index(x) == 6:
                            value += 2

                        elif self.board.index(x) == 5:
                            value -= 1

                        elif self.board.index(x) == 4:
                            value -= 3

                    elif y[2] == 3:
                        if self.board.index(x) == 6:
                            value += 0

                        elif self.board.index(x) == 5:
                            value += (adj * 3)

                        elif self.board.index(x) == 4:
                            value += (3 * (adj * 3))

                    else:
                        if self.board.index(x) == 7:
                            value -= (random.uniform(3, 6) * adj)

                        elif self.board.index(x) == 6:
                            value -= (2 * adj)

                        elif self.board.index(x) == 5:
                            value += (1 * adj)

                        elif self.board.index(x) == 4:
                            value += (2 * adj)

                        elif self.board.index(x) == 3:
                            value += (3 * adj)

                        elif self.board.index(x) == 2:
                            value += (2 * adj)



                    if x.index(y) == 0 or x.index(y) == 7:
                        value -= 3


        return value

    def move(self, piece, x, y, board):
        # print('start board.move')
        pieces = self.get_pieces_list(board)

        w = (x - 260) // 100
        z = (y - 60) // 100

        # print('piece:', piece)

        piece[0] = [x, y]
        self.board[z][w] = piece

        self.update_board(pieces)

        # print()
        # print('new board')
        # for x in self.board:
        #     print(x)

        # time.sleep(10)

        # print('end board.move')

    # gets all pieces in list form FROM SELF.BOARD
    def get_pieces_list(self, board):
        pieces = []

        for x in board.board:
            for y in x:
                if y != 0:
                    pieces.append(y)

        return pieces

