import random

def game_initialize():
    while True:
        try:
            player_count = int(input("Welcome to UnoPy! Enter Player Number Selection (2-4): "))
            if 2 <= player_count <= 4:
                print("Selection:", player_count)
                return player_count
            else:
                print("Invalid input. Please enter a number between 2 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# store the player count to be used for other operations later
variable_player_count = game_initialize()

def deck_builder(variable_player_count):
    # create & shuffle the initial UNO deck
    uno_deck_instance = list(range(56))
    random.shuffle(uno_deck_instance)

    # Initialize a list to store 2-4 lists of length 7
    players_deck_temp = []

    # Depending on the number of players, slice the original uno deck 7 cards at a time and append that 7 length list
    # to a new list
    for _ in range(variable_player_count):
        player_deck = uno_deck_instance[:7]
        uno_deck_instance = uno_deck_instance[7:]
        players_deck_temp.append(player_deck)

    # Use unpacking to assign each player with a deck (and then the game itself a deck) then return
    # (depending on player count)
    if variable_player_count == 2:
        player1_deck, player2_deck = players_deck_temp
        return player1_deck, player2_deck, uno_deck_instance
    elif variable_player_count == 3:
        player1_deck, player2_deck, player3_deck = players_deck_temp
        return player1_deck, player2_deck, player3_deck, uno_deck_instance
    elif variable_player_count == 4:
        player1_deck, player2_deck, player3_deck, player4_deck = players_deck_temp
        return player1_deck, player2_deck, player3_deck, player4_deck, uno_deck_instance

# store the player decks and the uno deck as a variable to be used in the game later.
if variable_player_count == 2:
    player1_deck, player2_deck, game1_deck = deck_builder(variable_player_count)
elif variable_player_count == 3:
    player1_deck, player2_deck, player3_deck, game1_deck = deck_builder(variable_player_count)
elif variable_player_count == 4:
    player1_deck, player2_deck, player3_deck, player4_deck, game1_deck = deck_builder(variable_player_count)

print(player4_deck, player3_deck, player2_deck, player1_deck, game1_deck)

