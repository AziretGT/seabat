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