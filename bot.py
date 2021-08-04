# bot.py
# https://realpython.com/how-to-make-a-discord-bot-python/
import os
import random
from dotenv import load_dotenv

import requests
import json
from bs4 import BeautifulSoup

# 1
import discord
from discord.ext import commands

load_dotenv()
# 봇 토큰임
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD2 = os.getenv('DISCORD_GUILD2')

'''
# 메시지 작성자게게 핑침
# await ctx.send(f'{ctx.author.mention}')

# ctx.guild 내의 멤버들 가져옴
async for member in ctx.guild.fetch_members(limit=150):
    print(member.name)
    print(member)

# bot이 들어간 서버내의 멤버들을 가져옴
async def members(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            print(member)

# 특정 롤 멘션하기
await ctx.send(discord.utils.get(ctx.guild.roles, name="Role Name").mention)

# discord.utils.find는 가장 처음의 것만 리턴해줌
guild = discord.utils.find(lambda g: g.name == GUILD2 or g.name == GUILD2, bot.guilds)
print(f'{bot.user} is connected to the following guild:\n')
print(f'{guild.name}(id: {guild.id})')

# Instead of using bot.event like before, you use bot.command(), passing the invocation command (name) as its argument.
# The function will now only be called when !99 is mentioned in chat. 
# This is different than the on_message() event, which was executed any time a user sent a message, regardless of the content.
# Any Command function (technically called a callback) must accept at least one parameter, called ctx, which is the Context surrounding the invoked Command.
# Keep in mind that all of this functionality exists only for the Bot subclass, not the Client superclass.

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    # ctx
    # A Context holds data such as the channel and guild that the user called the Command from.
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

# Sometimes, you require a parameter to be a certain type, but arguments to a Command function are, by default, strings.
# str(random.choice(range(1, number_of_sides + 1))) 이거 range에서 에러남 number_of_sides가 string이기 때문임
# async def roll(ctx, number_of_dice,  number_of_sides): 이렇게 하면 안된다는거임
'
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int,  number_of_sides: int):
    # _는 또한 어떤 특정값을 무시하기 위한 용도로 사용되기도한다. 값이 필요하지 않거나 사용되지 않는 값을 _에 할당하기만 하면된다.
    # 이제 그러니까 dice에 str(random.choice(range(1, number_of_sides + 1))을 number_of_dice만큼 반복한 거를 넣는거임
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

'''

# 2
# A Bot is a subclass of Client that adds a little bit of extra functionality that is useful when you’re creating bot users. 
# For example, a Bot can handle events and commands, invoke validation checks, and more.
# In general terms, a command is an order that a user gives to a bot so that it will do something. 
# Commands are different from events because they are:
# Arbitrarily defined
# Directly called by the user
# Flexible, in terms of their interface
# In technical terms, a Command is an object that wraps a function that is invoked by a text command in Discord. 
# The text command must start with the command_prefix, defined by the Bot object.
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# As you can see, Bot can handle events the same way that Client does.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    # Flattening into a list
    guilds = await bot.fetch_guilds(limit=150).flatten()
    for guild in guilds:
        print(f'{bot.user} is connected to the following guild:')
        print(f'{guild.name}(id: {guild.id})')

# op.gg 크롤링으로 롤 티어 불러오기
# 다음에는 롤 공식 api로 가져와보기
@bot.command(name='티어')
# *으로 명령어 뒤의 모든 내용 가져옴
async def lol_tier(ctx, *, name):
    url = 'https://www.op.gg/summoner/userName=' + name
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    nick = soup.select_one('body > div.l-wrap.l-wrap--summoner > div.l-container > div > div > div.Header > div.Profile > div.Information > span')
    if nick == None:
        await ctx.send(f'{name}은 없는 닉네임임')
    else:
        nick = nick.get_text()
        selector = '#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > '
        rank = soup.select_one(selector + 'div.TierRank').get_text()

        if rank.split()[0] == 'Unranked':
            print('second if')
            await ctx.send(f'{nick} is {rank}')
        else:
            selector += ' div.TierInfo > '
            lp = soup.select_one(selector + 'span.LeaguePoints').get_text().split()[0]
            win = soup.select_one(selector + 'span.WinLose > span.wins').get_text()
            loss = soup.select_one(selector + 'span.WinLose > span.losses').get_text()
            win_rate = soup.select_one(selector + 'span.WinLose > span.winratio').get_text().split()[2]
            
            print(f'{name}\n{rank} \n{lp} LP\n{win} {loss}\n승률 {win_rate}')
            await ctx.send(f'{name}\n{rank}\n{lp} LP\n{win} {loss}\n승률 {win_rate}')

# user 리스트 안에 있는 멤버들 mention함
@bot.command(name='ㄱ')
async def pind_to_loa_users(ctx):
    user = ['kukudas#2547',
            '사막하비화면#9955',
            '사막하비/96#6851',
            '늡눕이#1480',
            '이상제#8961',
            '레카#0822',
           ]

    async for member in ctx.guild.fetch_members(limit=150):
        if str(member) in user:
            await ctx.send(member.mention + "ㄱ")

# 주사위
@bot.command(name='roll', help='roll 주사위면수')
async def roll(ctx, number_of_sides: int):
    await ctx.send(str(random.choice(range(1, number_of_sides + 1))))

@bot.command(name='create-channel', help='!craete-channel 채널이름 으로 채널 생성')
# @commands.has.role은 if message.author == client.user: 대체로 사용가능함
@commands.has_role('관리자')
# create_channel() which takes an optional channel_name and creates that channel
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    # discord.utils.get() to ensure that you don’t create a channel with the same name as an existing channel.
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        # await suspends the execution of the surrounding coroutine until the execution of each coroutine has finished.
        await guild.create_text_channel(channel_name)
        await ctx.send(f'{format(channel_name)} 생성됨')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)