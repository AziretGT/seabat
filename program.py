import random
import time

def create_board():
    return [['O' for _ in range(7)] for _ in range(7)]

def print_player_board(player_ships, player_shots, computer_shots):
    print("   A B C D E F G")
    for i in range(7):
        print(f"{i+1} ", end="")
        for cell in player_ships[i]:
            print(cell, end=" ")
        print("    ", end="")
        for cell in player_shots[i]:
            print(cell, end=" ")
        print("    ", end="")
        for cell in computer_shots[i]:
            print(cell, end=" ")
        print()

def is_valid_position(board, ship, row, col):
    rows, cols = len(board), len(board[0])

    for r, c in ship:
        if not (0 <= row + r < rows and 0 <= col + c < cols):
            return False
        if board[row + r][col + c] != 'O':
            return False
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if (0 <= row + r + dr < rows and 0 <= col + c + dc < cols) and board[row + r + dr][col + c + dc] != 'O':
                    return False

    return True

def are_all_ships_sunk(board):
    for row in board:
        for cell in row:
            if cell in ['1', '2', '3']:
                return False
    return True