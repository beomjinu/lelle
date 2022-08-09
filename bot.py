import discord
from discord.ext import commands
from _module import ulang, stock

with open("data.txt", "r") as file:
    prefix, token = file.read().split(",")

bot = commands.Bot(
    command_prefix=prefix,
    status=discord.Status.online,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help")
)

@bot.command(aliases=["ulang"])
async def ulang_command(ctx, convert: str, *, text: str):
    convert = "en" if convert == "암호화" else "de" if convert == "복호화" else "en"
    convert_text = ulang.encryption(text) if convert == "en" else ulang.decryption(text)
    await ctx.channel.send("```" + convert_text + "```")  

@bot.command(aliases=["stock"])
async def stock_command(ctx, type: str, code: str):
    if type == "조회":
        _stock = stock.stock(code)

        embed = discord.Embed(
            title=f"{_stock.get_name()} | {code}",
            color=0x99ddff
        )

        embed.add_field(
            name="현재가",
            value=_stock.get_price(),
            inline=True
        )

        await ctx.channel.send(embed=embed)

    elif type == "검색":
        stock_list = stock.get_stock_list(code)
        
        embed = discord.Embed(
            title=f"\"{code}\"를 검색한 결과.. ",
            color=0x99ddff
        )

        if len(stock_list) == 0:
            embed.add_field(
                name=f"검색 결과가 없습니다.",
                value="검색어를 확인해주세요. (해외 주식은 조회 불가능 합니다.)",
                inline=False
            )
        else:
            for i in range(len(stock_list)):
                embed.add_field(
                    name=f"{i+1}. {stock_list[i][0]}",
                    value=f"코드 : {stock_list[i][1]}",
                    inline=False
                )

        embed.set_footer(text="개발자 github : https://github.com/beomjinu/lelle")

        await ctx.channel.send(embed=embed)


bot.run(token)