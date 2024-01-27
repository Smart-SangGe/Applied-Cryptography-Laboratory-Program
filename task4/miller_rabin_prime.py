import random


def is_prime(n, k=5):
    if n <= 1:
        return False

    # 处理小素数情况
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    # 将 n-1 表示为 2^r * d 的形式
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # 进行 k 轮检测
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1
        if is_prime(n):
            return n


bits = 1024
prime = generate_prime(bits)
print("生成的大素数:", prime)
