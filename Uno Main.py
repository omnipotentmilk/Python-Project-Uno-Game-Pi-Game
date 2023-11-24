import random

def game_initialize():
    while True:
        try:
            player_count = int(input("Welcome to UnoPy! Enter Player Number Selection (0-4): "))
            if 0 <= player_count <= 4:
                return player_count
            else:
                print("Invalid input. Please enter a number between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


game_initialize()