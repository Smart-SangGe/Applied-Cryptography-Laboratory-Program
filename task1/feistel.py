def feistel_round(left, right, subkey):
    """Feistel轮函数"""
    # 将右边的半个数据块作为输入
    # 进行扩展置换
    expanded = [right[E_TABLE[i]-1] for i in range(48)]
    # 将结果与子密钥进行异或
    xored = [expanded[i] ^ subkey[i] for i in range(48)]
    # 进行S盒代替
    sbox_output = []
    for i in range(8):
        start = i*6
        end = (i+1)*6
        row = (xored[start] << 1) + xored[end-1]
        col = (xored[start+1] << 3) + (xored[start+2] << 2) + \
            (xored[start+3] << 1) + xored[start+4]
        sbox_output.extend(
            [int(b) for b in "{0:b}".format(S_BOXES[i][row][col]).zfill(4)])
    # 进行P盒置换
    permuted = [sbox_output[P_TABLE[i]-1] for i in range(32)]
    # 将左边的半个数据块作为输出，右边的半个数据块与轮函数的输出进行异或
    return right, [left[i] ^ permuted[i] for i in range(32)]


def feistel_network(plaintext, subkeys):
    """Feistel平衡网络"""
    # 初始置换
    permuted = [plaintext[IP_TABLE[i]-1] for i in range(64)]
    left = permuted[:32]
    right = permuted[32:]
    # 进行16轮Feistel运算
    for i in range(16):
        left, right = feistel_round(left, right, subkeys[i])
    # 逆初始置换
    ciphertext = [left[i] for i in range(32)] + [right[i] for i in range(32)]
    ciphertext = [ciphertext[IP_TABLE_INVERSE[i]-1] for i in range(64)]
    return ciphertext


def generate_subkeys(key):
    """生成16个子密钥"""
    # 将64位密钥转换成56位
    permuted_key = [key[PC1_TABLE[i]-1] for i in range(56)]
    # 分成左右两个28位
    left = permuted_key[:28]
    right = permuted_key[28:]
    subkeys = []
    # 生成16个子密钥
    for i in range(16):
        # 左移位数
        if i in [0, 1, 8, 15]:
            shift = 1
        else:
            shift = 2
        # 左移
        left = left[shift:] + left[:shift]
        right = right[shift:] + right[:shift]
        # 合并
        combined = left + right
        # 进行压缩置换，生成48位子密钥
        subkey = [combined[PC2_TABLE[i]-1] for i in range(48)]
        subkeys.append(subkey)
    return subkeys


def feistel_round_decrypt(left, right, subkey):
    """Feistel轮函数的解密过程"""
    # 将右边的半个数据块作为输入
    # 进行扩展置换
    expanded = [right[E_TABLE[i]-1] for i in range(48)]
    # 将结果与子密钥进行异或
    xored = [expanded[i] ^ subkey[i] for i in range(48)]
    # 进行S盒代替
    sbox_output = []
    for i in range(8):
        start = i*6
        end = (i+1)*6
        row = (xored[start] << 1) + xored[end-1]
        col = (xored[start+1] << 3) + (xored[start+2] << 2) + \
            (xored[start+3] << 1) + xored[start+4]
        sbox_output.extend(
            [int(b) for b in "{0:b}".format(S_BOXES[i][row][col]).zfill(4)])
    # 进行P盒置换
    permuted = [sbox_output[P_TABLE[i]-1] for i in range(32)]
    # 将左边的半个数据块作为输出，右边的半个数据块与轮函数的输出进行异或
    return right, [left[i] ^ permuted[i] for i in range(32)]


def feistel_network_decrypt(ciphertext, subkeys):
    """Feistel平衡网络的解密过程"""
    # 初始置换
    permuted = [ciphertext[IP_TABLE[i]-1] for i in range(64)]
    left = permuted[:32]
    right = permuted[32:]
    # 进行16轮Feistel解密运算，子密钥使用反序
    for i in range(15, -1, -1):
        left, right = feistel_round_decrypt(left, right, subkeys[i])
    # 逆初始置换
    plaintext = [left[i] for i in range(32)] + [right[i] for i in range(32)]
    plaintext = [plaintext[IP_TABLE_INVERSE[i]-1] for i in range(64)]
    return plaintext


# PC1置换表
PC1_TABLE = [57, 49, 41, 33, 25, 17, 9, 1,
             58, 50, 42, 34, 26, 18, 10, 2,
             59, 51, 43, 35, 27, 19, 11, 3,
             60, 52, 44, 36, 63, 55, 47, 39,
             31, 23, 15, 7, 62, 54, 46, 38,
             30, 22, 14, 6, 61, 53, 45, 37,
             29, 21, 13, 5, 28, 20, 12, 4]

# PC2置换表
PC2_TABLE = [14, 17, 11, 24, 1, 5, 3, 28,
             15, 6, 21, 10, 23, 19, 12, 4,
             26, 8, 16, 7, 27, 20, 13, 2,
             41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56,
             34, 53, 46, 42, 50, 36, 29, 32]


E_TABLE = [32, 1, 2, 3, 4, 5,
           4, 5, 6, 7, 8, 9,
           8, 9, 10, 11, 12, 13,
           12, 13, 14, 15, 16, 17,
           16, 17, 18, 19, 20, 21,
           20, 21, 22, 23, 24, 25,
           24, 25, 26, 27, 28, 29,
           28, 29, 30, 31, 32, 1]

IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

IP_TABLE_INVERSE = [40, 8, 48, 16, 56, 24, 64, 32,
                    39, 7, 47, 15, 55, 23, 63, 31,
                    38, 6, 46, 14, 54, 22, 62, 30,
                    37, 5, 45, 13, 53, 21, 61, 29,
                    36, 4, 44, 12, 52, 20, 60, 28,
                    35, 3, 43, 11, 51, 19, 59, 27,
                    34, 2, 42, 10, 50, 18, 58, 26,
                    33, 1, 41, 9, 49, 17, 57, 25]

P_TABLE = [16, 7, 20, 21, 29, 12, 28, 17,
           1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9,
           19, 13, 30, 6, 22, 11, 4, 25]

S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],

    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],

    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


if __name__ == "__main__":
    plaintext = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
                 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
                 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
                 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    key = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
           1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

    # 将明文和密钥转化为二进制格式的数组
    plaintext = [int(b) for b in "{0:b}".format(
        int("".join([str(bit) for bit in plaintext]), 2)).zfill(64)]
    key = [int(b) for b in "{0:b}".format(
        int("".join([str(bit) for bit in key]), 2)).zfill(64)]

    print(plaintext)
    print(key)
    # 生成子密钥
    subkeys = generate_subkeys(key)

    # 加密明文
    ciphertext = feistel_network(plaintext, subkeys)

    # 将密文转化为十六进制格式
    ciphertext_hex = hex(int("".join([str(bit) for bit in ciphertext]), 2))[
        2:].zfill(16)

    print("Plaintext (in hex):  ", hex(
        int("".join([str(bit) for bit in plaintext]), 2))[2:].zfill(16))
    print("Key (in hex):        ", hex(
        int("".join([str(bit) for bit in key]), 2))[2:].zfill(16))
    print("Ciphertext (in hex):", ciphertext_hex)
    
    
