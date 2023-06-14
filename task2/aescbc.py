from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# AES密钥需要是16、24或32字节
key = get_random_bytes(16)

# 用于CBC模式的初始化向量需要是16字节
iv = get_random_bytes(16)

data = "Hello, world!".encode()  # 转换为字节串进行加密

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(data, AES.block_size))


print(ciphertext)

# 解密过程
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

print(plaintext)
