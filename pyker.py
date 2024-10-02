import sys
import random
from enum import Enum

class Rank(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

    def __str__(self):
        return self.name.capitalize()

# Card Class: represents a single card
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{Rank(self.rank)} of {self.suit}"

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __ne__(self, other):
        return self.rank != other.rank



# Deck Class: represents a deck of 52 cards
class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self):
        self.cards = [Card(rank.value, suit) for rank in Rank for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, num=1):
        drawn_cards = []
        for _ in range(num):
            if self.cards:
                drawn_cards.append(self.cards.pop())
        return drawn_cards

# Player Class: represents a player with 5 cards and a money balance
class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.hand_value = 0
        self.mattering_cards = []
        self.rest_cards = []

    def draw_cards(self, deck, num=5):
        self.hand = deck.draw(num)

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

def play_game(number_of_players, money_entrance, cost_per_hand):
    # Initialize deck and players

    players = [Player(f"Player {i+1}", money_entrance) for i in range(number_of_players)]

    while all(player.balance >= cost_per_hand for player in players):
        deck = Deck()
        deck.shuffle()
        # Players pay the cost per hand
        for player in players:
            player.balance -= cost_per_hand
        # Draw cards for each player
        for player in players:
            player.draw_cards(deck)
        # Evaluate each player's hand
        for player in players:
            evaluate_hand(player)
            print(f"{player.name} has: {player.hand_value} ({player.show_hand()})")

        # Find the winner(s) of the hand
        max_hand_value = max(player.hand_value for player in players)
        winners = [player for player in players if player.hand_value == max_hand_value]
        if len(winners) == 1:
            winner = winners[0]
            winner.balance += sum(player.balance for player in players)
            print(f"{winner.name} wins the hand!")
            print(f"Balances: {[f'{player.name}: {player.balance}' for player in players]}")
        else:
            # If there is a tie, compare the mattering cards
            for winner in winners:
                print(f"{winner.name} ties with: {', '.join(str(card) for card in winner.concerned_cards)}")
            # Find the winner(s) based on the mattering cards
            max_mattering_card = max(max(player.concerned_cards, key=lambda card: card.rank) for player in winners)
            winners = [player for player in winners if max(player.concerned_cards, key=lambda card: card.rank) == max_mattering_card]
            if len(winners) == 1:
                winner = winners[0]
                winner.balance += sum(player.balance for player in players)
                print(f"{winner.name} wins the hand!")
                print(f"Balances: {[f'{player.name}: {player.balance}' for player in players]}")
            else:
                max_rest_card = max(max(player.rest_cards, key=lambda card: card.rank) for player in winners)
                winner = [player for player in winners if max(player.rest_cards, key=lambda card: card.rank) == max_rest_card][0]
                winner.balance += sum(player.balance for player in players)
                print(f"{winner.name} wins the hand!")
                print(f"Balances: {[f'{player.name}: {player.balance}' for player in players]}")

    print("Game Over!")

def compare_cards(card1, card2):
    return card1.rank - card2.rank
def contains_straight_flush(hand):
    suits = {card.suit for card in hand}
    if len(suits) == 1:
        sorted_hand = sorted(hand, key=lambda card: card.rank)
        rank_indices = [card.rank for card in sorted_hand]
        if rank_indices == list(range(min(rank_indices), max(rank_indices) + 1)):
            return sorted_hand
    return False

def contains_four_of_a_kind(hand):
    ranks = [card.rank for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 4:
            return sorted([card for card in hand if card.rank == rank], key=lambda card: card.rank)
    return False

def contains_full_house(hand):
    ranks = [card.rank for card in hand]
    unique_ranks = set(ranks)
    if len(unique_ranks) == 2:
        for rank in unique_ranks:
            if ranks.count(rank) == 3:
                return sorted(hand, key=lambda card: card.rank)
    return False

def contains_flush(hand):
    suits = {card.suit for card in hand}
    if len(suits) == 1:
        return sorted(hand, key=lambda card: card.rank)
    return False

def contains_straight(hand):
    sorted_hand = sorted(hand, key=lambda card: card.rank)
    rank_indices = [card.rank for card in sorted_hand]
    if rank_indices == list(range(min(rank_indices), max(rank_indices) + 1)):
        return sorted_hand
    return False

def contains_three_of_a_kind(hand):
    ranks = [card.rank for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 3:
            return sorted([card for card in hand if card.rank == rank], key=lambda card: card.rank)
    return False

def contains_two_pair(hand):
    ranks = [card.rank for card in hand]
    unique_ranks = set(ranks)
    pairs = []
    for rank in unique_ranks:
        if ranks.count(rank) == 2:
            pairs.extend([card for card in hand if card.rank == rank])
    return sorted(pairs, key=lambda card: card.rank) if len(pairs) == 4 else False

def contains_one_pair(hand):
    ranks = [card.rank for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 2:
            return sorted([card for card in hand if card.rank == rank], key=lambda card: card.rank)
    return False

def evaluate_hand(player):
    hand = player.hand
    if (concerned_cards := contains_straight_flush(hand)):
        player.hand_value = 8
    elif (concerned_cards := contains_four_of_a_kind(hand)):
        player.hand_value = 7
    elif (concerned_cards := contains_full_house(hand)):
        player.hand_value = 6
    elif (concerned_cards := contains_flush(hand)):
        player.hand_value = 5
    elif (concerned_cards := contains_straight(hand)):
        player.hand_value = 4
    elif (concerned_cards := contains_three_of_a_kind(hand)):
        player.hand_value = 3
    elif (concerned_cards := contains_two_pair(hand)):
        player.hand_value = 2
    elif (concerned_cards := contains_one_pair(hand)):
        player.hand_value = 1
    else:
        player.hand_value = 0
        concerned_cards = []

    player.concerned_cards = concerned_cards
    player.rest_cards = [card for card in hand if card not in concerned_cards]

if __name__ == "__main__":
    # Expecting arguments in the format: python pyker.py number_of_players money_entrance cost_per_hand
    if len(sys.argv) != 4:
        print("Usage: python pyker.py number_of_players money_entrance cost_per_hand")
        sys.exit(1)

    number_of_players = int(sys.argv[1])
    money_entrance = int(sys.argv[2])
    cost_per_hand = int(sys.argv[3])

    play_game(number_of_players, money_entrance, cost_per_hand)