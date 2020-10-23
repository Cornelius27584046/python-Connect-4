import math
import random
import sys

import numpy as np
import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

WINDOW_LENGTH = 4
EMPTY = 0

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2


def create_board():
    tboard = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return tboard


def drop_piece(your_board, your_row, column, piece):
    your_board[your_row][column] = piece


def is_valid_location(your_board, column):
    return your_board[ROW_COUNT - 1][column] == 0


def get_next_open_row(your_board, column):
    for r in range(ROW_COUNT):
        if your_board[r][column] == 0:
            return r


def print_board(your_board):
    print(np.flip(your_board, 0))


def winning_move(your_board, piece):
    # check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if your_board[r][c] == piece and your_board[r][c + 1] == piece and your_board[r][c + 2] == piece and \
                    your_board[r][c + 3] == piece:
                return True

    # check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if your_board[r][c] == piece and your_board[r + 1][c] == piece and your_board[r + 2][c] == piece and \
                    your_board[r + 3][c] == piece:
                return True

    # check positive slope diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if your_board[r][c] == piece and your_board[r + 1][c + 1] == piece and your_board[r + 2][c + 2] == piece and \
                    your_board[r + 3][c + 3] == piece:
                return True

    # check negative slope diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if your_board[r][c] == piece and your_board[r - 1][c + 1] == piece and your_board[r - 2][c + 2] == piece and \
                    your_board[r - 3][c + 3] == piece:
                return True


def evaluate_window(window, piece):
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(your_board, piece):
    score = 0
    # score center column
    center_arr = [int(i) for i in list(your_board[:, COLUMN_COUNT//2])]
    center_count = center_arr.count(piece)
    score += center_count + 6

    # horizontal score
    for r in range(ROW_COUNT):
        row_arr = [int(i) for i in list(your_board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_arr[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # vertical score
    for c in range(COLUMN_COUNT):
        col_arr = [int(i) for i in list(your_board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_arr[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [your_board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # score negative sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [your_board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(your_board):
    return winning_move(your_board, PLAYER_PIECE) or winning_move(your_board, AI_PIECE) or len(get_valid_locations(your_board)) == 0


def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 1000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -1000000000
            else:
                return None, 0
        else:  # depth == 0
            return None, score_position(board, AI_PIECE)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for colm in valid_locations:
            rowm = get_next_open_row(board, colm)
            b_copy = board.copy()
            drop_piece(b_copy, rowm, colm, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            # print(new_score)
            if new_score > value:
                value = new_score
                column = colm
        return column, value

    else:  # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for colm in valid_locations:
            rowm = get_next_open_row(board, colm)
            c_copy = board.copy()
            drop_piece(c_copy, rowm, colm, PLAYER_PIECE)
            new_score = minimax(c_copy, depth-1, True)[1]
            # print(new_score)
            if new_score < value:
                value = new_score
                column = colm
        return column, value


def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 1000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -1000000000
            else:
                return None, 0
        else:  # depth == 0
            return None, score_position(board, AI_PIECE)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for colm in valid_locations:
            rowm = get_next_open_row(board, colm)
            b_copy = board.copy()
            drop_piece(b_copy, rowm, colm, AI_PIECE)
            new_score = minimax_alpha_beta(b_copy, depth-1, alpha, beta, False)[1]
            # print(new_score)
            if new_score > value:
                value = new_score
                column = colm
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for colm in valid_locations:
            rowm = get_next_open_row(board, colm)
            c_copy = board.copy()
            drop_piece(c_copy, rowm, colm, PLAYER_PIECE)
            new_score = minimax_alpha_beta(c_copy, depth-1, alpha, beta, True)[1]
            # print(new_score)
            if new_score < value:
                value = new_score
                column = colm
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(your_board):
    valid_locs = []
    for colm in range(COLUMN_COUNT):
        if is_valid_location(your_board, colm):
            valid_locs.append(colm)

    return valid_locs


def pick_best_move(your_board, piece):
    best_score = 0
    valid_locations = get_valid_locations(your_board)
    best_col = random.choice(valid_locations)
    for colm in valid_locations:
        rowm = get_next_open_row(your_board, colm)
        temp_board = your_board.copy()
        drop_piece(temp_board, rowm, colm, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = colm

    return best_col


def draw_board(your_board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if your_board[r][c] == 0:
                pygame.draw.circle(screen, BLACK,
                                   (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + int(SQUARESIZE * 1.5)),
                                   RADIUS)
            elif your_board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED,
                                   (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + int(SQUARESIZE * 1.5)),
                                   RADIUS)
            elif your_board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW,
                                   (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + int(SQUARESIZE * 1.5)),
                                   RADIUS)
    pygame.display.update()


board = create_board()
game_over = False

turn = random.randint(PLAYER, AI)

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:  # game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # ask for player1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn %= 2
                    draw_board(np.flip(board, 0))

    # ask for player2 input
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT - 1)
        # col = pick_best_move(board, AI_PIECE)

        col, minimax_score = minimax_alpha_beta(board, 3, -math.inf, math.inf, True)
        # col, minimax_score = minimax(board, 3, True)
        # print(col, ": ", minimax_score)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            pygame.time.wait(300)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            turn += 1
            turn %= 2

    # print_board(board)
    draw_board(np.flip(board, 0))
    # print("tiped")

    if game_over:
        pygame.time.wait(5000)
