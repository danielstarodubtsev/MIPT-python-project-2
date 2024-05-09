from deck import Deck

from utils import count_value

class Game:
  def __init__(self, stake: int) -> None:
    self.player_cards = []
    self.dealer_cards = []
    self.deck = Deck()

    self.player_take_card()
    self.player_take_card()
    self.dealer_take_card()
    self.dealer_take_card()

    self.stake = stake
    self.player_finished = False

  def dealer_take_card(self) -> None:
    self.dealer_cards.append(self.deck.take_card())

  def player_take_card(self) -> None:
    self.player_cards.append(self.deck.take_card())

  def __str__(self) -> str:
    if self.player_finished:
      return f"""
Dealer cards: {" ".join(list(map(str, self.dealer_cards)))}
Dealer value: {count_value(self.dealer_cards)}

Your cards: {" ".join(list(map(str, self.player_cards)))}
Your value: {count_value(self.player_cards)}
"""
    else:
      return f"""
Dealer cards: {self.dealer_cards[0]} ??
Dealer value: ???

Your cards: {" ".join(list(map(str, self.player_cards)))}
Your value: {count_value(self.player_cards)}
"""