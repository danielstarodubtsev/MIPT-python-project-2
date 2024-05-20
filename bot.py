import asyncio
import aioschedule

from config import TOKEN
from aiogram import Bot, Dispatcher

import user
import admin

async def main() -> None:
  global bot
  global dp
  bot = Bot(TOKEN)
  dp = Dispatcher()
  dp.startup.register(on_startup)
  dp.include_routers(admin.router, user.router)

  await dp.start_polling(bot)

async def scheduler() -> None:
  print("Bot is ready to start")

  while True:
    await aioschedule.run_pending()
    await asyncio.sleep(1)

async def on_startup() -> None:
  asyncio.create_task(scheduler())