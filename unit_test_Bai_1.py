import unittest
import Bai_1

class TestMomoWallet(unittest.TestCase):
    def setUp(self):
        Bai_1.balance = 0

    def test_deposit_logic(self):
        Bai_1.deposit_logic(500000)
        self.assertEqual(Bai_1.balance, 500000)

    def test_transfer_insufficient(self):
        Bai_1.balance = 100000
        with self.assertRaises(RuntimeError):
            Bai_1.transfer_logic(200000, "0912345678")

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            Bai_1.deposit_logic(-1000)

if __name__ == "__main__":
    unittest.main()