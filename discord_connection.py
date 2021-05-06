# Work with Python 3.6
import discord
from chat_bot import *
import os
from dotenv import load_dotenv

env = dotenv_values(".env")
TOKEN = env['discord_token']

client = discord.Client()
channels = []

class Status:
    def __init__(self,connected,channel):
        self.connected = connected
        self.channel = channel

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

botList = []

def get_bot_from_channel(ch):
    for x in botList:
        if x.channel == ch:
            return x
    return Status(False, null)

@client.event
async def on_message(message):
    ch = message.channel

    if ch in channels:
        botStatus = get_bot_from_channel(ch)
    else:
        channels.append(ch)
        botStatus = Status(False,ch)
        botList.append(botStatus)

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if botStatus.connected is True:
        print(message.content)
        msg = create_response(message.content)
        print(msg)
        await message.channel.send(msg)

    if message.content.startswith('#gel'):
        botStatus.connect()

    if message.content.startswith('#git'):
        botStatus.disconnect()

@client.event
async def on_member_join(ctx, *, member):
    channel = member.server.get_channel("channel id")
    fmt = 'Welcome to the {1.name} Discord server, {0.mention}'
    await ctx.send_message(channel, fmt.format(member, member.server))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
