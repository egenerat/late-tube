from utils import parse_date
import datetime

import unittest

class TestLateTube(unittest.TestCase):

    def test_calculate_duration(self):
        self.assertEqual(0, 0)

    def test_parse_date(self):
    	dt = parse_date("19-Aug-2017", "19:33")
    	self.assertEqual(datetime.datetime(2017, 8, 19, 19, 33), dt)

    def test_parse_date_morning(self):
    	dt = parse_date("19-Aug-2017", "09:33")
    	self.assertEqual(datetime.datetime(2017, 8, 19, 9, 33), dt)

if __name__ == '__main__':
    unittest.main()