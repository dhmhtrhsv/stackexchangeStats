import unittest
import stackexchangeStats


class TestStackstats(unittest.TestCase):

    def test_getDates(self):

        self.assertEqual(stackexchangeStats.getDates('2016-06-02-10-00-00', '2016-06-02-11-00-00'), (1464861600, 1464865200))


if __name__ == '__main__':
    unittest.main()