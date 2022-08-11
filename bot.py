import discord, json
from discord.ext import commands
from _module import ulang, stock, Dday, profile_message 

with open("data.json", "r") as file: json_data = json.load(file)
token, prefix = json_data["bot"]["token"], json_data["bot"]["prefix"]

bot = commands.Bot(
    command_prefix=prefix,
    status=discord.Status.online,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{prefix}help")
)

@bot.command(aliases=["ulang", "유러", "유랭", "u"])
async def ulang_command(ctx, convert: str, *, text: str):
    convert = "en" if convert == "암호화" else "de" if convert == "복호화" else "en"
    convert_text = ulang.encryption(text) if convert == "en" else ulang.decryption(text)
    
    embed = discord.Embed(
        title=f"\"{text}\" 를 변환합니다....",
        color=0x99ddff
    )
    embed.add_field(
        name="변환된 문장",
        value=convert_text
    )
    embed.set_footer(text="개발자: '^'#2854")
    await ctx.channel.send(embed=embed)  

@bot.command(aliases=["stock", "주식", "s"])
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

        embed.set_footer(text="개발자: '^'#2854")
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

        embed.set_footer(text="개발자: '^'#2854")
        await ctx.channel.send(embed=embed)

@bot.command(aliases=["dday", "디데이", "d"])
async def dday_command(ctx, command: str, date: str=None):
    dd = Dday.uld()
    user_id = str(ctx.author.id)

    if command in ["등록", "upload", "u"]:
        if not date:
            await ctx.channel.send("날짜 형식이 올바르지 않습니다.")
        else:
            dd.upload(user_id=user_id, date=date)
            await ctx.channel.send("등록 완료")

    elif command in ["삭제", "delete", "d"]:
        dd.delete(user_id=user_id)
        await ctx.channel.send("삭제 완료")

    elif command in ["조회", "보기", "load", "l"]:
        data = dd.load(user_id=user_id)
        if not data:
            await ctx.channel.send("등록된 디데이가 없음")
        else:
            dday = Dday.d_day(data["date"])
            await ctx.channel.send(("D+" if dday > 0 else "D") + str(dday) if dday != 0 else "D_Day!")

@bot.command(aliases=["한마디", "소개", "pm"])
async def pm_command(ctx, command: str, message: str=None):
    pm = profile_message.uld()
    user_id = str(ctx.author.id)

    if command in ["등록", "upload", "u"]:
        if not message:
            await ctx.channel.send("한마디 형식이 올바르지 않습니다")
        else:
            pm.upload(user_id=user_id, message=message)
            await ctx.channel.send("등록 완료")

    elif command in ["삭제", "delete", "d"]:
        pm.delete(user_id=user_id)
        await ctx.channel.send("삭제 완료")

    elif command in ["조회", "보기", "load", "l"]:
        load = pm.load(user_id=user_id)
        if not load:
            await ctx.channel.send("등록된 한마디가 없습니다")
        else:
            await ctx.channel.send(load)

bot.run(token)