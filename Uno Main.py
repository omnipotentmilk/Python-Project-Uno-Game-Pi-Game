import random

def game_initialize():
    while True:
        try:
            player_count = int(input("Welcome to UnoPy! Enter Player Number Selection (2-4): "))
            if 2 <= player_count <= 4:
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



# store the player decks and the uno deck as a variable(s) to be easily accessible
# Unused players are given a deck of [-1] so it is very obvious when debugging if a player that should not be
# included in the game has somehow gotten into a turn
if variable_player_count == 2:
    player1_deck, player2_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)
    player3_deck = [-1]
    player4_deck = [-1]
elif variable_player_count == 3:
    player1_deck, player2_deck, player3_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)
    player4_deck = [-1]
elif variable_player_count == 4:
    player1_deck, player2_deck, player3_deck, player4_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)



# takes a players deck and prints its contents
# this is neccessary because the game logic only works with numbers (ex: Game will be working with the list [0, 1]
# But the player will be looking at what those numbers represent [Red 0, Red1] )
def card_reader(input_deck):
    card_info = [
        "Red 0", "Red 1", "Red 2", "Red 3", "Red 4", "Red 5", "Red 6", "Red 7", "Red 8", "Red 9",
        "Yellow 0", "Yellow 1", "Yellow 2", "Yellow 3", "Yellow 4", "Yellow 5", "Yellow 6", "Yellow 7", "Yellow 8", "Yellow 9",
        "Green 0", "Green 1", "Green 2", "Green 3", "Green 4", "Green 5", "Green 6", "Green 7", "Green 8", "Green 9",
        "Blue 0", "Blue 1", "Blue 2", "Blue 3", "Blue 4", "Blue 5", "Blue 6", "Blue 7", "Blue 8", "Blue 9",
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
    #  if playerX_deck[0] has value 12, it will be "Yellow 1" for example.
    for n in input_deck:
        if 0 <= n < len(card_info):
            output.append(card_info[n])
        else:
            output.append(f"Invalid Card, cards number was:{n}") # this was added to debug if any card number
                                                                 # is messed up because i was having that issue
    return output



# self explanatory checks if length of any deck is 0. if it is that means that player has won
# true false and 0-4 is simply for future use, unimplemented yet
def win_condition_check(player1_deck, player2_deck, player3_deck, player4_deck):
    if len(player1_deck) == 0:
        return 0
    elif len(player2_deck) == 0:
        return 1
    elif len(player3_deck) == 0:
        return 2
    elif len(player4_deck) == 0:
        return 3
    else:
        return False



# this will be the function that controls player actions. when given input deck and current deck will allow player to
# do specific tasks
def player_card_turn(input_deck, remaining_deck):
    remaining_deck_instance = remaining_deck
    print(f"Current Cards: {card_reader(input_deck)}")
    print(f"Top Deck Card: {card_reader([remaining_deck_instance[0]])}")
    cards_drawn = 0
    cards_played = 0
    while True:
        try:
            player_selection = int(input("0 to play a card | 1 to draw a card | 2 to end turn | "))
            if (player_selection < 3 and player_selection > 0):
                if player_selection == 0:
                    print("SUccesffully chose 0")
                    break
                elif player_selection == 1:
                    print("SUccesffully chose 1")
                    break
                elif player_selection == 2:
                    print("SUccesffully chose 2")
                    break
            else:
                print("Invalid input. Please enter a number between 0 and 2.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return



# this will be the game loop which will act as the central location for the game to function
# specific things (such as reading player decks, checking if a player has won, and card-play logic) will be
# located seperately and called by this master function
def game_loop(player1_deck, player2_deck, player3_deck, player4_deck, variable_player_count, remaining_deck):
    current_player = list(range(variable_player_count))
    player_count = variable_player_count
    ####### remove later #########################
    # player_count variable currently has NO USE #
    ##############################################
    while win_condition_check(player1_deck, player2_deck, player3_deck, player4_deck) == False:
        if len(current_player) == 2:
            print("Player 1 Turn")
            card_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
            ############## remove later #############################################################################
            # sidenote i might make all this into its own function and just call it here because its very repetitive
            ########### remove later ################################################################################
        elif len(current_player) == 3:
            print("Player 1 Turn")
            card_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
        elif len(current_player) == 4:
            print("Player 1 Turn")
            card_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
        break
    return

game_loop(player1_deck, player2_deck, player3_deck, player4_deck, variable_player_count, remaining_deck)
# this giant mess of a function call just calls the master function with every possible input it would need to control
# eerything else and successfully control the game