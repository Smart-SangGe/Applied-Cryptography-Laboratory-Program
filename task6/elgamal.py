from Crypto.Util.number import *
import random

p = getPrime(512)
g = random.randint(2, p - 1)
a = random.randint(2, p - 2)
A = pow(g, a, p)

m = b"hello?world"
m = bytes_to_long(m)
k = random.randint(2, p - 2)
c1 = pow(g, k, p)
c2 = (m * pow(A, k, p)) % p
print("c1:", c1)
print("c2:", c2)

decrypt = (c2 * inverse(pow(c1, a, p), p)) % p
decrypt = long_to_bytes(decrypt)
print(decrypt)
