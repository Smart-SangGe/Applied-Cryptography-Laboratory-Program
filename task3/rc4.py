def rc4(key, plaintext):
    # Key-Scheduling Algorithm (KSA)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    ciphertext = bytearray()
    for byte in plaintext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        ciphertext.append(byte ^ k)

    return ciphertext


def rc4_decrypt(key, ciphertext):
    # Use the same RC4 algorithm for decryption
    return rc4(key, ciphertext)


# Set the key and plaintext
key = [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF]
plaintext = b"Hello World!"

# Encrypt the plaintext using RC4 algorithm
ciphertext = rc4(key, plaintext)

# Print the ciphertext
print(ciphertext)

# Decrypt the ciphertext using RC4 algorithm
plaintext = rc4_decrypt(key, ciphertext)

# Print the plaintext
print(plaintext)
