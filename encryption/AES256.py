import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

KEY_LENGTH = 32
class AESCipher(object):

    def __init__(self, key):
        AES.block_size = 16
        self.bs = AES.block_size
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = enc.decode().split(",")
        iv = base64.b64decode(enc[0])
        cipher_text = base64.b64decode(enc[1])

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = self._unpad(cipher.decrypt(cipher_text)).decode("utf-8")

        return plain_text

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
