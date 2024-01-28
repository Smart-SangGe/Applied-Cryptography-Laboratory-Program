import unittest
from sm2_sign import *


class TestSM2(unittest.TestCase):
    def setUp(self):
        # 初始化用于测试的点和密钥
        self.P = Point(Gx, Gy)
        self.private_key = random.randint(1, n - 1)
        self.public_key = point_multiplication(self.private_key, self.P)

    def test_point_addition(self):
        # 测试点加法
        # 选择两个点 P 和 Q，并计算 R = P + Q
        Q = point_multiplication(2, self.P)  # 例如，取P的两倍作为另一个点
        R = point_addition(self.P, Q)
        # [此处添加断言以验证 R 的正确性]

    def test_point_multiplication(self):
        # 测试点倍乘
        # 计算 kP 并验证
        k = 3
        R = point_multiplication(k, self.P)
        # [此处添加断言以验证 R 的正确性]

    def test_sm2_sign_and_verify(self):
        # 测试签名和验证
        message = b"Hello, SM2!"
        signature = sm2_sign(message, self.private_key)
        self.assertTrue(sm2_verify(message, signature, self.public_key))
        # 测试错误的签名
        wrong_message = b"Wrong message"
        self.assertFalse(sm2_verify(wrong_message, signature, self.public_key))


if __name__ == "__main__":
    unittest.main()
