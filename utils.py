from deck import Card
from consts import Values

def count_value(cards: list[Card]) -> int:
  aces_cnt = 0
  result = 0

  for card in cards:
    if card.value == Values.ACE:
      aces_cnt += 1
    else:
      result += min(card.value, 10)

  if aces_cnt == 0:
    return result

  if result + aces_cnt + 10 > 21:
    return result + aces_cnt
  
  return result + aces_cnt + 10

def save_balance(player_balance: int) -> None:
  with open("player_balance.txt", "w") as file:
    file.write(str(player_balance))

def load_balance() -> int:
  try:
    with open("player_balance.txt", "r") as file:
      return int(file.read())
  except FileNotFoundError:
    with open("player_balance.txt", "w") as file:
      file.write("1000")

    return 1000