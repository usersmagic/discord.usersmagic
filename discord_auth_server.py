import socket
import logging
import sys
import threading
from dotenv import load_dotenv, dotenv_values
from encryption.AES256 import AESCipher
import requests
import json

HOST = '127.0.0.1'
PORT = 5458

env = dotenv_values(".env")
KEY = env['SYMMETRIC_ENC_KEY']
CLIENT_ID= env['client_id']
CLIENT_SECRET = env['client_secret']
GUILD_ID = env['guild_id']
API_ENDPOINT = 'https://discord.com/api/v8'
BOT_TOKEN = env['discord_token']

FORMAT = '%(asctime)-15s %(levelname)-5s %(funcName)-10s %(lineno)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, stream=sys.stdout)
AESCipher = AESCipher(KEY)

def exchange_code(code):
    redirect_uri = 'http://localhost:3000/discord'
    data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    r.raise_for_status()
    return r.json()

def getUserInformation(token_type, access_token):
    headers =  {
        'Authorization': '{} {}'.format(token_type, access_token)
    }
    r = requests.get('%s/oauth2/@me' % API_ENDPOINT, headers= headers)
    return r.json()

def addUserToGuild(token_type, access_token, user_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bot {}'.format(BOT_TOKEN)
    }
    data = {
        'access_token' : '{}'.format(access_token)
    }

    r = requests.put('%s/guilds/{}/members/{}'.format(GUILD_ID, user_id) % API_ENDPOINT, headers= headers, data=json.dumps(data))
    print(r.status_code)

def sendBackUserId(id, conn):
    print("id: {}".format(id))
    data = AESCipher.encrypt(id)
    conn.send(data)
    # you need control here, if it works

# handle connections
def connection_thread(conn):
    data = conn.recv(1024)
    logging.info("data: {}".format(data))

    data = AESCipher.decrypt(data)
    logging.info("decrypted: {}".format(data))

    if "code=" in data:
        code_state = data.split('&')
        code = code_state[0].split("code=")[1]
        print(code)
        ret = exchange_code(code)
        user_inf = getUserInformation(ret['token_type'], ret['access_token'])
        addUserToGuild(ret['token_type'], ret['access_token'], user_inf["user"]["id"])
        sendBackUserId(user_inf["user"]["id"], conn)

    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    logging.info('\tServer is up on {} port number: {}'.format(HOST,PORT))

    # run the server
    while True:
        conn, addr = s.accept()
        logging.info('Connected by {}'.format(addr))

        # multi-threading
        connect_thread = threading.Thread(target=connection_thread, args=(conn,))
        connect_thread.start()
