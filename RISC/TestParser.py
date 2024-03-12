import unittest
from Parser import Parser


class TestParser(unittest.TestCase):

    def test_parse_instruction(self):
        parser = Parser()

        test_cases = [
            {"instruction": "ADD R2,R1,R4", "expected_binary": "00000010001000010100000000000000"},
            {"instruction": "BZ R3,8", "expected_binary": "01100000000000110000000000001000"},
        ]
        for case in test_cases:
            binary_code = parser.parse_instruction(case["instruction"], 1)

            self.assertEqual(binary_code, case["expected_binary"])


if __name__ == "__main__":
    unittest.main()
