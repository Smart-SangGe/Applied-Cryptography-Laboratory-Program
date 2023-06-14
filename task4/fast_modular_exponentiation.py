def fast_modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus

        exponent = exponent // 2
        base = (base * base) % modulus

    return result


base = 3
exponent = 7
modulus = 12

result = fast_modular_exponentiation(base, exponent, modulus)
print(result)
