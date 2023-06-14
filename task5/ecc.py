'''
Author: Smart-SangGe 2251250136@qq.com
Date: 2023-05-24 14:38:38
LastEditors: Smart-SangGe 2251250136@qq.com
LastEditTime: 2023-05-24 14:43:43
FilePath: \task5\ecc.py
Description: ecc
'''
class EllipticCurve:
    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def add_points(P, Q, curve):
    if P is None:  # None represents the identity element
        return Q
    if Q is None:
        return P

    x1, y1 = P.x, P.y
    x2, y2 = Q.x, Q.y

    if x1 == x2 and y1 == y2:  # P and Q are the same point
        m = (3 * x1 ** 2 + curve.a) * pow(2 * y1, -1, curve.mod)
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, curve.mod)

    m %= curve.mod

    x3 = (m ** 2 - x1 - x2) % curve.mod
    y3 = (m * (x1 - x3) - y1) % curve.mod

    return Point(x3, y3)


def multiply_point(n, P, curve):
    result = None
    addend = P

    while n:
        if n & 1:  # if the last digit of n is 1
            result = add_points(result, addend, curve)
        addend = add_points(addend, addend, curve)
        n >>= 1  # divide n by 2

    return result

if __name__ == '__main__':
    
    # Define a curve
    curve = EllipticCurve(a=2, b=3, mod=97)

    # Define two points
    P = Point(x=3, y=6)
    Q = Point(x=7, y=10)

    # Add two points
    R = add_points(P, Q, curve)
    print(f"P + Q = ({R.x}, {R.y})")

    # Multiply a point
    S = multiply_point(2, P, curve)
    print(f"2P = ({S.x}, {S.y})")