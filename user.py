from aiogram import  Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio

from game import Game
from utils import count_value, load_balance, save_balance

router = Router()
dp = Dispatcher()

game = None
player_balance = load_balance()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await message.answer(f"Bot is running and ready to work")

@router.message(Command('help'))
async def command_help_handler(message: types.Message) -> None:
  await message.answer("""
This bot can be used to play blackjack
Commands:
/start - start using the bot
/help - view this info
/game stake - starts a game with the given stake
/balance - shows how much money you have
/addmoney - adds 1000 money to your balance (only available if you have no money left)
                       """)

@router.message(Command(commands=["game"]))
async def start_game(message: types.Message) -> None:
  global game

  if game:
    await message.answer("Action failed! There is already a game in progress")
    return

  try:
    stake = int(message.text.split()[1])
  except IndexError:
    await message.answer('Action failed! Missing required argument "stake"')
    return

  if stake > player_balance:
    await message.answer("Your stake must be no higher than your balance!")
    return
  if stake <= 0:
    await message.answer("Your stake must be a positive integer!")
    return

  game = Game(stake)

  await message.answer("Game started successfully!")
  await message.answer(str(game))
  
  if not game.player_finished:
    await message.answer("Do you want to draw another card?")

@router.message(Command(commands=["balance"]))
async def show_balance(message: types.Message) -> None:
  global player_balance
  await message.answer(f"Your balance is {player_balance}")

@router.message(Command(commands=["addmoney"]))
async def add_money(message: types.Message) -> None:
  global player_balance

  if player_balance > 0:
    await message.answer("You can only use this command if your balance is zero")
  else:
    await message.answer("Success! Your balance is now 1000")
    player_balance = 1000

@router.message()
async def echo_handler(message: types.Message) -> None:
  global game
  global player_balance

  if game and not game.player_finished:
    if message.text.lower() == "yes":
      game.player_take_card()
      await message.answer(str(game))

      if count_value(game.player_cards) > 21:
        player_balance -= game.stake
        game = None
        save_balance(player_balance)
        await message.answer("Oh no! You lost the game")
        await message.answer(f"You lost your money and your balance is now {player_balance}")
      else:
        await message.answer("Do you want to take another card?")
    else:
      game.player_finished = True

      while True:
        await message.answer(str(game))

        if count_value(game.dealer_cards) < count_value(game.player_cards):
          await asyncio.sleep(2)
          await message.answer("Dealer wants to take another card")
          game.dealer_take_card()
        else:
          break
      
      await asyncio.sleep(2)

      if count_value(game.dealer_cards) == count_value(game.player_cards):
        await message.answer("You are tied with the dealer, you get your stake back")
      elif count_value(game.dealer_cards) <= 21:
        player_balance -= game.stake
        save_balance(player_balance)
        await message.answer("Oh no! You lost the game")
        await message.answer(f"You lost your money and your balance is now {player_balance}")
      else:
        player_balance += game.stake
        save_balance(player_balance)
        await message.answer("Congratulations, you won!")
        await message.answer(f"You doubled your stake and you balance is now {player_balance}")

      game = None