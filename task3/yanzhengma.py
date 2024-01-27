import numpy as np


class LFSR:
    def __init__(self, seed, taps):
        self.state = np.array(list(map(int, seed)))
        self.taps = np.array(taps)
        self.length = len(seed)
        self.cycle = 0
        self.history = []

    def shift(self):
        output = self.state[-1]
        feedback = np.bitwise_xor.reduce(self.state[self.taps])
        self.state = np.roll(self.state, 1)
        self.state[0] = feedback
        return output

    def run(self, steps):
        output = []
        for _ in range(steps):
            current_state = "".join(map(str, self.state))
            if current_state in self.history:
                break
            self.history.append(current_state)
            for _ in range(4):  # 4-bit binary to one decimal
                output.append(self.shift())
            self.cycle += 1
        return output


# Create an instance of LFSR
lfsr = LFSR(seed="1001101001011101", taps=[0, 3, 12, 15])

# Run the LFSR
code = lfsr.run(100)

# Convert binary to decimal and print the code
print(
    "".join(
        [
            str(int("".join(map(str, code[i : i + 4])), 2))
            for i in range(0, len(code), 4)
        ]
    )
)

# Print the period
print("Period:", lfsr.cycle)  # 51
