import os

from dotenv import load_dotenv

load_dotenv()

import asyncio
import random

from discord import User
from discord.ext.commands import Bot, Greedy

bot = Bot(command_prefix="!")
EMOJIS = open("emojis.txt", "r").read().split("\n")
TOTAL_EMOJI = len(EMOJIS)


def get_cards(n=8):
    temp = []
    for i in range(1, n + 1):
        temp.append(f"{i}. {EMOJIS[random.randint(0, TOTAL_EMOJI - 1)]}")

    return "\n\n".join(temp)


@bot.command()
async def dm(ctx, users: Greedy[User]):
    for user in users:
        cards = get_cards()
        await user.send(f"Your cards are\n\n{cards}")


bot.run(os.getenv("TOKEN"))
