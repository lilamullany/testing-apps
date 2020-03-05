import unittest
from temptracker import TemperatureTracker

class TestTempTracker(unittest.TestCase):
    def test_average_all_same(self):
        """Test that the average temperature is calculated correctly"""

        temp_data = [(32.00, '2020-03-02 20:52:59'), (32.00, '2020-03-02 19:52:59'),
                     (32.00, '2020-03-02 18:52:59'), (32.00, '2020-03-02 17:52:59')]

        tt = TemperatureTracker()
        result = tt.average(temp_data)
        self.assertEqual(result.split("/")[0], "32.00C")


    def test_average_all_different(self):
        temp_data = [(1.00, '2020-03-02 20:52:59'), (2.00, '2020-03-02 19:52:59'),
                     (3.00, '2020-03-02 18:52:59'), (4.00, '2020-03-02 17:52:59')]

        tt = TemperatureTracker()
        result = tt.average(temp_data)
        self.assertEqual(result.split("/")[0], "2.50C")


if __name__ == '__main__':
    unittest.main()