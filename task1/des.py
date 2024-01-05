import binascii
from Crypto.Cipher import DES

# 加密函数
def des_encrypt(key, plaintext):
    # 将密钥和明文转换为字节流
    key_bytes = key.encode('utf-8')
    plaintext_bytes = plaintext.encode('utf-8')
    # 使用DES算法创建密码对象
    des = DES.new(key_bytes, DES.MODE_ECB)
    # 将明文进行补位操作
    plaintext_bytes_padded = plaintext_bytes + (8 - len(plaintext_bytes) % 8) * b'\0'
    # 对补位后的明文进行加密
    ciphertext_bytes = des.encrypt(plaintext_bytes_padded)
    # 将加密后的字节流转换为16进制字符串
    ciphertext_hex = binascii.b2a_hex(ciphertext_bytes).decode('utf-8')
    return ciphertext_hex

# 解密函数
def des_decrypt(key, ciphertext_hex):
    # 将密钥和密文转换为字节流
    key_bytes = key.encode('utf-8')
    ciphertext_bytes = binascii.a2b_hex(ciphertext_hex.encode('utf-8'))
    # 使用DES算法创建密码对象
    des = DES.new(key_bytes, DES.MODE_ECB)
    # 对密文进行解密
    plaintext_bytes_padded = des.decrypt(ciphertext_bytes)
    # 去除补位
    plaintext_bytes = plaintext_bytes_padded.rstrip(b'\0')
    # 将解密后的字节流转换为字符串
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext

# 密钥
key = '01234567'
# 明文
plaintext = 'Hello, DES!'
# 加密
ciphertext = des_encrypt(key, plaintext)
print('Ciphertext:', ciphertext)
# 解密
decrypted = des_decrypt(key, ciphertext)
print('Decrypted:', decrypted)
