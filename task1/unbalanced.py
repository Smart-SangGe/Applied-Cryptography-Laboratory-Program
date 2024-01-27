def unbalanced_network(plaintext, subkeys):
    """非平衡网络"""
    # 初始置换
    permuted = [plaintext[IP_TABLE[i] - 1] for i in range(64)]
    left = permuted[:32]
    right = permuted[32:]
    # 进行16轮非平衡运算
    for i in range(16):
        # 将左右两边的数据块都与子密钥进行异或
        left = [left[j] ^ subkeys[i][j] for j in range(32)]
        right = [right[j] ^ subkeys[i][j] for j in range(32)]
        # 交换左右两边的数据块
        left, right = right, left
    # 逆初始置换
    ciphertext = [left[i] for i in range(32)] + [right[i] for i in range(32)]
    ciphertext = [ciphertext[IP_TABLE_INVERSE[i] - 1] for i in range(64)]
    return ciphertext


def unbalanced_network_decrypt(ciphertext, subkeys):
    """非平衡网络的解密过程"""
    # 初始置换
    permuted = [ciphertext[IP_TABLE[i] - 1] for i in range(64)]
    left = permuted[:32]
    right = permuted[32:]
    # 进行16轮非平衡解密运算，子密钥使用反序
    for i in range(15, -1, -1):
        # 交换左右两边的数据块
        left, right = right, left
        # 将左右两边的数据块都与子密钥进行异或
        left = [left[j] ^ subkeys[i][j] for j in range(32)]
        right = [right[j] ^ subkeys[i][j] for j in range(32)]
    # 逆初始置换
    plaintext = [left[i] for i in range(32)] + [right[i] for i in range(32)]
    plaintext = [plaintext[IP_TABLE_INVERSE[i] - 1] for i in range(64)]
    return plaintext


def generate_subkeys(key):
    """生成16个子密钥"""
    # 将64位密钥转换成56位
    permuted_key = [key[PC1_TABLE[i] - 1] for i in range(56)]
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
        subkey = [combined[PC2_TABLE[i] - 1] for i in range(48)]
        subkeys.append(subkey)
    return subkeys


# PC1置换表
PC1_TABLE = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]

# PC2置换表
PC2_TABLE = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]

IP_TABLE = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]

IP_TABLE_INVERSE = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]


if __name__ == "__main__":
    plaintext = [
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
    ]
    key = [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    # 将明文和密钥转化为二进制格式的数组
    plaintext = [
        int(b)
        for b in "{0:b}".format(int("".join([str(bit) for bit in plaintext]), 2)).zfill(
            64
        )
    ]
    key = [
        int(b)
        for b in "{0:b}".format(int("".join([str(bit) for bit in key]), 2)).zfill(64)
    ]

    print(plaintext)
    print(key)
    # 生成子密钥
    subkeys = generate_subkeys(key)

    # 加密明文
    ciphertext = unbalanced_network(plaintext, subkeys)

    # 将密文转化为十六进制格式
    ciphertext_hex = hex(int("".join([str(bit) for bit in ciphertext]), 2))[2:].zfill(
        16
    )

    print(
        "Plaintext (in hex): ",
        hex(int("".join([str(bit) for bit in plaintext]), 2))[2:].zfill(16),
    )
    print(
        "Key (in hex): ", hex(int("".join([str(bit) for bit in key]), 2))[2:].zfill(16)
    )
    print("Ciphertext (in hex): ", ciphertext_hex)
