########################################################################################################################
#                                            Initialization Section                                                    #
########################################################################################################################

import random

# modular way to change the player count
def game_initialize():
    while True:
        try:
            player_count = int(input("\nWelcome to UnoPy! Please enter the player count (1-55): "))
            card_count = int(input("Please enter the number of cards per player (1-55): "))
            if 1 <= player_count <= 55 and 1 <= card_count <= 56 and (player_count * card_count) + 1 <= 56:

                # creates an important list which will essentially have surgery preformed on it later
                global_player_deck = list(range(player_count))
                return [global_player_deck, card_count]

            # handles the case that an impossible number of players or cards is chosen
            else:
                print("\nImpossible player count/card count combination. Try again")
        except ValueError:
            print("Invalid input. Please enter a valid number.")



# generates a valid uno deck, shuffles it, and properly distributes it to the players
def deck_builder(global_player_deck, global_card_count):
    uno_deck_instance = list(range(56))
    random.shuffle(uno_deck_instance)
    players_deck_temp = []
    global_player_list_decks = []

    # properly slices the main deck, adding 7 cards at a time to as an index to a temp deck.
    # temp deck would look like this [[0, 1, 2, 3, 4, 5, 6, 7],[8, 9, 10, 11, 12, 13, 14]] except randomized
    for _ in range(len(global_player_deck)):
        player_deck = uno_deck_instance[:global_card_count]
        uno_deck_instance = uno_deck_instance[global_card_count:]
        players_deck_temp.append(player_deck)

    # makes sure that the top card of the remaining deck would not be a wild or +2/+4/skip/reverse card.
    if uno_deck_instance[0] in {55, 54, 53, 52, 42, 45, 48, 51, 40, 43, 46, 49, 41, 44, 47, 50}:
        uno_deck_instance.append(uno_deck_instance[0])
        uno_deck_instance.pop(0)

    # Distribute the temporary new deck segments (which are 7 long) to the players in global_player_deck
    for i in global_player_deck:
        global_player_list_decks.append(players_deck_temp[i])

    # packages and returns the nested player deck list and the remaining deck together for output
    output = [global_player_list_decks, uno_deck_instance]
    return output



# converts card number |ex: [10]| to readable format |ex [yellow, 0]|
def card_attribute_assigner(input_card): # Inputted in integer form
    attributes = []

    if input_card < 0:
        attributes.append(f"Invalid {input_card}")

    if (input_card in (63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52)):
        attributes.append("wild")
    if (0 <= input_card <= 9) or (40 <= input_card <= 42) or input_card in (56, 60, 64, 68, 72):
        attributes.append("red")
    elif (10 <= input_card <= 19) or (43 <= input_card <= 45) or input_card in (57, 61, 65, 69, 73):
        attributes.append("yellow")
    elif (20 <= input_card <= 29) or (46 <= input_card <= 48) or input_card in (58, 62, 66, 70, 74):
        attributes.append("green")
    elif (30 <= input_card <= 39) or (49 <= input_card <= 51) or input_card in (59, 63, 67, 71, 75):
        attributes.append("blue")

    if input_card in (40, 43, 46, 49, 64, 65, 66, 67):
        attributes.append("skip")
    if input_card in (64, 65, 66, 67, 68, 72, 69, 73, 70, 74, 71, 75):
        attributes.append("inactive")
    if input_card in (41, 44, 47, 50):
        attributes.append("reverse")

    if input_card in (42, 45, 48, 51):
        attributes.append("+2")
    elif input_card in (54, 55, 60, 61, 62, 63):
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



# modular way to read an entire deck of cards rather than an individual card.
def deck_reader(input_deck):
    output = []
    for card in input_deck:
        card_attributes = card_attribute_assigner(card)
        output.append(card_attributes)
    return output



# Checks to make sure no player has won the game
def win_condition_check(global_player_deck):
    player_tracker = 0

    # reads through each index of the nested global player list
    for player_deck in global_player_deck:

        # if length of the list at index 1 is smalelr than 1, return that player's number
        if len(player_deck) < 1:
            return True, player_tracker

        # if not, increment player tracker to the next player
        else:
            player_tracker += 1
    return False



########################################################################################################################
#                                            Game Logic Section                                                        #
#                                       (the explanations are worse)                                                   #
########################################################################################################################



# Holds all of the logic associated with a player turn
def player_card_turn(input_deck, remaining_deck):

    # initializes a bunch of empty variables that will be used throughout the function.
    cards_drawn = 0
    cards_played = 0
    attribute_card_player = -1
    attribute_card_deck = -1
    selected_card = -1
    removed_card = -1
    valid_card_placed = False
    deck_length = len(remaining_deck)

    # If top card was a +2 or +4, notify player and add to their deck (So long as there is enough cards in the deck)
    if len(remaining_deck) > 4:
        previous_player_2_or_4_check = card_attribute_assigner(remaining_deck[0])
        if "+2" in previous_player_2_or_4_check:
            print(f"\nPrevious player +2 card in effect.\nCards added: {deck_reader(remaining_deck[deck_length - 2:][::-1])}")
            if "red" in previous_player_2_or_4_check:
                remaining_deck[0] = 68
            elif "yellow" in previous_player_2_or_4_check:
                remaining_deck[0] = 69
            elif "green" in previous_player_2_or_4_check:
                remaining_deck[0] = 70
            elif "blue" in previous_player_2_or_4_check:
                remaining_deck[0] = 71
            for _ in range(2):
                input_deck.append(remaining_deck[-1])
                remaining_deck.pop()
        elif "+4" in previous_player_2_or_4_check:
            print(f"\nPrevious player +2 card in effect.\nCards added: {deck_reader(remaining_deck[deck_length - 4:][::-1])}")
            if "red" in previous_player_2_or_4_check:
                remaining_deck[0] = 72
            elif "yellow" in previous_player_2_or_4_check:
                remaining_deck[0] = 73
            elif "green" in previous_player_2_or_4_check:
                remaining_deck[0] = 74
            elif "blue" in previous_player_2_or_4_check:
                remaining_deck[0] = 75
            for _ in range(4):
                input_deck.append(remaining_deck[-1])
                remaining_deck.pop()

    while True:
        try:
            # checks to make sure a skip card has not been played
            previous_player_skip_check = card_attribute_assigner(remaining_deck[0])
            if "skip" in previous_player_skip_check and not "inactive" in previous_player_skip_check:
                print(f"\nPrevious player skip card in effect. Skipping turn . . .")
                if "red" in previous_player_skip_check:
                    remaining_deck[0] = 64
                elif "yellow" in previous_player_skip_check:
                    remaining_deck[0] = 65
                elif "green" in previous_player_skip_check:
                    remaining_deck[0] = 66
                elif "blue" in previous_player_skip_check:
                    remaining_deck[0] = 67
                # inactive skip ID's 64, 65, 66, 67
                # active skip ID's 40, 43, 46, 49
                # color order RYGB
                break

            # prints the card information and action information for the player to make a decision
            print(f"\nCurrent Cards: {deck_reader(input_deck)}")
            print(f"Top Deck Card: {deck_reader([remaining_deck[0]])}")
            player_selection = int(input("0 to play a card | 1 to draw a card | 2 to end turn | "))

            # master if statement that makes sure a input corresponds to a valid action
            if (player_selection < 3 and player_selection > -1):

                # Logic behind if the player input is to select a card
                if player_selection == 0:
                    if cards_played < 1:
                        while True:
                            try:

                                # asks the user which card to select
                                selected_card = int(input(f"Please select a card (1 - {len(input_deck)}) or 0 to cancel | "))
                                selected_card -= 1
                                if selected_card == -1:
                                    print("\ncancelled card placement.")
                                    break

                                # logic behind making sure the player's chosen card can be legally played
                                attribute_card_player = card_attribute_assigner(input_deck[selected_card])
                                attribute_card_deck = card_attribute_assigner(remaining_deck[0])
                                for attribute in attribute_card_deck:
                                    if attribute in attribute_card_player:
                                        valid_card_placed = True
                                if "wild" in attribute_card_player:
                                    valid_card_placed = True

                                # updates the deck and the player hand
                                if valid_card_placed == True:
                                    while True:
                                        try:

                                            # first runs a special updater for if the card is wild
                                            if "wild" in attribute_card_player:
                                                wild_color_choice = int(input("wild card selection | 0 red | 1 yellow | 2 green | 3 blue | "))
                                                if 0 <= wild_color_choice <= 4:
                                                    if wild_color_choice == 0:
                                                        remaining_deck.insert(0, 56)
                                                        removed_card = 56
                                                        input_deck.pop(selected_card)
                                                    elif wild_color_choice == 1:
                                                        remaining_deck.insert(0, 57)
                                                        removed_card = 57
                                                        input_deck.pop(selected_card)
                                                    elif wild_color_choice == 2:
                                                        remaining_deck.insert(0, 58)
                                                        removed_card = 58
                                                        input_deck.pop(selected_card)
                                                    elif wild_color_choice == 3:
                                                        remaining_deck.insert(0, 59)
                                                        removed_card = 59
                                                        input_deck.pop(selected_card)
                                                else:
                                                    print("Invalid input. Please enter a valid number.")
                                            # if the card was not wild, proceed without the normal updater
                                            else:
                                                remaining_deck.insert(0, input_deck[selected_card])
                                                removed_card = input_deck[selected_card]
                                                input_deck.pop(selected_card)
                                            break
                                        except ValueError:
                                            print("Invalid input. Please enter a valid number.")

                                # printing what card was played.
                                if valid_card_placed == True:
                                    cards_played += 1
                                    print(f"\nCard {[card_attribute_assigner(removed_card)]} played!")
                                    break
                                elif valid_card_placed == False:
                                    print("Cannot play this card.")
                                    continue

                            # error handling
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                                continue
                    else:
                        print("Cannot play another card.")
                        continue

                # Logic behind if the player input is to draw a card
                elif player_selection == 1:
                    if len(remaining_deck) > 4:
                        if cards_drawn < 1 and cards_played < 1:
                            cards_drawn += 1
                            input_deck.append(remaining_deck[-1])
                            remaining_deck.pop()
                            print("\nDrew a card!")
                        else:
                            print("\nCannot draw a card. Too many actions")
                            continue
                    else:
                        print("\nCannot draw a card. Not enough cards.")

                # Logic behind if the player input is to end turn
                elif player_selection == 2:
                    if (cards_drawn > 0) or (cards_played > 0):
                        print("\nTurn ending . . . ")
                        break
                    else:
                        print("\nCannot end turn.")
                        continue

        # Error handling for initial action choice
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 2.")

    # packaging outputs at the end of a player turn
    output = [input_deck, remaining_deck]
    return output

def global_player_deck_updater(input_deck, global_player_deck, current_player_num):
    global_player_deck[current_player_num] = input_deck
    return input_deck


# master function for the game logic (Calls most other functions and requires all previous variables)
# is RESPONSIBLE FOR THE TURN LOGIC
def game_loop(global_player_deck, remaining_deck):
    current_player_list = list(range(len(global_player_deck)))
    current_player_num = int(0)
    while True:
        try:
            # print game state
            print(f"\nPlayer {current_player_num + 1} Turn")

            # calls the turn funciton, updates player and game deck.
            output = player_card_turn(global_player_deck[current_player_num], remaining_deck)
            remaining_deck = output[1]
            global_player_deck[current_player_num] = output[0]

            # controls turn flow
            current_player_num += int(1)
            if current_player_num > len(current_player_list):
                current_player_num = int(len(current_player_list) / len(current_player_list)) - 1

            # breaks loop if a player has won
            if win_condition_check(global_player_deck) == False:
                continue
            else:
                player_that_won = win_condition_check(global_player_deck)
                print(f"Player {player_that_won} has won!")
                break
        except IndexError:
            current_player_num = 0
            continue
    return


# Initialization Loop ; Calls necessary game logic and creates global variables
while True:
    try:

        # Gets the initial global player list & card count.
        initialize_output = game_initialize()
        global_card_count = initialize_output[1]
        global_player_deck = initialize_output[0]


        # Calls upon the deck builder to get its output.
        # output[0] will be the original global_player_deck with its indexes replaced by each player's deck list.
        # output[1] will be the remaining cards from the deck player, which will act as the house deck.
        temp_deck_builder_output = deck_builder(global_player_deck, global_card_count)
        global_player_deck = temp_deck_builder_output[0]
        remaining_deck = temp_deck_builder_output[1]

        # sends the seperated outputs to the master game_loop
        game_loop(global_player_deck, remaining_deck)

        # prompts the user to start another game. if value error quit.
        quit = int(input("enter an integer to start another game."))
        continue
    except ValueError:
        print("\nQuitting game . . .")
        break


