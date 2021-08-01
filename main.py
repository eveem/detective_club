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

DATA = {
    "โรงพยาบาล": [
        "พยาบาล",
        "หมอ",
        "คนไข้",
        "ภารโรง",
        "ผู้อำนวยการ",
        "จิตแพทย์",
        "หมอฟัน",
        "พนักงานเปล",
    ],
    "โรงเรียน": [
        "ครู",
        "นักเรียน",
        "แม่บ้าน",
        "ภารโรง",
        "ผู้อำนวยการ",
        "ครูใหญ่",
        "หมา",
        "แม่ครัว",
    ],
}

bot.spy_id = 0
bot.players = []
bot.vote_score = {}
bot.scores = {}
bot.voted = 0
bot.player_mapper = {}
bot.voter = {}


def clear_value():
    bot.spy_id = 0
    bot.players = []
    bot.vote_score = {}
    bot.scores = {}
    bot.voted = 0
    bot.player_mapper = {}
    bot.voter = {}


def get_cards(n=8):
    temp = []
    for i in range(1, n + 1):
        temp.append(f"{i}. {EMOJIS[random.randint(0, TOTAL_EMOJI - 1)]}")

    return "\n\n".join(temp)


@bot.command()
async def hi(ctx):
    await ctx.send("สวัสดีพวกเด็กๆ")


@bot.command()
async def spyfall(ctx, users: Greedy[User]):
    clear_value()
    total_mention = len(users)
    bot.players = [str(user.id) for user in users]
    bot.spy_id = bot.players[random.randint(0, total_mention - 1)]
    place = random.choice(list(DATA.keys()))

    for i, user in enumerate(users):
        bot.player_mapper[str(user.id)] = user.name
        bot.scores[user.name] = 0
        bot.voter[str(user.id)] = []
        bot.vote_score[str(user.id)] = 0

        if str(user.id) != bot.spy_id:
            await user.send(
                f"เราอยู่กันที่ {place} ทำงานหน้าที่เป็น.. {DATA[place][i]}"
            )
        else:
            await user.send("นายเปง spy นะ เนียนๆ เข้าไว้")

    await asyncio.sleep(3)
    await ctx.send("ช่วงเวลาถามคำถาม หาตัวเจ้า spy เริ่ม!")
    message = await ctx.send("Timer start!")
    time = 10
    while True:
        try:
            await asyncio.sleep(1)
            time -= 1
            if time >= 3600:
                await message.edit(
                    content=f"Timer: {time // 3600} hours {time % 3600//60} minutes {time % 60} seconds"
                )
            elif time >= 60:
                await message.edit(
                    content=f"Timer: {time // 60} minutes {time % 60} seconds"
                )
            elif time < 60:
                await message.edit(content=f"Timer: {time} seconds")
            if time <= 0:
                await message.edit(content="Ended!")
                break
        except:
            break

    await message.edit(content="Vote time!")


@bot.command()
async def vote(ctx, user):
    bot.voted += 1
    voter_name = str(ctx.author).split("#")[0]
    print(bot.vote_score)
    print(bot.voter)
    print(bot.spy_id)
    print(user)
    # await asyncio.sleep(1)
    user_formatted = (
        str(user).replace("<", "").replace(">", "").replace("@", "").replace("!", "")
    )

    bot.vote_score[user_formatted] += 1
    bot.voter[user_formatted].append(voter_name)

    if bot.voted == len(bot.players):
        if max(bot.vote_score.values()) == bot.vote_score[bot.spy_id]:
            for v in bot.voter[bot.spy_id]:
                bot.scores[v] += 1
        result = "Rounds end:\n" + "\n".join(
            f"@{k}: {v} points" for k, v in bot.scores.items()
        )
        await ctx.send(result)


bot.run(os.getenv("TOKEN"))
