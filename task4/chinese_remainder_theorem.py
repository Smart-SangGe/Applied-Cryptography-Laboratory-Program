def chinese_remainder_theorem(n, a):
    sum = 0
    prod = 1

    for i in n:
        prod *= i

    for i in range(len(n)):
        p = prod // n[i]
        sum += a[i] * modular_inverse(p, n[i]) * p

    return sum % prod


def modular_inverse(a, m):
    g, x, y = extended_euclidean_algorithm(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist.")
    return x % m


def extended_euclidean_algorithm(a, b):
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_euclidean_algorithm(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


# 示例调用
n = [3, 5, 7]  # 模数列表
a = [2, 3, 2]  # 余数列表

result = chinese_remainder_theorem(n, a)
print("解:", result)
