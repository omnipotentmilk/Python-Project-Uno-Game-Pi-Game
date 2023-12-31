########################################################################################################################
#                                            Initialization Section                                                    #
########################################################################################################################

import random

# function to prompt for the player/card count when starting a game
def game_initialize():

    # enters a while loop to account for error handling
    while True:
        try:

            # prompts the host for the player and card count
            player_count = int(input("\nWelcome to UnoPy! Please enter the player count (1-infinity): "))
            card_count = int(input("Please enter the number of cards per player (1-infinity): "))

            # verifies that the input is greater than 0 (otherwise game would be impossible to play
            if player_count > 0 and card_count > 0:

                # if it is, create a list that is the length of the player_count long.
                # package this as a list at index 1, and package the player count at index 2
                # return this packaged list to the initialization loop
                global_player_deck = list(range(player_count))
                return [global_player_deck, card_count]

    # handles errors associated with player selection or acts of god
            else:
                print("Invalid input. Please enter a valid number")
                continue
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # this will likely never run, but hey, just incase
    print("ERROR")
    return "ERROR"



# generates a valid uno deck, shuffles it, properly distributes it to the players, packages outputs
# output[0] being a nested list containing the player decks
# output[1] being the remaining cards after distributing
def deck_builder(global_player_deck, global_card_count):

    # initialize variables for later use, it's best to ignore these for now
    players_deck_temp = [] #
    global_player_list_decks = []
    decks_generated = 0

    # Determine the total number of cards required VIA the len output[1] of the initialize function
    # in other words, if a list of 4 players are selected, output[1] is a list 4 indexes long.
    # taking the length of that list essentially gives us the player count.
    total_cards_needed = len(global_player_deck) * global_card_count

    # Calculate the number of decks required. If divisible by 56 (1 uno deck) continue, else add 1 to the number required
    # This helps us to avoid not generating enough decks in the case that the # of decks per player is not a multiple of 56
    if total_cards_needed % 56 == 0:
        decks_required = total_cards_needed // 56
    else:
        decks_required = total_cards_needed // 56 + 1

    # first create an empty list which will act as the "house". This deck is important because
    # it is outputted at the end of the function, as it represents the remaining cards in the stack
    uno_deck_instance = []

    # creates as many deck as calculated to be required, each time updating the deck creation counter.
    # the range (number of cards) of this deck is 56 because there are 56 unique cards per uno deck
    # each deck is shuffled, and then added to the house deck.
    for _ in range(decks_required):
        decks_generated += 1
        new_deck_instance = list(range(56))
        random.shuffle(new_deck_instance)
        uno_deck_instance.extend(new_deck_instance)


    # iterates a number of times equal to the number of players in the game
    for _ in range(len(global_player_deck)):

        # slices the list from the start [0] to desired # of cards [ex 1] exclusive of the last index
        # this means it will slice [0] if the card count was 1, and [0, 1] if the card count was 2
        player_deck = uno_deck_instance[:global_card_count]

        # sets the house deck to itself, starting at the card count (inclusive) to the end
        uno_deck_instance = uno_deck_instance[global_card_count:]

        # appends the cards sliced from the house to a temporary player deck
        #[[the cards will be added as a seperate index per player],[just like this]]
        players_deck_temp.append(player_deck)

    # makes sure that the top card of the remaining deck would not be a wild or +2/+4/skip/reverse card.
    # this is both practical and fun because it allows those cards to appear quicker in gameplay as well as avoid
    # any bugs on the first players turn

    # enters error handling loop
    while True:
        try:
            # These ID's correspond to Wild Cards, Reverse Cards, +2/+4 Cards, and Skip Cards.
            if uno_deck_instance[0] in {55, 54, 53, 52, 42, 45, 48, 51, 40, 43, 46, 49, 41, 44, 47, 50}:
                uno_deck_instance.append(uno_deck_instance[0])
                uno_deck_instance.pop(0) # append the issue card to the back and remove where it used to be

                # if the length of the deck was 1, appending and popping does nothing
                # A new set of decks is required entirely (uses the same method as earlier)
                if len(uno_deck_instance) == 1:

                    # generated a single shuffled valid uno deck depending on the number of decks required
                    uno_deck_instance = []
                    for _ in range(decks_required):
                        decks_generated += 1
                        new_deck_instance = list(range(56))
                        random.shuffle(new_deck_instance)
                        uno_deck_instance.extend(new_deck_instance)

                    # properly slices the main deck to the players, depending on the card count specified
                    for _ in range(len(global_player_deck)):
                        player_deck = uno_deck_instance[:global_card_count]
                        uno_deck_instance = uno_deck_instance[global_card_count:]
                        players_deck_temp.append(player_deck)
                    continue
                else:
                    continue

            # in the case that the top card was not flagged as an issue
            else:
                break
        except IndexError:
            decks_generated += 1
            new_deck_instance = list(range(56))
            random.shuffle(new_deck_instance)
            uno_deck_instance.extend(new_deck_instance)
            continue

    # distribute the temporary new deck segments to the players (index's within global_player_deck)
    for i in global_player_deck:
        global_player_list_decks.append(players_deck_temp[i])

    # packages and returns the nested player deck list and the remaining deck together for output
    print(f"\nUsed [{decks_generated}] deck(s) in generation!\n[{len(uno_deck_instance)}] cards remain in the deck!\nIt took [{decks_generated*56}] card(s) in total to create this game!")
    output = [global_player_list_decks, uno_deck_instance]
    return output



# converts card number |ex: [10]| to attribute format |ex [yellow, 0]|
# IDs were chosen because it made debugging easier. initially used purely string based approach
def card_attribute_assigner(input_card):
    attributes = []

    # in the case that any card was set to -1 as a result of an error
    if input_card < 0:
        attributes.append(f"Invalid {input_card}")

    # assigns initial wild and color attributes
    if (input_card in (63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 76, 77, 78, 79, 72, 73, 74, 75)):
        attributes.append("wild")
    if (0 <= input_card <= 9) or (40 <= input_card <= 42) or input_card in (56, 60, 64, 68, 72, 76, 80):
        attributes.append("red")
    elif (10 <= input_card <= 19) or (43 <= input_card <= 45) or input_card in (57, 61, 65, 69, 73, 77, 81):
        attributes.append("yellow")
    elif (20 <= input_card <= 29) or (46 <= input_card <= 48) or input_card in (58, 62, 66, 70, 74, 78, 82):
        attributes.append("green")
    elif (30 <= input_card <= 39) or (49 <= input_card <= 51) or input_card in (59, 63, 67, 71, 75, 79, 83):
        attributes.append("blue")

    # assigns special attributes
    if input_card in (40, 43, 46, 49, 64, 65, 66, 67):
        attributes.append("skip")
    if input_card in (41, 44, 47, 50, 80, 81, 82, 83):
        attributes.append("reverse")
    if input_card in (42, 45, 48, 51, 68, 69, 70, 71):
        attributes.append("+2")
    elif input_card in (54, 55, 60, 61, 62, 63, 72, 73, 74, 75, 76, 77, 78, 79):
        attributes.append("+4")

    # assigns number attributes
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

    # assigns inactive attributes for a card ID that has been designated as already played
    if input_card in (64, 65, 66, 67, 68, 72, 69, 73, 70, 74, 71, 75, 80, 81, 82, 83):
        attributes.append("inactive")

    return attributes



# easy way to read an entire deck of cards rather than an individual card.
def deck_reader(input_deck):
    output = []

    # per card in the input_deck, run it through the card_attribute_assigner
    for card in input_deck:
        card_attributes = card_attribute_assigner(card)
        output.append(card_attributes)
    return output



# checks to make sure no player has won the game
def win_condition_check(global_player_deck):
    player_tracker = 0

    # reads through each index of the nested global player list
    for player_deck in global_player_deck:

        # if the nested list at index 0 has a length < 1, return that player's number because they are the winner
        if len(player_deck) < 1:
            return [True, player_tracker]

        # if not, increment player tracker to the next player
        else:
            player_tracker += 1

    # return false if the loop did not find a winning player
    return False



########################################################################################################################
#                                            Game Logic Section                                                        #
#                                       (the explanations are worse)                                                   #
########################################################################################################################



# Holds all of the logic associated with a individual player turn
def player_card_turn(input_deck, remaining_deck):

    # initializes a bunch of empty variables that will be used throughout the function.
    cards_drawn = 0
    cards_played = 0
    attribute_card_player = -1
    attribute_card_deck = -1
    selected_card = -1
    removed_card = -1
    valid_card_placed = False
    reverse_card_played = False
    deck_length = len(remaining_deck)

    # if top card was a reverse card, update that card to be inactive (depending on color) with no other logic
    previous_player_reverse_check = card_attribute_assigner(remaining_deck[0])
    if "reverse" in previous_player_reverse_check:
        if "red" in previous_player_reverse_check:
            remaining_deck[0] = 80
        if "yellow" in previous_player_reverse_check:
            remaining_deck[0] = 81
        if "green" in previous_player_reverse_check:
            remaining_deck[0] = 82
        if "blue" in previous_player_reverse_check:
            remaining_deck[0] = 83

    # If top card was a +2 notify player, update card and do appropriate logic
    previous_player_2_or_4_check = card_attribute_assigner(remaining_deck[0])
    if "+2" in previous_player_2_or_4_check and not "inactive" in previous_player_2_or_4_check:
        print(f"\nPrevious player +2 card in effect.\nCards added: {deck_reader(remaining_deck[deck_length - 2:][::-1])}")

        # sets card to an inactive version of it depending on the color
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

    # If top card was a +4 notify player, update card and do appropriate logic
    if "+4" in previous_player_2_or_4_check and not "inactive" in previous_player_2_or_4_check:
        print(f"\nPrevious player +4 card in effect.\nCards added: {deck_reader(remaining_deck[deck_length - 4:][::-1])}")

        # sets card to an inactive version of it depending on the color
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

    # checks to make sure a skip card has not been played, set to inactive and return output.
    previous_player_skip_check = card_attribute_assigner(remaining_deck[0])
    if "skip" in previous_player_skip_check and not "inactive" in previous_player_skip_check:
        print(f"\nPrevious player skip card in effect. Skipping turn . . .")

        # sets card to an inactive version of it depending on the color
        if "red" in previous_player_skip_check:
            remaining_deck[0] = 64
        elif "yellow" in previous_player_skip_check:
            remaining_deck[0] = 65
        elif "green" in previous_player_skip_check:
            remaining_deck[0] = 66
        elif "blue" in previous_player_skip_check:
            remaining_deck[0] = 67

        # packaging outputs at the end of a player turn as a result of a skip
        output = [input_deck, remaining_deck, reverse_card_played]
        return output

    # player action logic begins here
    while True:
        try:

            # prints the card information and action information for the player to make a decision
            print(f"\nCurrent Cards: {deck_reader(input_deck)}")
            print(f"Top Deck Card: {deck_reader([remaining_deck[0]])}")
            player_selection = int(input("0 to play a card | 1 to draw a card | 2 to end turn | "))

            # verifies that the player has made a valid selection
            if (player_selection < 3 and player_selection > -1):

                # action logic if the player wants to place a card
                if player_selection == 0:

                    # continue so long as a card has not already been played
                    if cards_played < 1:
                        while True:
                            try:

                                # asks the user which card to select
                                selected_card = int(input(f"Please select a card (1 - {len(input_deck)}) or 0 to cancel | "))
                                selected_card -= 1
                                if selected_card == -1:
                                    print("\ncancelled card placement.")
                                    break

                                # makes sure chosen card can be legally placed
                                attribute_card_player = card_attribute_assigner(input_deck[selected_card])
                                attribute_card_deck = card_attribute_assigner(remaining_deck[0])
                                for attribute in attribute_card_deck:
                                    if attribute in attribute_card_player:
                                        valid_card_placed = True
                                if "wild" in attribute_card_player:
                                    valid_card_placed = True

                                # if card COULD be legally placed, continue to further logic
                                if valid_card_placed == True:
                                    while True:

                                        try:

                                            # if legal card played was a wild card
                                            if "wild" in attribute_card_player:
                                                wild_color_choice = int(input("wild card selection | 0 red | 1 yellow | 2 green | 3 blue | "))
                                                if 0 <= wild_color_choice <= 4:

                                                    # update the stack and player deck with an active card ID
                                                    # in the case of +4, only do this if there are enough cards
                                                    if wild_color_choice == 0:
                                                        if "+4" in attribute_card_player:
                                                            if deck_length > 4:
                                                                remaining_deck.insert(0, 76)
                                                                removed_card = 76
                                                                input_deck.pop(selected_card)
                                                            else:
                                                                valid_card_placed = False
                                                        else:
                                                            remaining_deck.insert(0, 56)
                                                            removed_card = 56
                                                            input_deck.pop(selected_card)
                                                    elif wild_color_choice == 1:
                                                        if "+4" in attribute_card_player:
                                                            if deck_length > 4:
                                                                remaining_deck.insert(0, 77)
                                                                removed_card = 77
                                                                input_deck.pop(selected_card)
                                                            else:
                                                                valid_card_placed = False
                                                        else:
                                                            remaining_deck.insert(0, 57)
                                                            removed_card = 57
                                                            input_deck.pop(selected_card)
                                                    elif wild_color_choice == 2:
                                                        if "+4" in attribute_card_player:
                                                            if deck_length > 4:
                                                                remaining_deck.insert(0, 78)
                                                                removed_card = 78
                                                                input_deck.pop(selected_card)
                                                            else:
                                                                valid_card_placed = False
                                                        else:
                                                            remaining_deck.insert(0, 58)
                                                            removed_card = 58
                                                            input_deck.pop(selected_card)
                                                    elif wild_color_choice == 3:
                                                        if "+4" in attribute_card_player:
                                                            if deck_length > 4:
                                                                remaining_deck.insert(0, 79)
                                                                removed_card = 79
                                                                input_deck.pop(selected_card)
                                                            else:
                                                                valid_card_placed = False
                                                        else:
                                                            remaining_deck.insert(0, 59)
                                                            removed_card = 59
                                                            input_deck.pop(selected_card)
                                                else:
                                                    print("Invalid input. Please enter a valid number.")

                                            # if legal card played was a +2 card AND there are enough cards remaining
                                            elif "+2" in attribute_card_player:
                                                if deck_length > 2:
                                                    remaining_deck.insert(0, input_deck[selected_card])
                                                    removed_card = input_deck[selected_card]
                                                    input_deck.pop(selected_card)
                                                else:
                                                    valid_card_placed = False

                                            # if legal card played was a reverse card
                                            elif "reverse" in attribute_card_player:
                                                reverse_card_played = True
                                                remaining_deck.insert(0, input_deck[selected_card])
                                                removed_card = input_deck[selected_card]
                                                input_deck.pop(selected_card)

                                            # if legal card played was any other card
                                            else:
                                                remaining_deck.insert(0, input_deck[selected_card])
                                                removed_card = input_deck[selected_card]
                                                input_deck.pop(selected_card)

                                            # exit the legal card placement logic
                                            break

                                        # incase wild card color selection was invalid
                                        except ValueError:
                                            print("Invalid input. Please enter a valid number.")

                                # printing what legal card was played.
                                if valid_card_placed == True:
                                    cards_played += 1
                                    print(f"\nCard {[card_attribute_assigner(removed_card)]} played!")
                                    break
                                elif valid_card_placed == False:
                                    print("Cannot play this card.")
                                    continue

                            # incase the player enters an invalid/non integer when selecting a card to be placed
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                                continue

                    # incase a card has already been played, restart the loop.
                    else:
                        print("Cannot play another card.")
                        continue

                # Logic behind if the player input is to draw a card
                elif player_selection == 1:

                    # makes sure there is at least 1 other card that can be drawn from the deck
                    if len(remaining_deck) > 1:

                        # if no cards have been drawn or placed, continue
                        if cards_drawn < 1 and cards_played < 1:

                            # begins the checking logic to set an inactive card to an active version
                            inactive_draw_card_checker = card_attribute_assigner(remaining_deck[-1])
                            if "inactive" in inactive_draw_card_checker:

                            # changes ID depending on card type to an active version. at this point it no longer
                            # matters if there are duplicate ID's since deck length is valid at creation
                                if "wild" in inactive_draw_card_checker:
                                    if "+4" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 55
                                    else:
                                        remaining_deck[-1] = 53
                                elif "+2" in inactive_draw_card_checker:
                                    if "red" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 42
                                    elif "yellow" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 45
                                    elif "green" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 48
                                    elif "blue" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 51
                                elif "skip" in inactive_draw_card_checker:
                                    if "red" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 40
                                    elif "yellow" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 43
                                    elif "green" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 46
                                    elif "blue" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 49
                                elif "reverse" in inactive_draw_card_checker:
                                    if "red" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 41
                                    elif "yellow" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 44
                                    elif "green" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 47
                                    elif "blue" in inactive_draw_card_checker:
                                        remaining_deck[-1] = 50
                                    pass

                            # after both special and normal cards have been handled, finish card draw logic
                                cards_drawn += 1
                                input_deck.append(remaining_deck[-1])
                                remaining_deck.pop()
                                print("\nDrew a card!")
                            else:
                                cards_drawn += 1
                                input_deck.append(remaining_deck[-1])
                                remaining_deck.pop()
                                print("\nDrew a card!")

                    # handles initial checks that made sure no card had already been drawn or placed
                    # aswell as if the deck is not long enough
                        else:
                            print("\nCannot draw a card. Too many actions")
                            continue
                    else:
                        print("\nCannot draw a card. Not enough cards. Ending game . . .")
                        input_deck = []
                        output = [input_deck, remaining_deck, reverse_card_played]
                        return output

                # Logic behind if the player input is to end turn
                elif player_selection == 2:
                    if (cards_drawn > 0) or (cards_played > 0):
                        print("\nTurn ending . . . ")
                        break
                    else:
                        print("\nCannot end turn.")
                        continue
            else:
                print("Invalid choice. Please enter a valid action")

        # Error handling for initial action choice
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 2.")

    # packaging outputs at the end of a player turn as a result of manually ending turn
    output = [input_deck, remaining_deck, reverse_card_played]
    return output

# holds the logic associated with deciding which players turn it is, and the order in which they are played
def game_loop(global_player_deck, remaining_deck):

    # Initialize variables for the function. Everything starts at 0 because player 1 goes first!
    current_player_num = int(0)
    reverse_counter = 0
    prev_player = 0

    ###################
    # Debugging Tools #
    ###################

    # DEBUG_REVERSE_ADDER = global_player_deck[0]
    # DEBUG_REVERSE_ADDER[0] = 41
    # DEBUG_REVERSE_ADDER[1] = 44
    # DEBUG_REVERSE_ADDER[2] = 47
    # DEBUG_REVERSE_ADDER[3] = 50
    # global_player_deck[0] = DEBUG_REVERSE_ADDER

    ###################
    # Debugging Tools #
    ###################

    # main turn loop
    while True:
        try:
            # print game state
            print(f"\nPlayer {current_player_num + 1} Turn")

            # Call a function that holds logic with player input
            # the first TWO i/o of this function is the player's deck and house deck after their turn
            # the third output is in the special case that a reverse card has been played
            output = player_card_turn(global_player_deck[current_player_num], remaining_deck)
            global_player_deck[current_player_num] = output[0]
            remaining_deck = output[1]

            # check if the current player played a reverse card
            if output[2]:

                # Increment reverse counter, save the PREVIOUS players position
                # Why? So when you play a reverse card you don't go twice
                reverse_counter += 1
                prev_player = current_player_num

            # only continue if a reverse card is active
            if reverse_counter % 2 != 0:

                # Reverse the turn order
                current_player_num = (current_player_num - 1) % len(global_player_deck)

            # else normal turn order
            else:
                current_player_num = (current_player_num + 1) % len(global_player_deck)

            # Breaks loop if a player has won
            if win_condition_check(global_player_deck) == False:
                continue
            else:
                player_that_won = win_condition_check(global_player_deck)
                print(f"\nPlayer {player_that_won[1] + 1} has won!")
                break
        except IndexError:
            current_player_num = 0
            continue

    return



# Initialization Loop ; Calls required game logic/master funcs and creates global variables to be used by those entities
while True:
    try:

        # gets the initial global player list & card count via the game_initialize func
        initialize_output = game_initialize()
        global_card_count = initialize_output[1]
        global_player_deck = initialize_output[0]


        # calls upon the deck builder to get its output
        # output[0] will be a nested list of all player's decks
        # output[1] will be the cards not in the player's decks (AKA the house deck)
        temp_deck_builder_output = deck_builder(global_player_deck, global_card_count)
        global_player_deck = temp_deck_builder_output[0]
        remaining_deck = temp_deck_builder_output[1]

        # pushes those outputs to game. only returns once the game (AKA game loop) has ended.
        game_loop(global_player_deck, remaining_deck)

        # prompts the user to start another game. if value error quit.
        quit = int(input("\nenter an integer to start another game"))
        continue
    except ValueError:
        print("\nQuitting game . . .")
        break
