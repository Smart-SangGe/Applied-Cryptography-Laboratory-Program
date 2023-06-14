import random
import hashlib

# 椭圆曲线参数
p = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16)
a = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16)
b = int("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16)
n = int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
Gx = int("32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1719BEE90", 16)
Gy = int("BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E1", 16)


# 点加法
def point_addition(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if P[0] == Q[0] and P[1] == -Q[1] % p:
        return None

    if P[0] == Q[0] and P[1] == Q[1]:
        lam = (3 * P[0] ** 2 + a) * pow(2 * P[1], p-2, p)
    else:
        lam = (Q[1] - P[1]) * pow(Q[0] - P[0], p-2, p)

    x = (lam ** 2 - P[0] - Q[0]) % p
    y = (lam * (P[0] - x) - P[1]) % p
    return (x, y)

# 点倍乘
def point_multiplication(k, P):
    Q = None
    for i in range(k.bit_length()):
        if (k >> i) & 1:
            Q = point_addition(Q, P)
        P = point_addition(P, P)
    return Q



# SM2签名
def sm2_sign(message, private_key):
    d = private_key
    e = message

    max_iterations = 100
    iteration = 0

    while iteration < max_iterations:
        k = random.randint(1, n-1)
        x1, y1 = point_multiplication(k, (Gx, Gy))
        r = (e + x1) % n
        if r == 0 or (r + k) == n:
            iteration += 1
            continue
        s = (mod_inverse(1 + d, n) * (k - r * d)) % n
        if s != 0:
            break
        print(iteration)
        iteration += 1

    if iteration == max_iterations:
        raise Exception("Failed to generate a valid signature.")

    return r, s

# SM2验证
def sm2_verify(message, signature, public_key):
    r, s = signature
    e = message

    t = (r + s) % n
    if t == 0:
        return False

    x1, y1 = point_multiplication((mod_inverse(s, n) * t) % n, (Gx, Gy))
    x2, y2 = point_multiplication((mod_inverse(s, n) * e) % n, public_key)
    x, y = point_addition((x1, y1), (x2, y2))
    if (r % n) == (x % n):
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
private_key = random.randint(1, n-1)
public_key = point_multiplication(private_key, (Gx, Gy))
print("私钥:", private_key)
print("公钥:", public_key)

# 待签名的消息
message = 122233455453423423423

# 签名
signature = sm2_sign(message, private_key)
print("签名:", signature)

# 验证签名
is_valid = sm2_verify(message, signature, public_key)
print("签名验证结果:", is_valid)
