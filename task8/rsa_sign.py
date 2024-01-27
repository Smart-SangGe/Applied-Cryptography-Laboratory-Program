from Crypto.Util.number import *


# 扩展欧几里得算法
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


# 求模反元素
def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd == 1:
        return (x % m + m) % m
    return None


# 生成密钥对
def generate_key_pair():
    # 选择两个大素数 p 和 q
    p = getPrime(32)

    q = getPrime(32)

    # 计算 N = p * q
    N = p * q

    # 计算欧拉函数值 φ(N) = (p - 1) * (q - 1)
    phi_N = (p - 1) * (q - 1)

    e = 65537

    # 计算 d 的模反元素
    d = mod_inverse(e, phi_N)

    # 返回公钥和私钥
    public_key = (N, e)
    private_key = (N, d)
    return public_key, private_key


# RSA签名
def rsa_sign(message, private_key):
    N, d = private_key
    return pow(message, d, N)


# RSA验证
def rsa_verify(message, signature, public_key):
    N, e = public_key
    return pow(signature, e, N) == message


# 示例用法
# 生成密钥对
public_key, private_key = generate_key_pair()
print("公钥:", public_key)
print("私钥:", private_key)

# 待签名的消息
message = 123456789

# 签名
signature = rsa_sign(message, private_key)
print("签名:", signature)

# 验证签名
is_valid = rsa_verify(message, signature, public_key)
print("签名验证结果:", is_valid)
