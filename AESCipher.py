import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32  # block size for padding
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw: bytes) -> bytes:
        """Encrypt raw bytes and return base64 encoded bytes"""
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc: bytes) -> bytes:
        """Decrypt base64 encoded bytes back to raw bytes"""
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s: bytes) -> bytes:
        """Pad data to make its length multiple of block size"""
        padding_len = self.bs - len(s) % self.bs
        padding = bytes([padding_len]) * padding_len
        return s + padding

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        """Remove padding"""
        return s[:-s[-1]]
