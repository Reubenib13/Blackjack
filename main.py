import random

CARDS = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def get_int(s, min_=None, max_=None):
    while True:
        try:
            res = int(input(s))
            if not (min_ is None or max_ is None):
                if res < min_ or res > max_:
                    print(f"Enter a number between {min_} and {max_}")
                else:
                    return res
            else:
                return res
        except ValueError:
            print("Enter a number")

def get_str(s, accepted):
    while True:
        res = input(s).upper()
        if res in accepted:
            return res

def random_card():
    return random.choice(CARDS)

def sum_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0, cards
    elif sum(cards) > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)

    if sum(cards) == 21 and len(cards) == 2:
        return 0, cards
    else:
        return sum(cards), cards

def split_game(user_cards, hand, bet, balance):
    print(f"Hand = {hand}, cards = {user_cards}")
    
    dealt = False
    while not dealt:
        if sum(user_cards) < 21:
            answer = get_str("Do you want to Hit(H), Stand(S) or Double(D): ", ("H", "S", "D"))
            if answer == 'H':
                user_cards.append(random_card())

            elif answer == "D":
                user_cards.append(random_card())
                if balance - (2 * bet) < 0:
                    bet += (balance - bet)
                else:
                    balance -= bet
                    bet *= 2
                dealt = True

            elif answer == "S":
                dealt = True

        else:
            dealt = True
    return (user_cards, hand, bet, balance)

def cheack_hands(user_score, user_cards, dealer_cards, dealer_score, balance, bet):
    if user_score > 21:
        balance -= bet
        print(f"You bust. You lose, your balance is {balance}")
    elif user_score == dealer_score:
        balance -= bet
        print(f"Equal hands. You lose, your balance is {balance}")
    elif dealer_score == 0:
        balance -= bet
        print(f"Lose, Dealer has Blackjack, balance is {balance}")
    elif user_score == 0:
        balance += bet * 1.5
        print(f"Win with a Blackjack, balance is {balance}")
    elif dealer_score > 21:
        x = sum(dealer_cards[:len(dealer_cards) - 1])
        if x > user_score:
            balance -= bet
            print(f"You Lose, your balance is {balance}")
        else:
            balance += bet
            print(f"Dealer bust. You win, balance is {balance}")
    elif user_score > dealer_score:
        balance += bet
        print(f"You win, balance is {balance}")
    else:
        balance -= bet
        print(f"You lose, balance is {balance}")
    return balance

balance = 1000
again = True

while balance > 0 and again:
    user_cards = [random_card(), random_card()]
    dealer_cards = [random_card(), random_card()]

    bet = get_int(f"\nChoose bet (Under {balance}): ", 1, balance)

    split = False
    dealt = False
    while not dealt:
        print(f"\nDealer has: {dealer_cards[0]}")
        score_user, user_cards = sum_score(user_cards)
        score_dealer, dealer_cards = sum_score(dealer_cards)
        print(f"Your cards: {user_cards} your current score: {sum(user_cards)}")

        split_option = user_cards[0] == user_cards[1] and balance - (2 * bet) >= 0 and len(user_cards) == 2

        if sum(user_cards) < 21:
            if split_option:
                answer = get_str("Do you want to Hit(H), Stand(S), Double(D) or Split(SP): ", ("H", "S", "D", "SP"))
            else:
                answer = get_str("Do you want to Hit(H), Stand(S) or Double(D): ", ("H", "S", "D"))

            if answer == 'H':
                user_cards.append(random_card())

            elif answer == "D":
                user_cards.append(random_card())
                if balance - (2 * bet) < 0:
                    bet += (balance - bet)
                else:
                    balance -= bet
                dealt = True

            elif answer == "S":
                dealt = True

            elif answer == "SP" and split_option:
                split = True
                user_cards1, hand, bet, balance = split_game(user_cards[0], 1, bet, balance)
                user_cards2, hand, bet, balance = split_game(user_cards[1], 2, bet, balance)

        else:
            dealt = True

    while score_dealer != 0 and score_dealer < 17:
        dealer_cards.append(random_card())
        score_dealer, dealer_cards = sum_score(dealer_cards)

    if split:
        user_score1, user_cards1 = sum_score(user_cards1)
        user_score2, user_cards2 = sum_score(user_cards2)
        dealer_score, dealer_cards = sum_score(dealer_cards)
        print(f"\nYour final hands: \n1: {user_cards1}, final score: {sum(user_cards1)}\n2: {user_cards2}, final score: {sum(user_cards2)}")
        print(f"Computer's final hand: {dealer_cards}, final score: {sum(dealer_cards)}")
        
        print("\nHAND 1:")
        balance = cheack_hands(user_score1, user_cards1, dealer_cards, dealer_score, balance, bet)

        print("\nHAND 2:")
        balance = cheack_hands(user_score2, user_cards2, dealer_cards, dealer_score, balance, bet)
    
    else:
        user_score, user_cards = sum_score(user_cards)
        dealer_score, dealer_cards = sum_score(dealer_cards)
        print(f"\nYour final hand: {user_cards}, final score: {sum(user_cards)}")
        print(f"Computer's final hand: {dealer_cards}, final score: {sum(dealer_cards)}")
        
        balance = cheack_hands(user_score, user_cards, dealer_cards, dealer_score, balance, bet)
    input("\nHit Enter to continue: ")
    

if balance <= 0:
    print("You are out of money. Game over")
else:
    a = input("Do you want to play another round? Y/N: ").upper()
    if a == 'Y':
        again == True
