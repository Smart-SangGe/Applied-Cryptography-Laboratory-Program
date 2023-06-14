def lfsr(seed):
    lfsr_sequence = seed
    while True:
        # x^10 + x^8 + x^7 + x^5 + 1
        output = lfsr_sequence[0] ^ lfsr_sequence[2] ^ lfsr_sequence[3] ^ lfsr_sequence[5]
        lfsr_sequence = lfsr_sequence[1:] + [output]
        yield output


# Initialize the LFSR sequence with a 10-bit seed value
seed = [0, 0, 1, 1, 0, 1, 1, 0, 0, 1]

# Create a generator object for the LFSR sequence
lfsr_generator = lfsr(seed)

# Generate the first 10 bits of the LFSR sequence
for i in range(10):
    print(next(lfsr_generator), end="")
