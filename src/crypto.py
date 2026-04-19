from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import config

def encrypt_payload(data_bytes):
    cipher = AES.new(config.AES_KEY, AES.MODE_CBC, config.AES_IV)
    return cipher.encrypt(pad(data_bytes, AES.block_size))

def encrypt_api_payload(hex_str):
    raw = bytes.fromhex(hex_str)
    cipher = AES.new(config.AES_KEY, AES.MODE_CBC, config.AES_IV)
    return cipher.encrypt(pad(raw, AES.block_size))
