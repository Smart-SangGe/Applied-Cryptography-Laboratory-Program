import binascii


def AES_encrypt(key, data):
    # 将需要加密的数据按16bytes进行分块
    state = [data[i : i + 16] for i in range(0, len(data), 16)]

    # 若最后一个数据块不满16bytes，则以数据00进行填充
    if len(state[-1]) < 16:
        state[-1] += b"\x00" * (16 - len(state[-1]))

    # 扩展密钥
    round_keys = generate_round_keys(key)
    # 执行第一轮轮密钥加
    add_round_key(state, round_keys[0])

    # 执行后9轮加密操作
    for i in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[i])

    # 执行
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[10])

    # Flatten the state array and return the result
    return b"".join(state)


def generate_round_keys(key):
    # 初始化密钥矩阵
    round_keys = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(11)]

    # 放入初始密钥
    for i in range(4):
        for j in range(4):
            round_keys[0][i][j] = key[i + 4 * j]

    rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    # 进行密钥扩展
    for i in range(1, 11):
        # 交换次序
        round_keys[i][0][0] = round_keys[i - 1][1][3]
        round_keys[i][1][0] = round_keys[i - 1][2][3]
        round_keys[i][2][0] = round_keys[i - 1][3][3]
        round_keys[i][3][0] = round_keys[i - 1][0][3]

        # 利用s盒进行替换
        for j in range(4):
            round_keys[i][j][0] = sub_bytes_column(round_keys[i][j][0])

        # 与常量进行异或
        round_keys[i][0][0] = round_keys[i][0][0] ^ rcon[i]

        # 进行密钥扩展
        for k in range(4):
            round_keys[i][k][0] = round_keys[i][k][0] ^ round_keys[i - 1][k][0]
        for j in range(1, 4):
            for k in range(4):
                round_keys[i][k][j] = round_keys[i][k][j - 1] ^ round_keys[i - 1][k][j]

    return round_keys


def add_round_key(state, round_key):
    # 依次对矩阵进行异或操作
    for i in range(len(state)):
        temp = b""
        for j in range(4):
            for k in range(4):
                temp += (state[i][j + k * 4] ^ round_key[k][j]).to_bytes(1, "big")
        state[i] = temp
    return state


def sub_bytes_column(state):
    # 设置s盒
    sbox = [
        0x63,
        0x7C,
        0x77,
        0x7B,
        0xF2,
        0x6B,
        0x6F,
        0xC5,
        0x30,
        0x01,
        0x67,
        0x2B,
        0xFE,
        0xD7,
        0xAB,
        0x76,
        0xCA,
        0x82,
        0xC9,
        0x7D,
        0xFA,
        0x59,
        0x47,
        0xF0,
        0xAD,
        0xD4,
        0xA2,
        0xAF,
        0x9C,
        0xA4,
        0x72,
        0xC0,
        0xB7,
        0xFD,
        0x93,
        0x26,
        0x36,
        0x3F,
        0xF7,
        0xCC,
        0x34,
        0xA5,
        0xE5,
        0xF1,
        0x71,
        0xD8,
        0x31,
        0x15,
        0x04,
        0xC7,
        0x23,
        0xC3,
        0x18,
        0x96,
        0x05,
        0x9A,
        0x07,
        0x12,
        0x80,
        0xE2,
        0xEB,
        0x27,
        0xB2,
        0x75,
        0x09,
        0x83,
        0x2C,
        0x1A,
        0x1B,
        0x6E,
        0x5A,
        0xA0,
        0x52,
        0x3B,
        0xD6,
        0xB3,
        0x29,
        0xE3,
        0x2F,
        0x84,
        0x53,
        0xD1,
        0x00,
        0xED,
        0x20,
        0xFC,
        0xB1,
        0x5B,
        0x6A,
        0xCB,
        0xBE,
        0x39,
        0x4A,
        0x4C,
        0x58,
        0xCF,
        0xD0,
        0xEF,
        0xAA,
        0xFB,
        0x43,
        0x4D,
        0x33,
        0x85,
        0x45,
        0xF9,
        0x02,
        0x7F,
        0x50,
        0x3C,
        0x9F,
        0xA8,
        0x51,
        0xA3,
        0x40,
        0x8F,
        0x92,
        0x9D,
        0x38,
        0xF5,
        0xBC,
        0xB6,
        0xDA,
        0x21,
        0x10,
        0xFF,
        0xF3,
        0xD2,
        0xCD,
        0x0C,
        0x13,
        0xEC,
        0x5F,
        0x97,
        0x44,
        0x17,
        0xC4,
        0xA7,
        0x7E,
        0x3D,
        0x64,
        0x5D,
        0x19,
        0x73,
        0x60,
        0x81,
        0x4F,
        0xDC,
        0x22,
        0x2A,
        0x90,
        0x88,
        0x46,
        0xEE,
        0xB8,
        0x14,
        0xDE,
        0x5E,
        0x0B,
        0xDB,
        0xE0,
        0x32,
        0x3A,
        0x0A,
        0x49,
        0x06,
        0x24,
        0x5C,
        0xC2,
        0xD3,
        0xAC,
        0x62,
        0x91,
        0x95,
        0xE4,
        0x79,
        0xE7,
        0xC8,
        0x37,
        0x6D,
        0x8D,
        0xD5,
        0x4E,
        0xA9,
        0x6C,
        0x56,
        0xF4,
        0xEA,
        0x65,
        0x7A,
        0xAE,
        0x08,
        0xBA,
        0x78,
        0x25,
        0x2E,
        0x1C,
        0xA6,
        0xB4,
        0xC6,
        0xE8,
        0xDD,
        0x74,
        0x1F,
        0x4B,
        0xBD,
        0x8B,
        0x8A,
        0x70,
        0x3E,
        0xB5,
        0x66,
        0x48,
        0x03,
        0xF6,
        0x0E,
        0x61,
        0x35,
        0x57,
        0xB9,
        0x86,
        0xC1,
        0x1D,
        0x9E,
        0xE1,
        0xF8,
        0x98,
        0x11,
        0x69,
        0xD9,
        0x8E,
        0x94,
        0x9B,
        0x1E,
        0x87,
        0xE9,
        0xCE,
        0x55,
        0x28,
        0xDF,
        0x8C,
        0xA1,
        0x89,
        0x0D,
        0xBF,
        0xE6,
        0x42,
        0x68,
        0x41,
        0x99,
        0x2D,
        0x0F,
        0xB0,
        0x54,
        0xBB,
        0x16,
    ]
    # 根据s盒进行替换
    return sbox[state]


def sub_bytes(state):
    # 设置s盒
    sbox = [
        0x63,
        0x7C,
        0x77,
        0x7B,
        0xF2,
        0x6B,
        0x6F,
        0xC5,
        0x30,
        0x01,
        0x67,
        0x2B,
        0xFE,
        0xD7,
        0xAB,
        0x76,
        0xCA,
        0x82,
        0xC9,
        0x7D,
        0xFA,
        0x59,
        0x47,
        0xF0,
        0xAD,
        0xD4,
        0xA2,
        0xAF,
        0x9C,
        0xA4,
        0x72,
        0xC0,
        0xB7,
        0xFD,
        0x93,
        0x26,
        0x36,
        0x3F,
        0xF7,
        0xCC,
        0x34,
        0xA5,
        0xE5,
        0xF1,
        0x71,
        0xD8,
        0x31,
        0x15,
        0x04,
        0xC7,
        0x23,
        0xC3,
        0x18,
        0x96,
        0x05,
        0x9A,
        0x07,
        0x12,
        0x80,
        0xE2,
        0xEB,
        0x27,
        0xB2,
        0x75,
        0x09,
        0x83,
        0x2C,
        0x1A,
        0x1B,
        0x6E,
        0x5A,
        0xA0,
        0x52,
        0x3B,
        0xD6,
        0xB3,
        0x29,
        0xE3,
        0x2F,
        0x84,
        0x53,
        0xD1,
        0x00,
        0xED,
        0x20,
        0xFC,
        0xB1,
        0x5B,
        0x6A,
        0xCB,
        0xBE,
        0x39,
        0x4A,
        0x4C,
        0x58,
        0xCF,
        0xD0,
        0xEF,
        0xAA,
        0xFB,
        0x43,
        0x4D,
        0x33,
        0x85,
        0x45,
        0xF9,
        0x02,
        0x7F,
        0x50,
        0x3C,
        0x9F,
        0xA8,
        0x51,
        0xA3,
        0x40,
        0x8F,
        0x92,
        0x9D,
        0x38,
        0xF5,
        0xBC,
        0xB6,
        0xDA,
        0x21,
        0x10,
        0xFF,
        0xF3,
        0xD2,
        0xCD,
        0x0C,
        0x13,
        0xEC,
        0x5F,
        0x97,
        0x44,
        0x17,
        0xC4,
        0xA7,
        0x7E,
        0x3D,
        0x64,
        0x5D,
        0x19,
        0x73,
        0x60,
        0x81,
        0x4F,
        0xDC,
        0x22,
        0x2A,
        0x90,
        0x88,
        0x46,
        0xEE,
        0xB8,
        0x14,
        0xDE,
        0x5E,
        0x0B,
        0xDB,
        0xE0,
        0x32,
        0x3A,
        0x0A,
        0x49,
        0x06,
        0x24,
        0x5C,
        0xC2,
        0xD3,
        0xAC,
        0x62,
        0x91,
        0x95,
        0xE4,
        0x79,
        0xE7,
        0xC8,
        0x37,
        0x6D,
        0x8D,
        0xD5,
        0x4E,
        0xA9,
        0x6C,
        0x56,
        0xF4,
        0xEA,
        0x65,
        0x7A,
        0xAE,
        0x08,
        0xBA,
        0x78,
        0x25,
        0x2E,
        0x1C,
        0xA6,
        0xB4,
        0xC6,
        0xE8,
        0xDD,
        0x74,
        0x1F,
        0x4B,
        0xBD,
        0x8B,
        0x8A,
        0x70,
        0x3E,
        0xB5,
        0x66,
        0x48,
        0x03,
        0xF6,
        0x0E,
        0x61,
        0x35,
        0x57,
        0xB9,
        0x86,
        0xC1,
        0x1D,
        0x9E,
        0xE1,
        0xF8,
        0x98,
        0x11,
        0x69,
        0xD9,
        0x8E,
        0x94,
        0x9B,
        0x1E,
        0x87,
        0xE9,
        0xCE,
        0x55,
        0x28,
        0xDF,
        0x8C,
        0xA1,
        0x89,
        0x0D,
        0xBF,
        0xE6,
        0x42,
        0x68,
        0x41,
        0x99,
        0x2D,
        0x0F,
        0xB0,
        0x54,
        0xBB,
        0x16,
    ]

    # 根据s盒进行替换
    for i in range(len(state)):
        temp = b""
        for j in range(16):
            temp += (sbox[state[i][j]]).to_bytes(1, "big")
        state[i] = temp
    return state


def shift_rows(state):
    # 行移位
    for i in range(len(state)):
        temp = (
            state[i][0].to_bytes(1, "big")
            + state[i][5].to_bytes(1, "big")
            + state[i][8].to_bytes(1, "big")
            + state[i][12].to_bytes(1, "big")
        )
        temp += (
            state[i][5].to_bytes(1, "big")
            + state[i][9].to_bytes(1, "big")
            + state[i][13].to_bytes(1, "big")
            + state[i][1].to_bytes(1, "big")
        )
        temp += (
            state[i][10].to_bytes(1, "big")
            + state[i][14].to_bytes(1, "big")
            + state[i][2].to_bytes(1, "big")
            + state[i][6].to_bytes(1, "big")
        )
        temp += (
            state[i][15].to_bytes(1, "big")
            + state[i][3].to_bytes(1, "big")
            + state[i][7].to_bytes(1, "big")
            + state[i][11].to_bytes(1, "big")
        )

        state[i] = temp

    return state


def mix_columns(state):
    matrix = [2, 3, 1, 1, 1, 2, 3, 1, 1, 1, 2, 3, 3, 1, 1, 2]

    # 进行矩阵乘法
    for i in range(len(state)):
        result = [0] * 16
        temp = b""

        for j in range(4):
            result[4 * j] = (
                gf_mult(matrix[4 * j], state[i][0])
                ^ gf_mult(matrix[4 * j + 1], state[i][1])
                ^ gf_mult(matrix[4 * j + 2], state[i][2])
                ^ gf_mult(matrix[4 * j + 3], state[i][3])
            )
            result[4 * j + 1] = (
                gf_mult(matrix[4 * j], state[i][4])
                ^ gf_mult(matrix[4 * j + 1], state[i][5])
                ^ gf_mult(matrix[4 * j + 2], state[i][6])
                ^ gf_mult(matrix[4 * j + 3], state[i][7])
            )
            result[4 * j + 2] = (
                gf_mult(matrix[4 * j], state[i][8])
                ^ gf_mult(matrix[4 * j + 1], state[i][9])
                ^ gf_mult(matrix[4 * j + 2], state[i][10])
                ^ gf_mult(matrix[4 * j + 3], state[i][11])
            )
            result[4 * j + 3] = (
                gf_mult(matrix[4 * j], state[i][12])
                ^ gf_mult(matrix[4 * j + 1], state[i][13])
                ^ gf_mult(matrix[4 * j + 2], state[i][14])
                ^ gf_mult(matrix[4 * j + 3], state[i][15])
            )

        for j in range(4):
            for k in range(4):
                temp += result[j + 4 * k].to_bytes(1, "big")

        state[i] = temp

    return state


def xtime(a, count):
    for i in range(0, count):
        if a >> 7 == 1:
            a = (0xFF & (a << 1)) ^ 0x1B
        else:
            a = a << 1
    return a


# GF(2^8)有限域上乘法函数
def gf_mult(a, b):
    if a == 0 or b == 0:
        return 0
    index_of_1_list = []  # 获得所有位数为1的下标 例如: 10011 返回一个[0,1,4] 的列表
    count = 0

    while b != 0:
        if b & 0x1 == 1:
            index_of_1_list.append(count)
        count += 1
        b = b >> 1

    xtime_result_list = []
    # 获取所有1的下标后 算出每次的结果 放在xtime_result_list列表中
    for i in index_of_1_list:
        xtime_result_list.append(xtime(a, i))

    # 将所有结果异或 得到的就是结果
    res = xtime_result_list[0]
    for i in range(1, len(xtime_result_list)):
        res = res ^ xtime_result_list[i]
    return res


# aes-128算法的密钥为128bits，16bytes
key = b"abcdefghijklmnop"

data = b"abcdefghijklmnop"

encrypted = AES_encrypt(key, data)

print(binascii.hexlify(encrypted))
