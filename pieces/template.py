import pygame
import colors

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class Template:

    def __init__(self, location, color):
        self.ID = ''
        self.image = pygame.Surface((0, 0))
        self.color = color
        self.location = location
        self.hasMoved = False
        self.active = False
        self.captured = False
        self.moveSquares = []

    def findSpaces(self, piecesAll):

        if self.ID == 'P':
            self.pawnSpaces(piecesAll)
        elif self.ID == 'R':
            self.rookSpaces(piecesAll)
        elif self.ID == 'N':
            self.knightSpaces(piecesAll)
        elif self.ID == 'B':
            self.bishopSpaces(piecesAll)
        elif self.ID == 'Q':
            self.queenSpaces(piecesAll)
        elif self.ID == 'K':
            self.kingSpaces(piecesAll)

    def _move(self):
        pass

    def move(self, location, piecesAll):

        self.hasMoved = True

        self.moveSquares.clear()
        self.location = location

        if self.location[0] < 0: self.location[0] = 0
        elif self.location[0] > 7: self.location[0] = 7
        if self.location[1] < 0: self.location[1] = 0
        elif self.location[1] > 7: self.location[1] = 7

        self.active = False

        self._move()

    def pawnSpaces(self, piecesAll):
        self.active = True
        self.moveSquares.clear()

        # Find all the possible spaces a pawn can move to given
        # any position, and any configuration of other pieces.

        # White is + because it is on the bottom,
        # and the y value has to decrease to go up.
        W = -1

        # Black is - because it is on the top,
        # and the y value has to increase to go down.
        B = 1

        # Color is set to the appropriate B/W value
        # from above according to it's color.
        #
        # Multiply it [B/W] with the number of
        # spaces forward the piece moves.
        COLOR = 0

        # Color is set to the piece's color
        if self.color == colors.PLAYER_1:
            COLOR = W
        elif self.color == colors.PLAYER_2:
            COLOR = B

        # -------------------------
        # Search for spaces

        # Find the space in front of the piece
        ADD = True
        x = [self.location[0], self.location[1] - COLOR]

        # If any other pieces are already in that space
        for piece in piecesAll:
            if piece.location == x and not piece.captured:
                # Don't add the space
                ADD = False

        # Add the space if it is empty
        if ADD:
            self.moveSquares.append(x)

            # -------------------------
        # A pawn can go 2 spaces forward on it's first move
        if not self.hasMoved and self.moveSquares:
            ADD = True
            x = [self.location[0], self.location[1] - COLOR * 2]

            # If any other pieces are already in that space
            for piece in piecesAll:
                if piece.location == x:
                    # Don't add the space
                    ADD = False

            # Add the space if it is empty
            if ADD:
                self.moveSquares.append(x)

        # -------------------------
        # Get the coordinates for the front-left and front-right to
        # check for enemies to attack.
        check_a = [self.location[0] - 1, self.location[1] - COLOR]
        check_b = [self.location[0] + 1, self.location[1] - COLOR]

        for otherPiece in piecesAll:

            # If there is an enemy in either space
            if otherPiece.location == check_a and otherPiece.color != self.color:
                # Add it to the list
                self.moveSquares.append(check_a)
            if otherPiece.location == check_b and otherPiece.color != self.color:
                self.moveSquares.append(check_b)

        # -------------------------
        # Check if there is an enemy pawn to the left or right of the piece
        # If there is, the piece can move to the upper left/right corner

        frontLeft = [self.location[0] - 1, self.location[1] - COLOR]
        frontRight = [self.location[0] + 1, self.location[1] - COLOR]
        left = [self.location[0] - 1, self.location[1]]
        right = [self.location[0] + 1, self.location[1]]

        for piece in piecesAll:

            # If any of the other pieces are enemy pawns, and not captured
            if piece.color != self.color and piece.ID == 'P' and not piece.captured:

                # Add the space behind them to the list
                if piece.location == left:
                    self.moveSquares.append(frontLeft)
                elif piece.location == right:
                    self.moveSquares.append(frontRight)

    def rookSpaces(self, piecesAll):
        self.active = True

        # Find all the possible spaces a king can move to given
        # any position, and any configuration of other pieces.

        # White is + because it is on the bottom,
        # and the y value has to decrease to go up.
        W = 1

        # Black is - because it is on the top,
        # and the y value has to increase to go down.
        B = -1

        # Color is set to the appropriate B/W value
        # from above according to it's color.
        #
        # Multiply it [B/W] with the number of
        # spaces forward the piece moves.
        COLOR = 0

        # Color is set to the piece's color
        if self.color == colors.PLAYER_1:
            COLOR = W
        elif self.color == colors.PLAYER_2:
            COLOR = B

        x = self.location[0]
        y = self.location[1]

        self.moveSquares.clear()

        _list = [
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
        ]

        for n in range(1, 8):

            list = [
                [[x, y - n], _list[0][1]],
                [[x - n, y], _list[1][1]],
                [[x + n, y], _list[2][1]],
                [[x, y + n], _list[3][1]],
            ]

            for r in range(len(list)):

                space = list[r]
                ADD = True

                for piece in piecesAll:

                    if piece.location == space[0] and not piece.captured:
                        _list[r][1] = False

                        if piece.color == self.color:
                            ADD = False

                if ADD and space[1]:
                    self.moveSquares.append(space[0])

    def knightSpaces(self, piecesAll):
        self.active = True
        self.moveSquares.clear()

        # Find all the possible spaces a king can move to given
        # any position, and any configuration of other pieces.

        # White is + because it is on the bottom,
        # and the y value has to decrease to go up.
        W = 1

        # Black is - because it is on the top,
        # and the y value has to increase to go down.
        B = -1

        # Color is set to the appropriate B/W value
        # from above according to it's color.
        #
        # Multiply it [B/W] with the number of
        # spaces forward the piece moves.
        COLOR = 0

        # Color is set to the piece's color
        if self.color == colors.PLAYER_1:
            COLOR = W
        elif self.color == colors.PLAYER_2:
            COLOR = B

        x = self.location[0]
        y = self.location[1]

        list = [
            [x - 1, y - 2],
            [x + 1, y - 2],
            [x + 2, y - 1],
            [x - 2, y - 1],
            [x - 2, y + 1],
            [x + 2, y + 1],
            [x - 1, y + 2],
            [x + 1, y + 2],

        ]

        for space in list:

            ADD = True

            for piece in piecesAll:

                if piece.location == space and piece.color == self.color and not piece.captured:
                    ADD = False
                elif not (0 <= space[0] <= 7) or not (0 <= space[1] <= 7):
                    ADD = False

            if ADD:
                self.moveSquares.append(space)

    def bishopSpaces(self, piecesAll):
        self.active = True

        # Find all the possible spaces a king can move to given
        # any position, and any configuration of other pieces.

        # White is + because it is on the bottom,
        # and the y value has to decrease to go up.
        W = 1

        # Black is - because it is on the top,
        # and the y value has to increase to go down.
        B = -1

        # Color is set to the appropriate B/W value
        # from above according to it's color.
        #
        # Multiply it [B/W] with the number of
        # spaces forward the piece moves.
        COLOR = 0

        # Color is set to the piece's color
        if self.color == colors.PLAYER_1:
            COLOR = W
        elif self.color == colors.PLAYER_2:
            COLOR = B

        x = self.location[0]
        y = self.location[1]

        self.moveSquares.clear()

        _list = [
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
        ]

        for n in range(1, 8):

            list = [
                [[x - n, y - n], _list[0][1]],
                [[x + n, y - n], _list[1][1]],
                [[x - n, y + n], _list[2][1]],
                [[x + n, y + n], _list[3][1]],
            ]

            for r in range(len(list)):

                space = list[r]
                ADD = True

                for piece in piecesAll:

                    if piece.location == space[0] and not piece.captured:
                        _list[r][1] = False

                        if piece.color == self.color:
                            ADD = False

                if ADD and space[1]:
                    self.moveSquares.append(space[0])

    def queenSpaces(self, piecesAll):
        self.active = True

        # Find all the possible spaces a king can move to given
        # any position, and any configuration of other pieces.

        # White is + because it is on the bottom,
        # and the y value has to decrease to go up.
        W = 1

        # Black is - because it is on the top,
        # and the y value has to increase to go down.
        B = -1

        # Color is set to the appropriate B/W value
        # from above according to it's color.
        #
        # Multiply it [B/W] with the number of
        # spaces forward the piece moves.
        COLOR = 0

        # Color is set to the piece's color
        if self.color == colors.PLAYER_1:
            COLOR = W
        elif self.color == colors.PLAYER_2:
            COLOR = B

        x = self.location[0]
        y = self.location[1]

        self.moveSquares.clear()

        _list = [
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
            [[0, 0], True],
        ]

        for n in range(1, 8):

            list = [
                [[x - n, y - n], _list[0][1]],
                [[x, y - n], _list[1][1]],
                [[x + n, y - n], _list[2][1]],
                [[x - n, y], _list[3][1]],
                [[x + n, y], _list[4][1]],
                [[x - n, y + n], _list[5][1]],
                [[x, y + n], _list[6][1]],
                [[x + n, y + n], _list[7][1]],
            ]

            for r in range(len(list)):

                space = list[r]
                ADD = True

                for piece in piecesAll:

                    if piece.location == space[0] and not piece.captured:
                        _list[r][1] = False

                        if piece.color == self.color:
                            ADD = False

                if ADD and space[1]:
                    self.moveSquares.append(space[0])

    def kingSpaces(self, piecesAll):
        self.active = True

        # Find all the possible spaces a king can move to given
        # any position, and any configuration of other pieces.

        # White is + because it is on the bottom,
        # and the y value has to decrease to go up.
        W = 1

        # Black is - because it is on the top,
        # and the y value has to increase to go down.
        B = -1

        # Color is set to the appropriate B/W value
        # from above according to it's color.
        #
        # Multiply it [B/W] with the number of
        # spaces forward the piece
        # moves, or subtract it from Y.
        COLOR = 0

        # Color is set to the piece's color
        if self.color == colors.PLAYER_1:
            COLOR = W
        elif self.color == colors.PLAYER_2:
            COLOR = B

        x = self.location[0]
        y = self.location[1]

        list = [
            [x - 1, y - 1],
            [x - 1, y],
            [x - 1, y + 1],
            [x, y - 1],
            [x, y + 1],
            [x + 1, y - 1],
            [x + 1, y],
            [x + 1, y + 1],
        ]

        for space in list:

            ADD = True

            for piece in piecesAll:

                if piece.location == space and piece.color == self.color and not piece.captured:
                    ADD = False
                elif not (0 <= space[0] <= 7) or not (0 <= space[1] <= 7):
                    ADD = False

            if ADD:
                self.moveSquares.append(space)
