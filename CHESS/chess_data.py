import random
import pygame

### VARIABLES ###

# minimax depth
DEPTH = 3

MOVE_COUNT = 0
SWITCH = False
game_over = False

block_size = 100
sprite_size = 80

# importing sprites
wr = ['WR', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/w_rook_png_1024px.png'), (sprite_size, sprite_size))]
wkn = ['WKN', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                       'chess/w_knight_png_1024px.png'), (sprite_size, sprite_size))]
wb = ['WB', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/w_bishop_png_1024px.png'), (sprite_size, sprite_size))]
wq = ['WQ', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/w_queen_png_1024px.png'), (sprite_size, sprite_size))]
wk = ['WK', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/w_king_png_1024px.png'), (sprite_size, sprite_size))]
wp = ['WP', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/w_pawn_png_1024px.png'), (sprite_size, sprite_size))]

br = ['BR', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/b_rook_png_1024px.png'), (sprite_size, sprite_size))]
bkn = ['BKN', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                       'chess/b_knight_png_1024px.png'), (sprite_size, sprite_size))]
bb = ['BB', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/b_bishop_png_1024px.png'), (sprite_size, sprite_size))]
bq = ['BQ', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/b_queen_png_1024px.png'), (sprite_size, sprite_size))]
bk = ['BK', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/b_king_png_1024px.png'), (sprite_size, sprite_size))]
bp = ['BP', pygame.transform.scale(pygame.image.load('/Users/jonathanguite/PycharmProjects/basics-startup/pygame/'
                                                     'chess/b_pawn_png_1024px.png'), (sprite_size, sprite_size))]

sprites = [wk, wq, wb, wkn, wr, wp, bk, bq, bb, bkn, br, bp]

# 0 = computer vs. computer, 1 = single player
GAME_MODE = 0

# render in pygame or not
render = False

# episode = 1
# EPISODES = 10
# SHOW_EVERY = 100
#
# # size of grid (8x8)
# GRID_SIZE = 8
#
# ACTION_SPACE_SIZE = 230
# OBSERVATION_SPACE_VALUES = (8, 8, 12)
# OBSERVATION_SPACE_SIZE = 32
#
# REPLAY_MEMORY_SIZE = 50_000  # How many last steps to keep for model training
# MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps in a memory to start training
#
# MINIBATCH_SIZE = 64  # How many steps (samples) to use for training
# UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
#
# MODEL_NAME = 'CHESS_IDK'
# MIN_REWARD = -200  # For model save
# MEMORY_FRACTION = 0.20
#
# # reward values (OWN PIECES TAKEN)
# king_penalty = -1000
# queen_penalty = -9
# rook_penalty = -5
# bishop_penalty = -3
# knight_penalty = -3
# pawn_penalty = -1
#
# # reward values (OPPOSITE PIECES TAKEN)
# king_reward = 1000
# queen_reward = 9
# rook_reward = 5
# bishop_reward = 3
# knight_reward = 3
# pawn_reward = 1
#
# # epsilon determines how many moves are explore vs. exploit
# epsilon = 0.9
# # how fast epsilon decays (epsilon 0 = full exploitation)
# EPS_DECAY = 0.95
#
# # how much the future expected reward is discounted
# DISCOUNT = 0.95
# LEARNING_RATE = 0.1
#
# # can use an existing q table file here to start from
# start_q_table = None
#
# episode_rewards = []

# DATA COLLECTION VARIABLES

chess_board = [[], [], [], [], [], [], [], []]
chess_board2 = [[], [], [], [], [], [], [], []]

x = [(x * 100) + 260 for x in range(8)]
y = [(x * 100) + 60 for x in range(8)]

let = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
num = [8, 7, 6, 5, 4, 3, 2, 1]

board_labels_dict = {}

for w in range(len(num)):
    for q in let:
        chess_board[w].append(f'{q}{num[w]}')

for w in range(len(y)):
    for q in x:
        chess_board2[w].append([q, y[w]])

for y in range(8):
    for x in range(8):
        board_labels_dict.update({str(chess_board2[x][y]): chess_board[x][y]})

game_state_dict = board_labels_dict.copy()

game_state = [[1] * 8 for i in range(8)]


def game_state_update(board):
    for x in game_state_dict:
        game_state_dict[x] = None

    for x in board:
        for y in x[1:]:
            for z in game_state_dict:
                if str(y.position) == z:
                    game_state_dict.update({z: str(y.ID)})

    count = 0
    count2 = 0

    for x in game_state_dict.values():
        game_state[count][count2] = x
        count += 1

        if count == 8:
            count = 0
            count2 += 1

    # for x in game_state:
    #     print(x)


# for x in chess_board2:
#     print(x)
pass

# q_table_dict = {}
#
# # king
# for x in range(8):
#     q_table_dict[x] = f'K{x}'
#
# # queen
# for x in range(8, 62):
#     q_table_dict[x] = f'Q{x - 8}'
#
# # rook
# for x in range(62, 90):
#     q_table_dict[x] = f'R{x - 62}'
#
# # bishop
# for x in range(90, 116):
#     q_table_dict[x] = f'B{x - 90}'
#
# # knight
# for x in range(116, 124):
#     q_table_dict[x] = f'N{x - 116}'
#
# # pawn
# for x in range(124, 128):
#     q_table_dict[x] = f'P{x - 124}'

# print(q_table_dict)
# print(len(q_table_dict))

# for item in q_table_dict.items():
#     print(item)

# white_action_space_dict = {
#     0: [100, 100, 'K'], 1: [-100, -100, 'K'], 2: [-100, 100, 'K'], 3: [100, -100, 'K'],
#     4: [100, 0, 'K'], 5: [0, 100, 'K'], 6: [-100, 0, 'K'], 7: [0, -100, 'K'],
#     8: [100, 0, 'Q'], 9: [200, 0, 'Q'], 10: [300, 0, 'Q'], 11: [400, 0, 'Q'],
#     12: [500, 0, 'Q'], 13: [600, 0, 'Q'], 14: [700, 0, 'Q'], 15: [0, 100, 'Q'],
#     16: [0, 200, 'Q'], 17: [0, 300, 'Q'], 18: [0, 400, 'Q'], 19: [0, 500, 'Q'],
#     20: [0, 600, 'Q'], 21: [0, 700, 'Q'], 22: [-100, 0, 'Q'], 23: [-200, 0, 'Q'],
#     24: [-300, 0, 'Q'], 25: [-400, 0, 'Q'], 26: [-500, 0, 'Q'], 27: [-600, 0, 'Q'],
#     28: [-700, 0, 'Q'], 29: [0, -100, 'Q'], 30: [0, -200, 'Q'], 31: [0, -300, 'Q'],
#     32: [0, -400, 'Q'], 33: [0, -500, 'Q'], 34: [0, -600, 'Q'], 35: [0, -700, 'Q'],
#     36: [100, 100, 'Q'], 37: [200, 200, 'Q'], 38: [300, 300, 'Q'], 39: [400, 400, 'Q'],
#     40: [500, 500, 'Q'], 41: [600, 600, 'Q'], 42: [700, 700, 'Q'], 43: [-100, -100, 'Q'],
#     44: [-200, -200, 'Q'], 45: [-300, -300, 'Q'], 46: [-400, -400, 'Q'], 47: [-500, -500, 'Q'],
#     48: [-600, -600, 'Q'], 49: [-700, -700, 'Q'], 50: [100, -100, 'Q'], 51: [-100, 100, 'Q'],
#     52: [-200, 200, 'Q'], 53: [200, -200, 'Q'], 54: [300, -300, 'Q'], 55: [-300, 300, 'Q'],
#     56: [400, -400, 'Q'], 57: [-400, 400, 'Q'], 58: [500, -500, 'Q'], 59: [-500, 500, 'Q'],
#     60: [600, -600, 'Q'], 61: [-600, 600, 'Q'], 62: [600, -600, 'Q'], 63: [-600, 600, 'Q'],
#     64: [100, 0, 'R1'], 65: [200, 0, 'R1'], 66: [300, 0, 'R1'], 67: [400, 0, 'R1'],
#     68: [500, 0, 'R1'], 69: [600, 0, 'R1'], 70: [700, 0, 'R1'], 71: [0, 100, 'R1'],
#     72: [0, 200, 'R1'], 73: [0, 300, 'R1'], 74: [0, 400, 'R1'], 75: [0, 500, 'R1'],
#     76: [0, 600, 'R1'], 77: [0, 700, 'R1'], 78: [-100, 0, 'R1'], 79: [-200, 0, 'R1'],
#     80: [-300, 0, 'R1'], 81: [-400, 0, 'R1'], 82: [-500, 0, 'R1'], 83: [-600, 0, 'R1'],
#     84: [-700, 0, 'R1'], 85: [0, -100, 'R1'], 86: [0, -200, 'R1'], 87: [0, -300, 'R1'],
#     88: [0, -400, 'R1'], 89: [0, -500, 'R1'], 90: [0, -600, 'R1'], 91: [0, -700, 'R1'],
#     92: [100, 100, 'LB'], 93: [200, 200, 'LB'], 94: [300, 300, 'LB'], 95: [400, 400, 'LB'],
#     96: [500, 500, 'LB'], 97: [600, 600, 'LB'], 98: [700, 700, 'LB'], 99: [-100, 100, 'LB'],
#     100: [-200, 200, 'LB'], 101: [-300, 300, 'LB'], 102: [-400, 400, 'LB'], 103: [-500, 500, 'LB'],
#     104: [-600, 600, 'LB'], 105: [100, -100, 'LB'], 106: [200, -200, 'LB'], 107: [300, -300, 'LB'],
#     108: [400, -400, 'LB'], 109: [500, -500, 'LB'], 110: [600, -600, 'LB'], 111: [-100, -100, 'LB'],
#     112: [-200, -200, 'LB'], 113: [-300, -300, 'LB'], 114: [-400, -400, 'LB'], 115: [-500, -500, 'LB'],
#     116: [-600, -600, 'LB'], 117: [-700, -700, 'LB'], 118: [200, 100, 'N1'], 119: [-200, 100, 'N1'],
#     120: [200, -100, 'N1'], 121: [-200, -100, 'N1'], 122: [100, 200, 'N1'], 123: [-100, 200, 'N1'],
#     124: [100, -200, 'N1'], 125: [-100, -200, 'N1'], 126: [0, -100, 'P1'], 127: [0, -200, 'P1'],
#     128: [100, -100, 'P1'], 129: [-100, -100, 'P1'], 130: [0, -100, 'P2'], 131: [0, -200, 'P2'],
#     132: [100, -100, 'P2'], 133: [-100, -100, 'P2'], 134: [0, -100, 'P3'], 135: [0, -200, 'P3'],
#     136: [100, -100, 'P3'], 137: [-100, -100, 'P3'], 138: [0, -100, 'P4'], 139: [0, -200, 'P4'],
#     140: [100, -100, 'P4'], 141: [-100, -100, 'P4'], 142: [0, -100, 'P5'], 143: [0, -200, 'P5'],
#     144: [100, -100, 'P5'], 145: [-100, -100, 'P5'], 146: [0, -100, 'P6'], 147: [0, -200, 'P6'],
#     148: [100, -100, 'P6'], 149: [-100, -100, 'P6'], 150: [0, -100, 'P7'], 151: [0, -200, 'P7'],
#     152: [100, -100, 'P7'], 153: [-100, -100, 'P7'], 154: [0, -100, 'P8'], 155: [0, -200, 'P8'],
#     156: [100, -100, 'P8'], 157: [-100, -100, 'P8'], 158: [200, 100, 'N2'], 159: [-200, 100, 'N2'],
#     160: [200, -100, 'N2'], 161: [-200, -100, 'N2'], 162: [100, 200, 'N2'], 163: [-100, 200, 'N2'],
#     164: [100, -200, 'N2'], 165: [-100, -200, 'N2'], 166: [100, 0, 'R2'], 167: [200, 0, 'R2'],
#     168: [300, 0, 'R2'], 169: [400, 0, 'R2'], 170: [500, 0, 'R2'], 171: [600, 0, 'R2'],
#     172: [700, 0, 'R2'], 173: [0, 100, 'R2'], 174: [0, 200, 'R2'], 175: [0, 300, 'R2'],
#     176: [0, 400, 'R2'], 177: [0, 500, 'R2'], 178: [0, 600, 'R2'], 179: [0, 700, 'R2'],
#     180: [-100, 0, 'R2'], 181: [-200, 0, 'R2'], 182: [-300, 0, 'R2'], 183: [-400, 0, 'R2'],
#     184: [-500, 0, 'R2'], 185: [-600, 0, 'R2'], 186: [-700, 0, 'R2'], 187: [0, -100, 'R2'],
#     188: [0, -200, 'R2'], 189: [0, -300, 'R2'], 190: [0, -400, 'R2'], 191: [0, -500, 'R2'],
#     192: [0, -600, 'R2'], 193: [0, -700, 'R2'], 194: [100, 100, 'DB'], 195: [200, 200, 'DB'],
#     196: [300, 300, 'B'], 197: [400, 400, 'DB'], 198: [500, 500, 'DB'], 199: [600, 600, 'DB'],
#     200: [700, -700, 'DB'], 201: [-100, 100, 'DB'], 202: [-200, 200, 'DB'], 203: [-300, 300, 'DB'],
#     204: [-400, 400, 'DB'], 205: [-500, 500, 'DB'], 206: [-600, 600, 'DB'], 207: [100, -100, 'DB'],
#     208: [200, -200, 'DB'], 209: [300, -300, 'DB'], 210: [400, -400, 'DB'], 211: [500, -500, 'DB'],
#     212: [600, -600, 'DB'], 213: [-100, -100, 'DB'], 214: [-200, -200, 'DB'], 215: [-300, -300, 'DB'],
#     216: [-400, -400, 'DB'], 217: [-500, -500, 'DB'], 218: [-600, -600, 'DB'], 219: [-700, 700, 'DB']
# }
#
# black_action_space_dict = {
#     0: [100, 100, 'K'], 1: [-100, -100, 'K'], 2: [-100, 100, 'K'], 3: [100, -100, 'K'],
#     4: [100, 0, 'K'], 5: [0, 100, 'K'], 6: [-100, 0, 'K'], 7: [0, -100, 'K'],
#     8: [100, 0, 'Q'], 9: [200, 0, 'Q'], 10: [300, 0, 'Q'], 11: [400, 0, 'Q'],
#     12: [500, 0, 'Q'], 13: [600, 0, 'Q'], 14: [700, 0, 'Q'], 15: [0, 100, 'Q'],
#     16: [0, 200, 'Q'], 17: [0, 300, 'Q'], 18: [0, 400, 'Q'], 19: [0, 500, 'Q'],
#     20: [0, 600, 'Q'], 21: [0, 700, 'Q'], 22: [-100, 0, 'Q'], 23: [-200, 0, 'Q'],
#     24: [-300, 0, 'Q'], 25: [-400, 0, 'Q'], 26: [-500, 0, 'Q'], 27: [-600, 0, 'Q'],
#     28: [-700, 0, 'Q'], 29: [0, -100, 'Q'], 30: [0, -200, 'Q'], 31: [0, -300, 'Q'],
#     32: [0, -400, 'Q'], 33: [0, -500, 'Q'], 34: [0, -600, 'Q'], 35: [0, -700, 'Q'],
#     36: [100, 100, 'Q'], 37: [200, 200, 'Q'], 38: [300, 300, 'Q'], 39: [400, 400, 'Q'],
#     40: [500, 500, 'Q'], 41: [600, 600, 'Q'], 42: [700, 700, 'Q'], 43: [-100, -100, 'Q'],
#     44: [-200, -200, 'Q'], 45: [-300, -300, 'Q'], 46: [-400, -400, 'Q'], 47: [-500, -500, 'Q'],
#     48: [-600, -600, 'Q'], 49: [-700, -700, 'Q'], 50: [100, -100, 'Q'], 51: [-100, 100, 'Q'],
#     52: [-200, 200, 'Q'], 53: [200, -200, 'Q'], 54: [300, -300, 'Q'], 55: [-300, 300, 'Q'],
#     56: [400, -400, 'Q'], 57: [-400, 400, 'Q'], 58: [500, -500, 'Q'], 59: [-500, 500, 'Q'],
#     60: [600, -600, 'Q'], 61: [-600, 600, 'Q'], 62: [600, -600, 'Q'], 63: [-600, 600, 'Q'],
#     64: [100, 0, 'R1'], 65: [200, 0, 'R1'], 66: [300, 0, 'R1'], 67: [400, 0, 'R1'],
#     68: [500, 0, 'R1'], 69: [600, 0, 'R1'], 70: [700, 0, 'R1'], 71: [0, 100, 'R1'],
#     72: [0, 200, 'R1'], 73: [0, 300, 'R1'], 74: [0, 400, 'R1'], 75: [0, 500, 'R1'],
#     76: [0, 600, 'R1'], 77: [0, 700, 'R1'], 78: [-100, 0, 'R1'], 79: [-200, 0, 'R1'],
#     80: [-300, 0, 'R1'], 81: [-400, 0, 'R1'], 82: [-500, 0, 'R1'], 83: [-600, 0, 'R1'],
#     84: [-700, 0, 'R1'], 85: [0, -100, 'R1'], 86: [0, -200, 'R1'], 87: [0, -300, 'R1'],
#     88: [0, -400, 'R1'], 89: [0, -500, 'R1'], 90: [0, -600, 'R1'], 91: [0, -700, 'R1'],
#     92: [100, 100, 'LB'], 93: [200, 200, 'LB'], 94: [300, 300, 'LB'], 95: [400, 400, 'LB'],
#     96: [500, 500, 'LB'], 97: [600, 600, 'LB'], 98: [700, 700, 'LB'], 99: [-100, 100, 'LB'],
#     100: [-200, 200, 'LB'], 101: [-300, 300, 'LB'], 102: [-400, 400, 'LB'], 103: [-500, 500, 'LB'],
#     104: [-600, 600, 'LB'], 105: [100, -100, 'LB'], 106: [200, -200, 'LB'], 107: [300, -300, 'LB'],
#     108: [400, -400, 'LB'], 109: [500, -500, 'LB'], 110: [600, -600, 'LB'], 111: [-100, -100, 'LB'],
#     112: [-200, -200, 'LB'], 113: [-300, -300, 'LB'], 114: [-400, -400, 'LB'], 115: [-500, -500, 'LB'],
#     116: [-600, -600, 'LB'], 117: [-700, -700, 'LB'], 118: [200, 100, 'N1'], 119: [-200, 100, 'N1'],
#     120: [200, -100, 'N1'], 121: [-200, -100, 'N1'], 122: [100, 200, 'N1'], 123: [-100, 200, 'N1'],
#     124: [100, -200, 'N1'], 125: [-100, -200, 'N1'], 126: [0, 100, 'P1'], 127: [0, 200, 'P1'],
#     128: [100, 100, 'P1'], 129: [-100, 100, 'P1'], 130: [0, 100, 'P2'], 131: [0, 200, 'P2'],
#     132: [100, 100, 'P2'], 133: [-100, 100, 'P2'], 134: [0, 100, 'P3'], 135: [0, 200, 'P3'],
#     136: [100, 100, 'P3'], 137: [-100, 100, 'P3'], 138: [0, 100, 'P4'], 139: [0, 200, 'P4'],
#     140: [100, 100, 'P4'], 141: [-100, 100, 'P4'], 142: [0, 100, 'P5'], 143: [0, 200, 'P5'],
#     144: [100, 100, 'P5'], 145: [-100, 100, 'P5'], 146: [0, 100, 'P6'], 147: [0, 200, 'P6'],
#     148: [100, 100, 'P6'], 149: [-100, 100, 'P6'], 150: [0, 100, 'P7'], 151: [0, 200, 'P7'],
#     152: [100, 100, 'P7'], 153: [-100, 100, 'P7'], 154: [0, 100, 'P8'], 155: [0, 200, 'P8'],
#     156: [100, 100, 'P8'], 157: [-100, 100, 'P8'], 158: [200, 100, 'N2'], 159: [-200, 100, 'N2'],
#     160: [200, -100, 'N2'], 161: [-200, -100, 'N2'], 162: [100, 200, 'N2'], 163: [-100, 200, 'N2'],
#     164: [100, -200, 'N2'], 165: [-100, -200, 'N2'], 166: [100, 0, 'R2'], 167: [200, 0, 'R2'],
#     168: [300, 0, 'R2'], 169: [400, 0, 'R2'], 170: [500, 0, 'R2'], 171: [600, 0, 'R2'],
#     172: [700, 0, 'R2'], 173: [0, 100, 'R2'], 174: [0, 200, 'R2'], 175: [0, 300, 'R2'],
#     176: [0, 400, 'R2'], 177: [0, 500, 'R2'], 178: [0, 600, 'R2'], 179: [0, 700, 'R2'],
#     180: [-100, 0, 'R2'], 181: [-200, 0, 'R2'], 182: [-300, 0, 'R2'], 183: [-400, 0, 'R2'],
#     184: [-500, 0, 'R2'], 185: [-600, 0, 'R2'], 186: [-700, 0, 'R2'], 187: [0, -100, 'R2'],
#     188: [0, -200, 'R2'], 189: [0, -300, 'R2'], 190: [0, -400, 'R2'], 191: [0, -500, 'R2'],
#     192: [0, -600, 'R2'], 193: [0, -700, 'R2'], 194: [100, 100, 'DB'], 195: [200, 200, 'DB'],
#     196: [300, 300, 'B'], 197: [400, 400, 'DB'], 198: [500, 500, 'DB'], 199: [600, 600, 'DB'],
#     200: [700, -700, 'DB'], 201: [-100, 100, 'DB'], 202: [-200, 200, 'DB'], 203: [-300, 300, 'DB'],
#     204: [-400, 400, 'DB'], 205: [-500, 500, 'DB'], 206: [-600, 600, 'DB'], 207: [100, -100, 'DB'],
#     208: [200, -200, 'DB'], 209: [300, -300, 'DB'], 210: [400, -400, 'DB'], 211: [500, -500, 'DB'],
#     212: [600, -600, 'DB'], 213: [-100, -100, 'DB'], 214: [-200, -200, 'DB'], 215: [-300, -300, 'DB'],
#     216: [-400, -400, 'DB'], 217: [-500, -500, 'DB'], 218: [-600, -600, 'DB'], 219: [-700, 700, 'DB']
# }


# in the future use board positions instead of independent actions?


# def move(choice):
#     dict_key = random.randint(0, 231)
#
#     return choice[dict_key]


# for x in range(5):
#     print(move(white_action_space_dict))



# # king
# for x in range(8):
#     black_action_space_dict[x].append('K')
#
# # queen
# for x in range(8, 62):
#     black_action_space_dict[x].append('Q')
#
# # rook
# for x in range(62, 90):
#     black_action_space_dict[x].append('R')
#
# # bishop
# for x in range(90, 116):
#     black_action_space_dict[x].append('B')
#
# # knight
# for x in range(116, 124):
#     black_action_space_dict[x].append('N')
#
# # pawn
# for x in range(124, 128):
#     black_action_space_dict[x].append('P')
