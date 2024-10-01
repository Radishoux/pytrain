import sys
import random

# Card Class: represents a single card
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck Class: represents a deck of 52 cards
class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

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

    def draw_cards(self, deck, num=5):
        self.hand = deck.draw(num)

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)


def play_game(number_of_players, money_entrance, cost_per_hand):
    # Initialize deck and players
    players = [Player(f"Player {i+1}", money_entrance) for i in range(number_of_players)]

    while len(players) > 1:
      deck = Deck()
      deck.shuffle()


      # Deal 5 cards to each player
      for player in players:
          player.draw_cards(deck)

      # Display player hands and deduct cost per hand
      for player in players:
          player.balance -= cost_per_hand
          print(f"{player.name}'s hand: {player.show_hand()} | Balance: ${player.balance}")

      # do dictionnary of players and their hands
      players_hands = {player: evaluate_hand(player) for player in players}
      # get the winner(s)
      winners = [player for player, hand_value in players_hands.items() if hand_value == max(players_hands.values())]
      # add the pot to the winner(s)
      for winner in winners:
          winner.balance += (len(players) * cost_per_hand) // len(winners)

      # Display the winner(s) and their hand
      for winner in winners:
          print(f"Winner: {winner.name} | Hand: {player_hand_value_to_string(winner.hand)}")
          print(f"{winner.name}'s hand: {winner.show_hand()} | Balance: ${winner.balance}")
          print("--------------------")

      # remove the players with no money
      players = [player for player in players if player.balance >= cost_per_hand]

    print("Game Over!")

def player_hand_value_to_string(hand):
    if contains_straight_flush(hand):
        return "Straight Flush"
    elif contains_four_of_a_kind(hand):
        return "Four of a Kind"
    elif contains_full_house(hand):
        return "Full House"
    elif contains_flush(hand):
        return "Flush"
    elif contains_straight(hand):
        return "Straight"
    elif contains_three_of_a_kind(hand):
        return "Three of a Kind"
    elif contains_two_pair(hand):
        return "Two Pair"
    elif contains_one_pair(hand):
        return "One Pair"
    else:
        return "High Card"

def contains_straight_flush(hand):
    suits = {card.suit for card in hand}
    if len(suits) == 1:
        ranks = sorted(Deck.ranks.index(card.rank) for card in hand)
        return ranks == list(range(min(ranks), max(ranks) + 1))
    return False

def contains_four_of_a_kind(hand):
    ranks = [card.rank for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 4:
            return True
    return False

def contains_full_house(hand):
    ranks = [card.rank for card in hand]
    unique_ranks = set(ranks)
    if len(unique_ranks) == 2:
        for rank in unique_ranks:
            if ranks.count(rank) == 3:
                return True
    return False

def contains_flush(hand):
    suits = {card.suit for card in hand}
    return len(suits) == 1

def contains_straight(hand):
    ranks = sorted(Deck.ranks.index(card.rank) for card in hand)
    return ranks == list(range(min(ranks), max(ranks) + 1))

def contains_three_of_a_kind(hand):
    ranks = [card.rank for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 3:
            return True
    return False

def contains_two_pair(hand):
    ranks = [card.rank for card in hand]
    unique_ranks = set(ranks)
    pairs = 0
    for rank in unique_ranks:
        if ranks.count(rank) == 2:
            pairs += 1
    return pairs == 2

def contains_one_pair(hand):
    ranks = [card.rank for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 2:
            return True
    return False

def evaluate_hand(player):
    hand = player.hand
    if contains_straight_flush(hand):
        return 8
    elif contains_four_of_a_kind(hand):
        return 7
    elif contains_full_house(hand):
        return 6
    elif contains_flush(hand):
        return 5
    elif contains_straight(hand):
        return 4
    elif contains_three_of_a_kind(hand):
        return 3
    elif contains_two_pair(hand):
        return 2
    elif contains_one_pair(hand):
        return 1
    else:
        return 0


if __name__ == "__main__":
    # Expecting arguments in the format: python pyker.py number_of_players money_entrance cost_per_hand
    if len(sys.argv) != 4:
        print("Usage: python pyker.py number_of_players money_entrance cost_per_hand")
        sys.exit(1)

    number_of_players = int(sys.argv[1])
    money_entrance = int(sys.argv[2])
    cost_per_hand = int(sys.argv[3])

    play_game(number_of_players, money_entrance, cost_per_hand)