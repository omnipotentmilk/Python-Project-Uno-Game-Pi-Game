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

    # Initialize a empty list which will be used to help create the player deck
    players_deck_temp = []

    # Depending on the number of players, slice the original uno deck 7 cards at a time and append resulting list
    # to temp deck for later
    for _ in range(variable_player_count):
        player_deck = uno_deck_instance[:7]
        uno_deck_instance = uno_deck_instance[7:]
        players_deck_temp.append(player_deck)

    # Use unpacking to return each players deck
    if variable_player_count == 2:
        player1_deck, player2_deck = players_deck_temp
        return player1_deck, player2_deck, uno_deck_instance, players_deck_temp
    elif variable_player_count == 3:
        player1_deck, player2_deck, player3_deck = players_deck_temp
        return player1_deck, player2_deck, player3_deck, uno_deck_instance, players_deck_temp
    elif variable_player_count == 4:
        player1_deck, player2_deck, player3_deck, player4_deck = players_deck_temp
        return player1_deck, player2_deck, player3_deck, player4_deck, uno_deck_instance, players_deck_temp

# store the player decks and the uno deck as a variable to be easily accessible
if variable_player_count == 2:
    player1_deck, player2_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)
elif variable_player_count == 3:
    player1_deck, player2_deck, player3_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)
elif variable_player_count == 4:
    player1_deck, player2_deck, player3_deck, player4_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)

print(player1_deck)


