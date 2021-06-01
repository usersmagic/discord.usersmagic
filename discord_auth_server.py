import socket
import logging
import sys
import threading
from dotenv import load_dotenv, dotenv_values
from encryption.AES256 import AESCipher

HOST = '127.0.0.1'
PORT = 5458

env = dotenv_values(".env")
FORMAT = '%(asctime)-15s %(levelname)-5s %(funcName)-10s %(lineno)s %(message)s'
KEY = env['SYMMETRIC_ENC_KEY']
logging.basicConfig(format=FORMAT, level=logging.INFO, stream=sys.stdout)
AESCipher = AESCipher(KEY)

# handle connections
def connection_thread(conn):
    data = conn.recv(1024)
    logging.info("data: {}".format(data))

    data = AESCipher.decrypt(data)
    logging.info("decrypted: {}".format(data))

    if "code=" in data:
        code_state = data.split('&')
        print(code_state)

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
