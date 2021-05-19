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
GENERAL_TXT_CHANNEL = env['general_text_id']

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
channels = []
idchannel = GENERAL_TXT_CHANNEL

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
    with open('images/usersmagic_title.png', 'rb') as f:
        picture = discord.File(f)
        await member.send(file=picture)

    welcome_message = f"**Usersmagic Discord Topluluğu**'na **Hoşgeldin {member.name}**,\n\nSizi **usersmagic.com**'un bir üyesi olarak görmekten mutluluk duyuyoruz ve burada bulunduğunuz sürece keyif alacağınızı umuyoruz. :tophat: :innocent:\n\nBu sunucu, sizi Usersmagic ve sitemiz üzerinden para kazanabileceğiniz Usersmagic projeleri hakkında bilgilendirmek içindir. Kısa ve kolay anketlerle hızlıca para kazanabileceksiniz."
    await member.send(welcome_message)

    with open('images/server_rules.png', 'rb') as f:
        picture = discord.File(f)
        await member.send(file=picture)

    rules = f":small_blue_diamond: Diğer Kullanıcıları Rahatsız Etmeyin: Topluluğumuz üyelerini rahatsız edecek her türlü eylemden kaçınınız. Görevli olmayan topluluk üyelerine özelden mesaj atmayınız. Topluluğumuzda, Irkçılık, cinsiyetçilik, yabancı düşmanlığı, transfobi, homofobi, kadın düşmanlığı vb. eylemler yasaktır ve ban sebebidir.\n:small_blue_diamond: Topluluk içerisindeki iletişiminizi izniniz olan kanallarda yürütün: Aksi olasılıklarda topluluk yetkililerimizce uyarılacaksınız.\n:small_blue_diamond: Uygun bir dille kendinizi ifade edin: Topluluk kurallarımızla bağdaşmayacak şekilde, saygısızca belirtilecek olan herhangi bir görüş ban sebebidir. Topluluk içerisindekilerle karşılıklı saygıyı koruyunuz.\n:small_blue_diamond: Yetkiniz dışında hareket etmeyiniz: Diğer Usersmagic Discord Topluluğu kullanıcıları adına, moderatörler ya da yöneticiler adına görüş bildirmeyiniz.\n:small_blue_diamond: Arka arkaya 'Spam' mesajlar atmayınız: Herhangi bir konu hakkında, ne olursa olsun arka arkaya 'metin kanalı'nı ve tüm Usersmagic Discord Topluluğunu rahatsız edecek şekilde mesaj atmayınız. Bu geçici ban sebebi olarak değerlendirilebilir.\n:small_blue_diamond: Discord NSFW kuralları dışında bir içerik paylaşmayınız: Sunucu içerisinde ifade edeceğiniz her türlü mesaj ve içerik, sözlü ya da yazılı olması fark etmeksizin Discord NSFW kurallarına uymalıdır.\n"

    rules2 = ":small_blue_diamond: Uygunsuz veya saldırgan kullanıcı adları, durum veya profil resimleri kullanmayınız: Topluluk yetkililerince, bunları değiştirmeniz istenebilir.\n:small_blue_diamond: Yetkililer dışında paylaşılacak her türlü reklam, tanıtım, ticari kaygı içeren topluluk dışı içerik ve benzeri, hiçbir istisna içermeksizin yasaktır: Topluluğumuzun hiçbir 'metin kanalı'nda ya da 'sesli oda'sında ve hatta topluluğumuz içerisinde bulunan diğer kullanıcılara özelden bu tarz mesajlar içeren içerikler yollamak bu yasaklara tamamen dahildir.\n:small_blue_diamond: Topluluk yetkilileri dışında herhangi bir internet linki paylaşmak yasaktır: Bu, bundan önceki ve bundan sonraki hiçbir maddede belirtilen olgulara aykırı olmayan herhangi bir talebinizde @Moderatör 'lerimize ulaşınız.\n:small_blue_diamond: Usersmagic Discord Topluluğu Yetkilileri olan @Yönetici ve @Moderatör 'leri yetkilidir: Onların görevlerini sağlıkla sürdürmelerine yardımcı olunuz.\n:small_blue_diamond: Usersmagic Kullanıcı Sözleşmesi'ne, Discord Hizmet Koşulları'na ve Discord Topluluk İlkeleri'ne saygı duyunuz;\n\n:mega: https://tester.usersmagic.com/agreement/user.\n:mega: https://discord.com/terms.\n:mega: https://discord.com/guidelines."

    await member.send(rules)
    await member.send(rules2)


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
