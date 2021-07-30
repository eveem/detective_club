import os

from dotenv import load_dotenv

load_dotenv()

import asyncio
import random

from discord import User
from discord.ext.commands import Bot, Greedy

bot = Bot(command_prefix="!")


@bot.command()
async def dm(ctx, users: Greedy[User], *, message):
    for user in users:
        await user.send(message)


bot.run(os.getenv("TOKEN"))
