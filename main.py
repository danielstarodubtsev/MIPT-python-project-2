import asyncio
import nest_asyncio
from bot import main

nest_asyncio.apply()

if __name__ == "__main__":
  asyncio.run(main())