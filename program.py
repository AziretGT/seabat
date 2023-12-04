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

def place_ship_manually(board, ship_size):
    while True:
        print_player_board(board, create_board(), create_board())
        try:
            position = input(f"Enter position (e.g., A:3) for ship of size {ship_size}: ").strip().upper()
            col = ord(position[0]) - ord('A')
            row = int(position[2:]) - 1

            orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()

            ship_cells = [(0, i) if orientation == 'H' else (i, 0) for i in range(ship_size)]

            if is_valid_position(board, ship_cells, row, col):
                for r, c in ship_cells:
                    board[row + r][col + c] = str(ship_size)
                break
            else:
                print("Invalid position or ships touching. Try again.")
        except (ValueError, IndexError):
            print("Invalid input format or position. Please try again.")

def place_ships_manually(board):
    ships = {
        3: 1,
        2: 2,
        1: 4
    }

    for ship_size, ship_count in ships.items():
        for _ in range(ship_count):
            place_ship_manually(board, ship_size)

def place_ships(board):
    ships = {
        3: [(0, 0), (0, 1), (0, 2)],
        2: [(0, 0), (0, 1)],
        1: [(0, 0)]
    }

    for ship_size, ship_cells in ships.items():
        for _ in range(4 if ship_size == 1 else 2):
            placed = False
            while not placed:
                row = random.randint(0, 6)
                col = random.randint(0, 6)
                orientation = random.choice(['H', 'V'])
                ship_cells = [(0, i) if orientation == 'H' else (i, 0) for i in range(ship_size)]

                if is_valid_position(board, ship_cells, row, col):
                    for r, c in ship_cells:
                        board[row + r][col + c] = str(ship_size)
                    placed = True
    return board

def is_valid_shot(board, row, col, shots_board):
    rows, cols = len(board), len(board[0])

    if not (0 <= row < rows and 0 <= col < cols):
        return False

    return shots_board[row][col] == 'O'

def player_turn(board, shots_board):
    while True:
        try:
            move = input("Enter your move (e.g., A:3): ").strip().upper()
            if len(move) < 3 or not move[0].isalpha() or not move[1] == ":" or not move[2:].isdigit():
                raise ValueError
            col = ord(move[0]) - ord('A')
            row = int(move[2:]) - 1

            if is_valid_shot(board, row, col, shots_board):
                return row, col
            else:
                print("Invalid move. Try again.")

        except ValueError:
            print("Invalid input format. Please use format like 'A:3'.")

def computer_turn(board, shots_board):
    while True:
        row = random.randint(0, 6)
        col = random.randint(0, 6)

        if is_valid_shot(board, row, col, shots_board):
            return row, col
        
def play_game():
    player_ships_board = create_board()
    computer_ships_board = create_board()
    player_shots_board = create_board()
    computer_shots_board = create_board()

    player_shots = [['O' for _ in range(7)] for _ in range(7)]
    computer_shots = [['O' for _ in range(7)] for _ in range(7)]

    print("Place your ships:")
    place_ships_manually(player_ships_board)
    print("\nComputer is placing ships...")
    time.sleep(1)
    place_ships(computer_ships_board)

    while True:
        print("\nPlayer's turn:")
        print_player_board(player_ships_board, player_shots, computer_shots)
        player_row, player_col = player_turn(computer_ships_board, computer_shots_board)

        if computer_ships_board[player_row][player_col] != 'O':
            print("Hit!")
            computer_ships_board[player_row][player_col] = 'X'
            player_shots[player_row][player_col] = 'X'
            if are_all_ships_sunk(computer_ships_board):
                print("Congratulations! You won!")
                return
        else:
            print("Miss!")
            player_shots[player_row][player_col] = '-'

        if all(all(cell in ['X', '-'] for cell in row) for row in computer_ships_board):
            print("Congratulations! You won!")
            break

        print("\nComputer's turn:")
        time.sleep(1)
        computer_row, computer_col = computer_turn(player_ships_board, player_shots_board)

        if player_ships_board[computer_row][computer_col] != 'O':
            print("Computer hit your ship!")
            player_ships_board[computer_row][computer_col] = 'X'
            computer_shots[computer_row][computer_col] = 'X'
            if are_all_ships_sunk(player_ships_board):
                print("Computer won!")
                return
        else:
            print("Computer missed!")
            computer_shots[computer_row][computer_col] = '-'

        if all(all(cell in ['X', '-'] for cell in row) for row in player_ships_board):
            print("Computer won!")
            break
