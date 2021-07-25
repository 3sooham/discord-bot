# bot.py
# https://discordpy.readthedocs.io/en/latest/api.html#
import os
import random
import discord
from dotenv import load_dotenv

# load_dotenv() loads environment variables from a .env file into your shell’s environment variables so that you can use them in your code.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


'''
There are two ways in discord.py to implement an event handler:

1. Using the client.event decorator
2. Creating a subclass of Client and overriding its handler methods
'''


# 1. Using the client.event decorator

# A Client is an object that represents a connection to Discord. A Client handles events, tracks state, and generally interacts with Discord APIs.
client = discord.Client()

@client.event
# Client and implemented its on_ready() event handler, 
# which handles the event when the Client has established a connection to Discord 
# and it has finished preparing the data that Discord has sent, such as login state, guild and channel data, and more.
async def on_ready():
    # In this case, you’re trying to find the guild with the same name as the one you stored in the DISCORD_GUILD environment variable. 
    # Once find() locates an element in the iterable that satisfies the predicate, 
    # it will return the element. 
    # This is essentially equivalent to the break statement in the previous example, but cleaner.
    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    # get() takes the iterable and some keyword arguments. 
    # The keyword arguments represent attributes of the elements in the iterable that must all be satisfied for get() to return the element.
    #guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        # f'{guild.name}(id: {guild.id})'
    )

    # member.name\n -member.name~ 이런식으로 join임
    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

@client.event
# on_member_join(), as its name suggests, handles the event of a new member joining a guild.
async def on_member_join(member):
    # await suspends the execution of the surrounding coroutine until the execution of each coroutine has finished.
    await member.create_dm()
    # await member.channel.send
    await member.dm_channel.send(
        f'Hi {member.name}, 코딩&로아방'
    )

'''
# 2. Creating a subclass of Client and overriding its handler methods
class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

client = CustomClient()
client.run(TOKEN)
'''

@client.event\
# on_message() occurs when a message is posted in a channel that your bot has access to.
async def on_message(message):
    # Because a Client can’t tell the difference between a bot user and a normal user account, 
    # your on_message() handler should protect against a potentially recursive case where the bot sends a message that it might, itself, handle.
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    # with 나올때 close도 자동으로 불러줌
    with open('err.log', 'a') as f:
        # If the Exception originated in the on_message() event handler, you .write() a formatted string to the file err.log. 
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        # If another event raises an Exception, then we simply want our handler to re-raise the exception to invoke the default behavior.
        else:
            raise

client.run(TOKEN)