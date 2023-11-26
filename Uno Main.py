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
    player3_deck = [0]
    player4_deck = [0]
elif variable_player_count == 3:
    player1_deck, player2_deck, player3_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)
    player4_deck = [0]
elif variable_player_count == 4:
    player1_deck, player2_deck, player3_deck, player4_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)

playerX_deck = player1_deck

# takes a players deck and prints its contents
def card_reader(playerX_deck):
    card_info = [
        "Red 1", "Red 2", "Red 3", "Red 4", "Red 5", "Red 6", "Red 7", "Red 8", "Red 9",
        "Yellow 1", "Yellow 2", "Yellow 3", "Yellow 4", "Yellow 5", "Yellow 6", "Yellow 7", "Yellow 8", "Yellow 9",
        "Green 1", "Green 2", "Green 3", "Green 4", "Green 5", "Green 6", "Green 7", "Green 8", "Green 9",
        "Blue 1", "Blue 2", "Blue 3", "Blue 4", "Blue 5", "Blue 6", "Blue 7", "Blue 8", "Blue 9",
        "Red Special Skip", "Red Special Reverse", "Red Special +2",
        "Yellow Special Skip", "Yellow Special Reverse", "Yellow Special +2",
        "Green Special Skip", "Green Special Reverse", "Green Special +2",
        "Blue Special Skip", "Blue Special Reverse", "Blue Special +2",
        "Wild Card Color Change", "Wild Card Color Change", "Wild Card +4 Color Change", "Wild Card +4 Color Change"
    ]
    # creates an empty list to be used later
    output = []

    # iterates through each value (n) of the player list, and appends to a new list. this new list rather than having
    # number values has the string values associated with its position in the card_info list.
    #  if playerX_deck[0] has value 12, it will be "Yellow 4" for example.
    for n in playerX_deck:
        output.append(card_info[n])
    print(output)
    return

def win_condition_check(player1_deck, player2_deck, player3_deck, player4_deck):
    if len(player1_deck) == 0:
        return True, 0
    elif len(player2_deck) == 0:
        return True, 1
    elif len(player3_deck) == 0:
        return True, 2
    elif len(player4_deck) == 0:
        return True, 3
    else:
        return False, 4


card_reader(player1_deck)


