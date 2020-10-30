from pieces import pawn
from pieces import king
from pieces import queen
from pieces import bishop
from pieces import rook
from pieces import knight
import colors

import pygame
display = pygame.display.set_mode((1000, 800))
def mouseOver(rect):
    m = pygame.mouse.get_pos()
    if rect[0] < m[0] < rect[0] + rect[2]:
        if rect[1] < m[1] < rect[1] + rect[3]:
            return True
    return False

class ChessSet:

    def __init__(self):

        self.colors = [colors.PLAYER_1, colors.PLAYER_2]

        self.pieces = [
            # PLAYER_1 pieces

            pawn.Pawn([0, 6], self.colors[1]),
            pawn.Pawn([1, 6], self.colors[1]),
            pawn.Pawn([2, 6], self.colors[1]),
            pawn.Pawn([3, 6], self.colors[1]),
            pawn.Pawn([4, 6], self.colors[1]),
            pawn.Pawn([5, 6], self.colors[1]),
            pawn.Pawn([6, 6], self.colors[1]),
            pawn.Pawn([7, 6], self.colors[1]),

            rook.Rook([0, 7], self.colors[1]),
            rook.Rook([7, 7], self.colors[1]),

            knight.Knight([1, 7], self.colors[1]),
            knight.Knight([6, 7], self.colors[1]),

            bishop.Bishop([2, 7], self.colors[1]),
            bishop.Bishop([5, 7], self.colors[1]),

            queen.Queen([3, 7], self.colors[1]),
            king.King([4, 7], self.colors[1]),

            # PLAYER_2 pieces

            pawn.Pawn([0, 1], self.colors[0]),
            pawn.Pawn([1, 1], self.colors[0]),
            pawn.Pawn([2, 1], self.colors[0]),
            pawn.Pawn([3, 1], self.colors[0]),
            pawn.Pawn([4, 1], self.colors[0]),
            pawn.Pawn([5, 1], self.colors[0]),
            pawn.Pawn([6, 1], self.colors[0]),
            pawn.Pawn([7, 1], self.colors[0]),

            rook.Rook([0, 0], self.colors[0]),
            rook.Rook([7, 0], self.colors[0]),

            knight.Knight([1, 0], self.colors[0]),
            knight.Knight([6, 0], self.colors[0]),

            bishop.Bishop([2, 0], self.colors[0]),
            bishop.Bishop([5, 0], self.colors[0]),

            queen.Queen([3, 0], self.colors[0]),
            king.King([4, 0], self.colors[0]),
        ]

class Board:

    class Space:

        def __init__(self, color):
            self.color = color
            self.contents = None

    def __init__(self, gridSize):

        self.gridSize = gridSize
        self.chessSet = ChessSet()
        self.image = pygame.image.load('pieces/img/board.png')
        self.SELECT_FLAG = False

    def getMouse(self):

        m = pygame.mouse.get_pos()

        x = int((m[0] - 244) / self.gridSize)
        y = int((m[1] - 144) / self.gridSize)

        return [x, y]

    def promote(self, piece):

        rookImg = pygame.image.load('pieces/img/White R.png')
        knightImg = pygame.image.load('pieces/img/White N.png')
        bishopImg = pygame.image.load('pieces/img/White B.png')
        queenImg = pygame.image.load('pieces/img/White Q.png')

        if piece.color == colors.PLAYER_2:
            rookImg = pygame.image.load('pieces/img/Black R.png')
            knightImg = pygame.image.load('pieces/img/Black N.png')
            bishopImg = pygame.image.load('pieces/img/Black B.png')
            queenImg = pygame.image.load('pieces/img/Black Q.png')

        promoting = True

        while promoting:

            for event in pygame.event.get():

                # Exit when exit button is pushed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    if mouseOver([318, 384, 64, 64]):
                        piece.ID = 'R'
                        piece.image = rookImg
                        piece.promote = False
                        promoting = False
                    elif mouseOver([414, 384, 64, 64]):
                        piece.ID = 'N'
                        piece.image = knightImg
                        piece.promote = False
                        promoting = False
                    elif mouseOver([510, 384, 64, 64]):
                        piece.ID = 'B'
                        piece.image = bishopImg
                        piece.promote = False
                        promoting = False
                    elif mouseOver([604, 384, 64, 64]):
                        piece.ID = 'Q'
                        piece.image = queenImg
                        piece.promote = False
                        promoting = False
                    else:
                        pass

            # Grey background of popup
            pygame.draw.rect(self.image, (100, 100, 100), [48, 192, 416, 128], 0)

            # Black border around popup
            pygame.draw.rect(self.image, (0, 0, 0), [48, 192, 416, 128], 15)

            # Red background behind pieces
            pygame.draw.rect(self.image, (128, 0, 0), [74, 240, 64, 64], 0)
            pygame.draw.rect(self.image, (128, 0, 0), [170, 240, 64, 64], 0)
            pygame.draw.rect(self.image, (128, 0, 0), [266, 240, 64, 64], 0)
            pygame.draw.rect(self.image, (128, 0, 0), [360, 240, 64, 64], 0)

            # Piece images
            pygame.Surface.blit(self.image, rookImg, (74, 240))
            pygame.Surface.blit(self.image, knightImg, (170, 240))
            pygame.Surface.blit(self.image, bishopImg, (266, 240))
            pygame.Surface.blit(self.image, queenImg, (360, 240))

            # White squares around pieces
            pygame.draw.rect(self.image, (255, 255, 255), [74, 240, 64, 64], 1)
            pygame.draw.rect(self.image, (255, 255, 255), [170, 240, 64, 64], 1)
            pygame.draw.rect(self.image, (255, 255, 255), [266, 240, 64, 64], 1)
            pygame.draw.rect(self.image, (255, 255, 255), [360, 240, 64, 64], 1)

            # Text
            pygame.font.init()
            font = pygame.font.SysFont('arial', 16, True, False)
            label = font.render('Promote Pawn', True, (255, 255, 255))
            rect = label.get_rect()
            x = 256 - rect[2] / 2
            y = 216 - rect[3] / 2
            pygame.Surface.blit(self.image, label, [x, y])

            pygame.Surface.blit(display, self.image, (244, 144))
            pygame.display.update()

        return piece

    def update(self):

        for event in pygame.event.get():

            # Exit when exit button is pushed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # If the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # If there is already a piece selected
                if self.SELECT_FLAG:

                    # Find the active piece
                    for piece in self.chessSet.pieces:
                        if piece.active:

                            # If the mouse is over the active piece
                            if piece.location == self.getMouse():

                                # Deselect the piece
                                self.SELECT_FLAG = False
                                piece.active = False

                            else:

                                # Else if the mouse is over any of the piece's selected squares
                                for space in piece.moveSquares:
                                    if space == self.getMouse():

                                        # Move the piece to the space
                                        piece.move(space, self.chessSet.pieces)
                                        self.SELECT_FLAG = False

                                        # Keep the space on the board
                                        if piece.location[0] < 0: piece.location[0] = 0
                                        if piece.location[1] < 0: piece.location[1] = 0
                                        if piece.location[0] > 7: piece.location[0] = 7
                                        if piece.location[1] > 7: piece.location[1] = 7

                                        # If there is an enemy in the
                                        # new space, capture it.
                                        for otherPiece in self.chessSet.pieces:
                                            if space == otherPiece.location:
                                                if otherPiece.color != piece.color:
                                                    otherPiece.captured = True

                # If there is no piece selected yet
                elif not self.SELECT_FLAG:

                    # Go through all the pieces
                    for piece in self.chessSet.pieces:

                        # If the mouse is over an active piece
                        if piece.location == self.getMouse() and not piece.captured:

                            # Select and move the piece
                            self.SELECT_FLAG = True
                            piece.findSpaces(self.chessSet.pieces)

        # Check if any pawns are on the opposite side of the board
        for n in range(len(self.chessSet.pieces)):
            piece = self.chessSet.pieces[n]
            if piece.ID == 'P':
                if piece.color == colors.PLAYER_1 and piece.location[1] == 7:
                    self.chessSet.pieces[n] = self.promote(piece)
                if piece.color == colors.PLAYER_2 and piece.location[1] == 0:
                    self.chessSet.pieces[n] = self.promote(piece)

        # Promote any pawns if needed
        for n in range(len(self.chessSet.pieces)):

            piece = self.chessSet.pieces[n]

            if piece.ID == 'P':
                if piece.promote:
                    self.chessSet.pieces[n] = self.promote(piece)

    def draw(self):

        #squareWidth = 4
        squareWidth = 0

        # Reset the board image
        self.image = pygame.image.load('pieces/img/board.png')
        # -------------------------
        # Draw red squares around all the spaces onto the board image
        for piece in self.chessSet.pieces:
            if piece.active:

                for square in piece.moveSquares:
                    # Create a rectangle from the coordinates
                    rect = [square[0] * self.gridSize,
                            square[1] * self.gridSize,
                            self.gridSize,
                            self.gridSize]

                    # Draw the square
                    pygame.draw.rect(self.image, (128, 0, 0), rect, squareWidth)
        # -------------------------
        # Draw a blue square around the selected piece
        # Create a rectangle from the coordinates
        for piece in self.chessSet.pieces:
            if piece.active:
                rect = [piece.location[0] * self.gridSize,
                        piece.location[1] * self.gridSize,
                        self.gridSize,
                        self.gridSize]

                # Draw the square
                pygame.draw.rect(self.image, (0, 128, 0), rect, squareWidth)

        # -------------------------
        # Draw the pieces
        for piece in self.chessSet.pieces:

            # If the piece hasn't been captured
            if not piece.captured:
                # Find it's location and draw it's image
                loc = [piece.location[0] * self.gridSize, piece.location[1] * self.gridSize]
                pygame.Surface.blit(self.image, piece.image, loc)
