import random
import hashlib
from Crypto.Util.number import *


# 生成素数q
def generate_prime_q(bits):
    while True:
        q = random.getrandbits(bits - 1)
        q |= 1 << (bits - 1)
        if isPrime(q):
            return q


# 生成素数p
def generate_prime_p(q, bits):
    while True:
        k = random.getrandbits(bits - 1)
        p = k * q + 1
        if isPrime(p):
            return p


# 生成生成元g
def generate_generator(p, q):
    while True:
        h = random.randint(2, p - 1)
        g = pow(h, (p - 1) // q, p)
        if g != 1:
            return g


# 生成私钥和公钥
def generate_key_pair(bits):
    q = generate_prime_q(bits)
    p = generate_prime_p(q, bits)
    g = generate_generator(p, q)

    x = random.randint(1, q - 1)  # 私钥
    y = pow(g, x, p)  # 公钥

    private_key = x
    public_key = (p, q, g, y)

    return private_key, public_key


# DSA签名
def dsa_sign(message, private_key, public_key):
    p, q, g, y = public_key
    k = random.randint(1, q - 1)  # 随机数k

    r = pow(g, k, p) % q

    hashed_message = hashlib.sha1(message.encode()).digest()
    hashed_message_int = int.from_bytes(hashed_message, "big")

    s = (inverse(k, q) * (hashed_message_int + private_key * r)) % q

    return r, s


# DSA验证
def dsa_verify(message, signature, public_key):
    p, q, g, y = public_key
    r, s = signature

    hashed_message = hashlib.sha1(message.encode()).digest()
    hashed_message_int = int.from_bytes(hashed_message, "big")

    w = inverse(s, q)
    u1 = (hashed_message_int * w) % q
    u2 = (r * w) % q

    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q

    return v == r


# 示例用法
bits = 32  # 素数的位数

private_key, public_key = generate_key_pair(bits)
print("私钥:", private_key)
print("公钥:", public_key)

# 待签名的消息
message = "Hello, World!"

# 签名
signature = dsa_sign(message, private_key, public_key)
print("签名:", signature)

# 验证签名
is_valid = dsa_verify(message, signature, public_key)
print("签名验证结果:", is_valid)
