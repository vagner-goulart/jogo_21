import random
import math
from time import sleep

user_cards = []
user_cards_splitted = []
dealer_cards = []

dealer_final_sum = 0
user_final_sum = 0
user_splitted_final_sum = 0

ONE_CARD_DECK = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4
DECK_TO_PLAY = ONE_CARD_DECK * 6
random.shuffle(DECK_TO_PLAY)
DECK_TO_PLAY.pop(0)

final_result = ""

user_tokens = 50
user_bet = 0
obtained_tokens = 0
boll_splitted_pair = False
run_once = True


def print_cards(cards_to_print):
    if cards_to_print == user_cards or cards_to_print == user_cards_splitted:
        print("Your cards: ", end="")
    elif cards_to_print == dealer_cards:
        print("Dealer cards: ", end="")

    for card_index, card in enumerate(cards_to_print, start=1):

        if card_index == len(cards_to_print):
            print(card, end="  - ")
        else:
            print(card, "|", end=" ")

    if cards_to_print == user_cards:
        print(user_final_sum)

    elif cards_to_print == dealer_cards:
        print(dealer_final_sum)

    elif cards_to_print == user_cards_splitted:
        print(user_splitted_final_sum)


def bet_tokens():
    while True:

        print(f"You have {user_tokens} tokens")
        input_bet_tokens = input("How much do you want to bet? : ")

        if input_bet_tokens.isdigit():

            if int(input_bet_tokens) > user_tokens:
                print(f"\nYou do not have {int(input_bet_tokens)} tokens to bet!\n")

            elif int(input_bet_tokens) <= 0:
                print("\nEnter a valid number!\n")

            elif int(input_bet_tokens) == 1:
                print("\nThe minimum bet is 2 tokens.\n")

            else:
                return int(input_bet_tokens)

        else:
            print("\nEnter only numbers!\n")


def cards_sum_logic(cards_to_sum):

    final_sum = 0

    for card in cards_to_sum:

        if card == "J" or card == "Q" or card == "K":
            final_sum += 10

        if isinstance(card, int):
            final_sum += card

    for card in cards_to_sum:
        if card == "A":

            if 1 + final_sum > 21:
                final_sum += 1
            else:
                if 11 + final_sum <= 21:
                    final_sum += 11
                elif 1 + final_sum <= 21:
                    final_sum += 1

    return final_sum


def split_pair():
    print("\nHand 2:\n")

    global user_splitted_final_sum

    while True:

        if boll_splitted_pair and len(user_cards) == user_cards.count("A"):

            print_cards(user_cards_splitted)
            user_cards_splitted.append(DECK_TO_PLAY.pop(0))
            user_splitted_final_sum = cards_sum_logic(user_cards_splitted)
            print_cards(user_cards_splitted)
            print()
            break

        user_splitted_final_sum = cards_sum_logic(user_cards_splitted)

        print_cards(user_cards_splitted)
        print()

        if user_splitted_final_sum >= 21:
            print(f"Hand sum: {user_splitted_final_sum}")
            break

        while True:

            input_user_splitted = input("\n(1)-Hit me (2)-Stand : ")

            if input_user_splitted == "1" or input_user_splitted == "2":
                break

            else:
                print("\nEnter one of the values below!")

        print()

        if input_user_splitted == "1":
            user_cards_splitted.append(DECK_TO_PLAY.pop(0))

        elif input_user_splitted == "2":
            print_cards(user_cards_splitted)
            print()
            break


def double_down():

    if user_bet * 2 > user_tokens:
        print(f"You do not have more {user_bet} tokens to double down!\n")
        return user_bet, False
    else:
        user_cards.append(DECK_TO_PLAY.pop(0))
        print()
        return user_bet * 2, True


def define_result_message(user_final_sum):
    if user_final_sum < 21 and dealer_final_sum < 21:
        print(f"\nUser result: {user_final_sum}")
        print(f"Dealer result: {dealer_final_sum}\n")

    elif user_final_sum > 21 or dealer_final_sum > 21:
        dealer_or_user = "You" if user_final_sum > 21 else "Dealer"
        print(dealer_or_user, "went over 21")

    if user_final_sum > 21:
        return "Dealer wins"

    elif dealer_final_sum > 21:
        return "User wins"

    else:
        if dealer_final_sum > user_final_sum or user_final_sum > 21:
            return "Dealer wins"

        elif dealer_final_sum < user_final_sum or dealer_final_sum > 21:
            return "User wins"

        elif dealer_final_sum == user_final_sum:
            return "Draw"


def calc_obtained_tokens(user_bet_param):
    store_tokens = 0

    if "Dealer" in final_result:
        return 0 - user_bet_param

    elif "User" in final_result:
        store_tokens += user_bet_param

        if len(user_cards) == 2 and user_final_sum == 21 and not boll_splitted_pair:
            print("\nBLACKJACK!\n")
            store_tokens += math.floor(user_bet_param * 1.5)

        return store_tokens

    elif "Draw" in final_result:
        return 0


print("This is a Blackjack game!\n")
print("You received 50 tokens")
print("-" * 30)
print()

while True:

    for i in range(2):
        dealer_cards.append(DECK_TO_PLAY.pop(0))

        user_cards.append(DECK_TO_PLAY.pop(0))

    user_bet = bet_tokens()

    print(f"\n\nDealer cards: {dealer_cards[0]} | #\n")

    dealer_have_Q_J_or_K = any(char in dealer_cards for char in ["Q", "j", "K"])

    dealer_tem_21 = "A" in dealer_cards and dealer_have_Q_J_or_K

    while not dealer_tem_21:

        if boll_splitted_pair and len(user_cards) == user_cards.count("A"):
            print_cards(user_cards)
            user_cards.append(DECK_TO_PLAY.pop(0))
            user_final_sum = cards_sum_logic(user_cards)
            print_cards(user_cards)
            print()
            break

        user_final_sum = cards_sum_logic(user_cards)

        print_cards(user_cards)
        print()

        if user_final_sum >= 21:
            print(f"Hand sum: {user_final_sum}")
            break

        standart_inputs = ["1", "2", "3", "4"] if len(set(user_cards)) == 1 else ["1", "2","3"]
        allowed_inputs = standart_inputs if not boll_splitted_pair else ["1", "2"]
        user_input_msg = "\n(1)-Hit me (2)-Stand (3)-Double down : "

        if run_once and len(set(user_cards)) == 1:
            user_input_msg = "\n(1)-Hit me (2)-Stand (3)-Double down (4)-Split pair : "

        elif boll_splitted_pair:
            user_input_msg = "\n(1)-Hit me (2)-Stand : "

        while True:

            user_input = input(user_input_msg)

            if user_input in allowed_inputs:

                run_once = False
                break

            else:
                print("\nEnter one of the values below!")

        print()

        if user_input == "1":
            user_cards.append(DECK_TO_PLAY.pop(0))

        elif user_input == "2":
            print_cards(user_cards)
            print()
            break

        elif user_input == "3":
            user_bet, x = double_down()
            if x:
                user_final_sum = cards_sum_logic(user_cards)
                print_cards(user_cards)
                break

        elif user_input == "4":

            if user_bet * 2 > user_tokens:
                print(f"You do not have {user_bet} tokens left to split a pair!\n")
            else:
                boll_splitted_pair = True
                user_cards_splitted.append(user_cards.pop(0))
                print("Hand 1:\n")

    if len(user_cards_splitted) == 1:
        split_pair()

    if user_final_sum <= 21 or boll_splitted_pair and user_splitted_final_sum <= 21:

        print("\nDealer playing:\n")

        while True:

            dealer_final_sum = cards_sum_logic(dealer_cards)

            print_cards(dealer_cards)
            sleep(1.5)

            if dealer_final_sum >= 21:
                print(f"\nHand sum: {dealer_final_sum}")
                break

            more_than_user_and_17 = 17 <= dealer_final_sum >= user_final_sum
            more_than_user_and_17_splitted = 17 <= dealer_final_sum >= user_splitted_final_sum

            if boll_splitted_pair:

                if user_final_sum > 21 and more_than_user_and_17_splitted:
                    break

                elif user_splitted_final_sum > 21 and more_than_user_and_17:
                    break

                elif more_than_user_and_17 and more_than_user_and_17_splitted:
                    break

            elif more_than_user_and_17:
                break

            if dealer_final_sum < 17:
                dealer_cards.append(DECK_TO_PLAY.pop(0))

            elif boll_splitted_pair:
                if 21 >= user_final_sum > dealer_final_sum:
                    dealer_cards.append(DECK_TO_PLAY.pop(0))

                elif 21 >= user_splitted_final_sum > dealer_final_sum:
                    dealer_cards.append(DECK_TO_PLAY.pop(0))

            elif dealer_final_sum < user_final_sum:
                dealer_cards.append(DECK_TO_PLAY.pop(0))

    print("\n\nResult(s):")

    # TODO: this is ugly, find another way to do it
    if len(user_cards_splitted) >= 1:

        print("\nHand 1:")
        final_result = define_result_message(user_final_sum)

        obtained_tokens = calc_obtained_tokens(user_bet)

        user_tokens += obtained_tokens

        print(f"{final_result}  | {'+' if obtained_tokens > 0 else ''}{obtained_tokens} token(s)")
        print("¨" * 30)

        print("\nHand 2:")
        final_result = define_result_message(user_splitted_final_sum)

        obtained_tokens = calc_obtained_tokens(user_bet)

        user_tokens += obtained_tokens

        print(f"{final_result}  | {'+' if obtained_tokens > 0 else ''}{obtained_tokens} token(s)")

    else:
        final_result = define_result_message(user_final_sum)

        obtained_tokens = calc_obtained_tokens(user_bet)

        user_tokens += obtained_tokens

        print(f"{final_result}  | {'+' if obtained_tokens > 0 else ''}{obtained_tokens} token(s)")

    print("¨" * 30)
    print()

    if user_tokens <= 0:
        print("You ran out of tokens, Game Over.")
        input("Press ENTER to close")
        break

    if len(DECK_TO_PLAY) < 78:
        DECK_TO_PLAY = ONE_CARD_DECK * 6
        random.shuffle(DECK_TO_PLAY)
        DECK_TO_PLAY.pop(0)

    final_result = ""
    user_cards_splitted, user_cards, dealer_cards = [], [], []
    dealer_final_sum, user_final_sum = 0, 0
    user_bet, obtained_tokens = 0, 0
    run_once = True
    boll_splitted_pair = False
