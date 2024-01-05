from gmssl import sm4 # pylint: disable=e0401

# 加密函数
def sm4_encrypt(key, plaintext):
    # 将密钥和明文转换为字节流
    key_bytes = key.encode('utf-8')
    plaintext_bytes = plaintext.encode('utf-8')
    # 创建SM4密码对象
    cipher = sm4.CryptSM4()
    # 设置密钥
    cipher.set_key(key_bytes, sm4.SM4_ENCRYPT)
    # 对明文进行加密
    ciphertext_bytes = cipher.crypt_ecb(plaintext_bytes)
    # 将加密后的字节流转换为16进制字符串
    ciphertext_hex = ciphertext_bytes.hex()
    return ciphertext_hex

# 解密函数
def sm4_decrypt(key, ciphertext_hex):
    # 将密钥和密文转换为字节流
    key_bytes = key.encode('utf-8')
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    # 创建SM4密码对象
    cipher = sm4.CryptSM4()
    # 设置密钥
    cipher.set_key(key_bytes, sm4.SM4_DECRYPT)
    # 对密文进行解密
    plaintext_bytes = cipher.crypt_ecb(ciphertext_bytes)
    # 将解密后的字节流转换为字符串
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext

# 密钥
key = '0123456789abcdef'
# 明文
plaintext = 'Hello, SM4!'
# 加密
ciphertext = sm4_encrypt(key, plaintext)
print('Ciphertext:', ciphertext)
# 解密
decrypted = sm4_decrypt(key, ciphertext)
print('Decrypted:', decrypted)

