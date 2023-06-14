import struct
import math

# 左循环移位
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF

# MD5的四个非线性函数
def F(x, y, z): return (x & y) | (~x & z)
def G(x, y, z): return (x & z) | (y & ~z)
def H(x, y, z): return x ^ y ^ z
def I(x, y, z): return y ^ (x | ~z)

# 定义四轮操作函数
def round_func(a, b, c, d, k, s, i, func, M):
    a = (a + func(b, c, d) + M[k] + T[i-1]) & 0xffffffff
    return ((b + left_rotate(a, s)) & 0xffffffff, a, b, c)

# MD5 padding
def md5_padding(data):
    bytes = bytearray(data, "utf8")

    orig_len_in_bits = (8 * len(bytes)) & 0xffffffffffffffff
    bytes.append(0x80)
    while len(bytes) % 64 != 56:
        bytes.append(0)
    bytes += struct.pack('<Q', orig_len_in_bits)

    return bytes

T = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

# 主函数，进行MD5加密
def md5(data):
    bytes = md5_padding(data)

    hash_pieces = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    for chunk_ofst in range(0, len(bytes), 64):
        a, b, c, d = hash_pieces
        chunk = bytes[chunk_ofst:chunk_ofst+64]
        M = struct.unpack('<16I', chunk)

        # 四轮加密过程
        for i in range(64):
            if i < 16:
                a, b, c, d = round_func(a, b, c, d, i, S[i], i+1, F, M)
            elif i < 32:
                a, b, c, d = round_func(a, b, c, d, (5*i + 1)%16, S[i], i+1, G, M)
            elif i < 48:
                a, b, c, d = round_func(a, b, c, d, (3*i + 5)%16, S[i], i+1, H, M)
            else:
                a, b, c, d = round_func(a, b, c, d, (7*i)%16, S[i], i+1, I, M)

        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xffffffff

    return "".join(f"{i:08x}" for i in hash_pieces)

# 测试MD5算法
print(md5("123456"))
