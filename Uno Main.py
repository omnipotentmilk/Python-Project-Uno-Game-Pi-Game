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



# takes a players deck and prints its contents
# this is neccessary because the game logic only works with numbers (ex: Game will be working with the list [0, 1]
# But the player will be looking at what those numbers represent [Red 0, Red1] )
def deck_reader(input_deck):
    output = []

    for card in input_deck:
        card_attributes = card_attribute_assigner(card)
        output.append(card_attributes)

    return output



# Interprets inputted cards and returns what their attributes are for the purposes of comparison
# NOT for user display, only for game logic
# This and the function above could easily be combined, however, for the sake of time I opted not to do that
def card_attribute_assigner(input_card): # Inputted in integer form

    attributes = []

    if input_card < 0:
        attributes.append(f"Invalid {input_card}")

    if (0 <= input_card <= 9) or (40 <= input_card <= 42):
        attributes.append("red")
    elif (10 <= input_card <= 19) or (43 <= input_card <= 45):
        attributes.append("yellow")
    elif (20 <= input_card <= 29) or (46 <= input_card <= 48):
        attributes.append("green")
    elif (30 <= input_card <= 39) or (49 <= input_card <= 51):
        attributes.append("blue")

    if (input_card in (55, 54, 53, 52)):
        attributes.append("wild")

    if input_card in (40, 43, 46, 49):
        attributes.append("skip")

    if input_card in (41, 44, 47, 50):
        attributes.append("reverse")

    if input_card in (42, 45, 48, 51):
        attributes.append("+2")

    if input_card in (54, 55):
        attributes.append("+4")

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
    cards_drawn = 0
    cards_played = 0
    attribute_card_player = -1
    attribute_card_deck = -1
    selected_card = -1
    valid_card_placed = False
    while True:
        try:

            print("")
            print(f"Current Cards: {deck_reader(input_deck)}")
            print(f"Top Deck Card: {deck_reader([remaining_deck_instance[0]])}")
            player_selection = int(input("0 to play a card | 1 to draw a card | 2 to end turn | "))
            if (player_selection < 3 and player_selection > -1): # only pass if valid action
                if player_selection == 0:

                    if cards_played < 1: # In the case a player attempts to play a card
                       while True:
                        try:
                            selected_card = int(input(f"Please select a card (1 - {len(input_deck)}) or 0 to cancel |  "))
                            selected_card -= 1
                            if selected_card == -1:
                                break

                            # in the case the player selects a card from their deck, compare it against deck
                            attribute_card_player = card_attribute_assigner(input_deck[selected_card])
                            attribute_card_deck = [(attribute_card_player[0])]
                            for attribute in attribute_card_deck:
                                if attribute in attribute_card_player:
                                    valid_card_placed = True
                            if "wild" in attribute_card_player:
                                valid_card_placed = True

                            # if comparison shows success, end action. if not, end action
                            if valid_card_placed == True:
                                cards_played += 1
                                print(f"Card {deck_reader([int(input_deck[int(selected_card)])])} played!")
                                break
                            else:
                                print("Cannot play this card.")
                                continue

                        # in the case the player does not enter an integer
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                            continue
                    else:
                        print("Cannot play another card.")
                        continue

                elif player_selection == 1: # In the case the player attempts to draw a card
                    if cards_drawn < 1 and cards_played < 1:
                        cards_drawn += 1
                        input_deck.append(remaining_deck_instance[-1])
                        remaining_deck_instance.pop()
                        print("Drew a card!")
                        continue
                    else:
                        print("Cannot draw a card.")
                        continue
                    break

                elif player_selection == 2: # in the case the player attempts to end their turn
                    if (cards_drawn > 0) or (cards_played > 0):
                        print("Turn ending . . . ")
                        break
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
        # a function instead
        # second option, use global variables and f"player {n} turn" to be infnitely modular
        # append players to the list to add players
        ######################## remove later #####################################################################

        if len(current_player) == 2:
            print("")
            print("Player 1 Turn")
            deck_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
        elif len(current_player) == 3:
            print("Player 1 Turn")
            deck_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
        elif len(current_player) == 4:
            print("Player 1 Turn")
            deck_reader(player1_deck)
            player_card_turn(player1_deck, remaining_deck)
        break
    return



# Loop for testing purposes only #
while True:
    try:
        # stores the output of our initialize as a variable
        variable_player_count = game_initialize()

        # this stores the player decks and the uno deck as a variable(s) to be easily accessible
        # Unused players are given a deck of [-1] so it is very obvious when debugging if a player that should not be
        # included in the game has somehow gotten into a turn
        if variable_player_count == 2:
            player1_deck, player2_deck, remaining_deck, combined_deck_list = deck_builder(variable_player_count)
            player3_deck = [-1]
            player4_deck = [-1]
        elif variable_player_count == 3:
            player1_deck, player2_deck, player3_deck, remaining_deck, combined_deck_list = deck_builder(
                variable_player_count)
            player4_deck = [-1]
        elif variable_player_count == 4:
            player1_deck, player2_deck, player3_deck, player4_deck, remaining_deck, combined_deck_list = deck_builder(
                variable_player_count)


        # Calls the main game loop func and provides all variables it needs
        game_loop(player1_deck, player2_deck, player3_deck, player4_deck, variable_player_count, remaining_deck)

        # lets me quit while debugging
        RAH = int(input("enter integer"))
        continue
    except ValueError:
        break


