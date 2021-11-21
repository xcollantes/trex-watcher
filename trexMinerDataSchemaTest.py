import unittest
from trexMinerDataSchema import TrexMinerDataSchema


class TestTrexMinerDataSchema(unittest.TestCase):
    def testSchemaType(self):
        self.assertTrue(isinstance(TrexMinerDataSchema({"": ""}), dict))


if __name__ == "__main__":
    unittest.main()
