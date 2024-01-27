from Crypto.Util.number import *

p = getPrime(512)
q = getPrime(512)
e = 65537

n = p * q

m = b"helloworld"
m = bytes_to_long(m)
cipher = pow(m, e, n)
print(cipher)

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
decrypt = pow(cipher, d, n)
decrypt = long_to_bytes(decrypt)
print(decrypt)
