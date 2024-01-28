import unittest
import sm2_sign


class TestPointAddition(unittest.TestCase):
    def test_point_addition(self):
        P = Point(3, 10)
        Q = Point(9, 7)

        expected = Point(1, 1)

        result = sm2_sign.point_addition(P, Q)

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
