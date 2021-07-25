# bot.py
import os
import random
from dotenv import load_dotenv

# 1
import discord
from discord.ext import commands

load_dotenv()
# 봇 토큰임
TOKEN = os.getenv('DISCORD_TOKEN')

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
bot = commands.Bot(command_prefix='!')

# As you can see, Bot can handle events the same way that Client does.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Instead of using bot.event like before, you use bot.command(), passing the invocation command (name) as its argument.
# The function will now only be called when !99 is mentioned in chat. 
# This is different than the on_message() event, which was executed any time a user sent a message, regardless of the content.
# Any Command function (technically called a callback) must accept at least one parameter, called ctx, which is the Context surrounding the invoked Command.
# Keep in mind that all of this functionality exists only for the Bot subclass, not the Client superclass.
@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
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
'''
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int,  number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
'''
@bot.command(name='roll', help='roll 주사위면수')
async def roll(ctx, number_of_sides: int):
    await ctx.send(str(random.choice(range(1, number_of_sides + 1))))

@bot.command(name='create-channel', help='!craete-channel 채널이름 으로 채널 생성')
@commands.has_role('관리자')
# create_channel() which takes an optional channel_name and creates that channel
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    # discord.utils.get() to ensure that you don’t create a channel with the same name as an existing channel.
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await guild.create_text_channel(channel_name)
        await ctx.send('{} 생성됨'.format(channel_name))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)