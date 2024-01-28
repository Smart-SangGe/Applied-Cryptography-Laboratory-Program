import random
import hashlib
from dataclasses import dataclass

# 椭圆曲线参数
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
# 逆天gpt3.5,把gxgy给错了
# Gx = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1719BEE90", 16)
# Gy = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E1", 16)
Gx = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7", 16)
Gy = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0", 16)


@dataclass
class Point:
    """
    define point class
    """

    x: int
    y: int


@dataclass
class Signature:
    """
    define signature
    """

    r: int
    s: int


# 点加法
def point_addition(P: Point, Q: Point) -> Point:
    """
    implment of sm2 point addition
    """
    # gpt4 version
    if P is None:
        return Q
    if Q is None:
        return P

    if P.x == Q.x and P.y == Q.y:  # Point doubling
        m = (3 * P.x**2 + a) * pow(2 * P.y, -1, p)
    else:
        m = (Q.y - P.y) * pow(Q.x - P.x, -1, p)

    Rx = (m**2 - P.x - Q.x) % p
    Ry = (m * (P.x - Rx) - P.y) % p

    return Point(Rx, Ry)


# 点倍乘
def point_multiplication(k: int, P: Point) -> Point:
    Q = None
    for i in range(k.bit_length()):
        if (k >> i) & 1:
            Q = point_addition(Q, P)
        P = point_addition(P, P)
    return Q


# SM2签名
def sm2_sign(message: bytes, private_key: int):
    d = private_key
    bytes_e = hashlib.sha256(message).digest()
    e = int.from_bytes(bytes_e)
    G = Point(Gx, Gy)
    max_iterations = 10000
    iteration = 0

    while iteration < max_iterations:
        k = random.randint(1, n - 1)
        public_key = point_multiplication(k, G)
        r = (e + public_key.x) % n
        if r == 0 or (r + k) == n:
            iteration += 1
            continue
        # s = (mod_inverse(1 + d, n) * (k - r * d)) % n
        s = (pow(1 + d, -1, n) * (k - r * d) % n) % n
        if s != 0:
            break
        iteration += 1

    if iteration == max_iterations:
        raise Exception("Failed to generate a valid signature.")

    return Signature(r, s)


# SM2验证
def sm2_verify(message: bytes, signature: Signature, public_key: Point) -> bool:
    r = signature.r
    s = signature.s
    bytes_e = hashlib.sha256(message).digest()
    e = int.from_bytes(bytes_e)
    G = Point(Gx, Gy)

    t = (r + s) % n
    if t == 0:
        return False

    # gpt3.5和4.0没一个顶用？？？？这验签计算和条件判断全错？？？？
    # point_1 = point_multiplication((mod_inverse(s, n) * t) % n, (Gx, Gy))
    # point_2 = point_multiplication((mod_inverse(s, n) * e) % n, public_key)
    point_1 = point_multiplication(s, G)
    point_2 = point_multiplication(t, public_key)
    point_3 = point_addition(point_1, point_2)
    
    # if (r % n) == (point_3.x % n):
    if r == ((e + point_3.x) % n):
        return True
    else:
        return False


# 求模反元素
def mod_inverse(a, m):
    if a < 0:
        a = a % m
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = m // a, m % a
        m, a = a, r
        x, y, u, v = u, v, x - q * u, y - q * v
    return x % m


# 示例用法
private_key = random.randint(1, n - 1)
public_key = point_multiplication(private_key, Point(Gx, Gy))
print("私钥:", private_key)
print("公钥:", public_key)

# 待签名的消息
message = b"22233455453423423423"

# 签名
signature = sm2_sign(message, private_key)
print("签名:", signature)

# 验证签名
is_valid = sm2_verify(message, signature, public_key)
print("签名验证结果:", is_valid)
