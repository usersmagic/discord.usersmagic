# Work with Python 3.6
import discord
from chat_bot import *
import os
from dotenv import load_dotenv

env = dotenv_values(".env")
TOKEN = env['discord_token']
DEVELOPER = env['developer']
DEVELOPER_CHANNEL = env['developer_channel_id']
ADMIN1 = env['admin1']
ADMIN1_CHANNEL = env['admin1_channel_id']
ADMIN2 = env['admin2']
ADMIN2_CHANNEL = env['admin2_channel_id']

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
channels = []
idchannel = 0

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
    global idchannel
    #advertisement filter
    if(message.channel.id == idchannel and not (has_role(message.author, "Yönetici") or has_role(message.author, "Moderatör")) and ("usersmagic" not in message.content or "discord" not in message.content) and ("https://" in message.content or "http://" in message.content or "www" in message.content) ):
        await message.delete()
        await message.channel.send("İllegal link paylaşımı algılandı, bu durum ilgili birimlere bildirilmiştir...")
        developer = await client.fetch_user(DEVELOPER)
        #admin1 = await client.fetch_user(ADMIN1)
        #admin2 = await client.fetch_user(ADMIN2)
        await developer.send("{} isimli kişinin link paylaşmaya çalıştığı tespit edildi, mesajın içeriği: {}".format(message.author.name, message.content))
        #await admin1.send("{} isimli kişinin link paylaşmaya çalıştığı tespit edildi, mesajın içeriği: {}".format(message.author.name, message.content))
        #await admin2.send("{} isimli kişinin link paylaşmaya çalıştığı tespit edildi, mesajın içeriği: {}".format(message.author.name, message.content))

    # chat bot
    else:
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
            if msg != "no response":
                await message.channel.send(msg)

        if message.content.startswith('!bağlan') and has_role(message.author, "Yönetici"):
            botStatus.connect()

        if message.content.startswith('!kop') and has_role(message.author, "Yönetici"):
            botStatus.disconnect()

@client.event
async def on_member_join(member):
    await client.get_channel(idchannel).send(f"Hoşgeldin {member.name}!")

@client.event
async def on_ready():
    global idchannel
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for guild in client.guilds:
        print("operating on servers: {}, {}".format(guild.name, guild.id))
        for channel in guild.text_channels:
            if channel.id == 831135841703165975:
                idchannel = channel.id
                print(idchannel)

    print('------')

def has_role(member, role):
    roles = member.roles

    for m_role in roles:
        if m_role.name == role:
            return True

    return False

client.run(TOKEN)
