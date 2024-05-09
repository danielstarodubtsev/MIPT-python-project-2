import random

from consts import Suits

class Card:
  def __init__(self, value: int, suit: int) -> None:
    self.value = value
    self.suit = suit

  def __str__(self) -> str:
    suit_str = {
      Suits.SPADES: "♠",
      Suits.CLUBS: "♣",
      Suits.DIAMONDS: "♦",
      Suits.HEARTS: "♥",
    }[self.suit]

    if self.value < 10:
      return str(self.value) + suit_str
    
    return {
      10: "T",
      11: "J",
      12: "Q",
      13: "K",
      14: "A",
    }[self.value] + suit_str

class Deck:
  def __init__(self) -> None:
    self.deck = [Card(value, suit) for 
                 value in range(2, 15) for 
                 suit in (Suits.CLUBS, Suits.DIAMONDS, Suits.HEARTS, Suits.SPADES)]
    self.shuffle()

  def shuffle(self) -> None:
    random.shuffle(self.deck)

  def size(self) -> int:
    return len(self.deck)
  
  def empty(self) -> bool:
    return not self.deck
  
  def take_card(self) -> Card:
    return self.deck.pop()