# pretty much only used during initializing when shuffling the deck
import random

################# Remove later ###################################
# Perhaps we could import a color module and color all the cards #
################################## Remove later ##################



# asks the user to specify how many players will be playing
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

# stores the output of our initialize as a variable
variable_player_count = game_initialize()



# creates the player decks (depending on player count) and the remaining decks
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

    # at the end of deck creation, if top card would be a wild card, append to back and delete.
    if (uno_deck_instance[0] == 55) or (uno_deck_instance[0] == 54) or (uno_deck_instance[0] == 53) or (uno_deck_instance[0] == 52):
        uno_deck_instance.append(0)
        uno_deck_instance.pop(0)
    else:
        pass

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



# this stores the player decks and the uno deck as a variable(s) to be easily accessible
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
    ] # If the top deck card is a wild card, i dont know what to do, impleement a fix so the first player choses what card
    # will be the wild card

    # creates an empty list to be used later
    output = []

    # responsible for doing the conversion from integer -> string
    for n in input_deck:
        if 0 <= n < len(card_info):
            output.append(card_info[n])
        else:
            output.append(f"Invalid Card, cards number was:{n}") # added to debug if any card number
                                                                 # is messed up because i was having that issue
    return output



# Interprets inputted cards and returns what their attributes are for the purposes of comparison
# NOT for user display, only for game logic
def card_attribute_assigner(input_card): # Inputted in integer form
    attributes = []
    if (0 <= input_card <= 9) or (40 <= input_card <= 42):
        attributes.append("red")
    elif (10 <= input_card <= 19) or (43 <= input_card <= 45):
        attributes.append("yellow")
    elif (20 <= input_card <= 29) or (46 <= input_card <= 48):
        attributes.append("green")
    elif (30 <= input_card <= 39) or (49 <= input_card <= 51):
        attributes.append("blue")
    if (input_card in (0, 10, 20, 30)):
        attributes.append("0")
    elif (input_card in (1, 11, 21, 31)):
        attributes.append("1")
    elif (input_card in (2, 12, 22, 32)):
        attributes.append("2")
    elif (input_card in (3, 13, 23, 33)):
        attributes.append("3")
    elif (input_card in (4, 14, 24, 34)):
        attributes.append("4")
    elif (input_card in (5, 15, 25, 35)):
        attributes.append("5")
    elif (input_card in (6, 16, 26, 36)):
        attributes.append("6")
    elif (input_card in (7, 17, 27, 37)):
        attributes.append("7")
    elif (input_card in (8, 18, 28, 38)):
        attributes.append("8")
    elif (input_card in (9, 19, 29, 39)):
        attributes.append("9")
    return attributes
    # TODO implement WILD CARD attribute and special attributes ####



# Checks to make sure no player has won the game!
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



# Holds all of the logic associated with a player turn other than checking if a played card is valid.
def player_card_turn(input_deck, remaining_deck):
    remaining_deck_instance = remaining_deck
    print(f"Current Cards: {card_reader(input_deck)}")
    print(f"Top Deck Card: {card_reader([remaining_deck_instance[0]])}")
    cards_drawn = 0
    cards_played = 0
    attribute_card_1 = -1
    attribute_card_2 = -1
    selected_card = -1
    print(input_deck) ########### remove later ##############
    while True:
        try:
            player_selection = int(input("0 to play a card | 1 to draw a card | 2 to end turn | "))
            if (player_selection < 3 and player_selection > -1): # only pass if valid action
                if player_selection == 0:
                    if cards_played < 1:
                        while True:
                            try:
                                selected_card = int(input(f"Please select a card (1 - {len(input_deck)}) |  "))
                                selected_card -= 1
                                attribute_card_1 = card_attribute_assigner(input_deck[selected_card])
                                attribute_card_2 = card_attribute_assigner(remaining_deck_instance[0])
                                print(input_deck[selected_card], remaining_deck_instance[0])
                                print(attribute_card_1, attribute_card_2)
                                ######### TEMP ###########
                                for card in attribute_card_1:
                                    if card in attribute_card_2:
                                        cards_played += 1
                                        print("TEST SUCCESS CARD PLAYED")
                                        break
                                else:
                                    print("You cannot play this card.")
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                    else:
                        print("Cannot play another card.")
                        continue
                elif player_selection == 1:
                    if cards_drawn < 1:
                        cards_drawn += 1
                        input_deck.append(remaining_deck_instance[-1])
                        remaining_deck_instance.pop()
                        print("Drew a card!")
                        print(f"Current Cards: {card_reader(input_deck)}")
                        print(f"Top Deck Card: {card_reader([remaining_deck_instance[0]])}")
                        continue
                    else:
                        print("Cannot draw another card.")
                        continue
                    break
                elif player_selection == 2:
                    if (cards_drawn > 0) or (cards_played > 0):
                        break # The user has completed all requirements for a turn
                    else:
                        print("Cannot end turn.")
                        continue
            else:
                print("Invalid input. Please enter a number between 0 and 2.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return



# master function for the game logic (Calls most other functions and requires all previous variables)
def game_loop(player1_deck, player2_deck, player3_deck, player4_deck, variable_player_count, remaining_deck):
    current_player = list(range(variable_player_count))
    while win_condition_check(player1_deck, player2_deck, player3_deck, player4_deck) == False:

        ############## remove later ###############################################################################
        # I might replace this with a function because im literally doing the same thing 3 times. i cld just call #
        # a function instead                                                                                      #
        ######################## remove later #####################################################################

        if len(current_player) == 2:
            print("Player 1 Turn")
            card_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
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