import discord
from discord.ext import commands

with open("data.txt", "r") as file:
    prefix, token = file.read().split(",")

bot = commands.Bot(
    command_prefix=prefix,
    status=discord.Status.online,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help")
)

@bot.command(aliases=["ping"])
async def _ping(ctx):
    await ctx.channel.send("pong 🥳")


bot.run(token)