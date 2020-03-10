import unittest
import time
from temperature_tracker import TemperatureTracker

class TestTempTracker(unittest.TestCase):
    def test_average_all_same(self):
        """Test that the average temperature is calculated correctly when all
        input is the same"""

        temp_data = [(32.00, time.localtime()), (32.00, time.localtime()),
                     (32.00, time.localtime()), (32.00, time.localtime())]

        tt = TemperatureTracker()
        result = tt.average_from(temp_data)
        self.assertEqual(result, 32.0)

        # test the regular average function the user will call
        tt = TemperatureTracker(temp_data)
        result = tt.average()
        self.assertEqual(result, 32.0)



    def test_average_all_different(self):
        """Test that the average temperature is calculated correctly when all
        input is different"""

        temp_data = [(1.00, time.localtime()), (2.00, time.localtime()),
                     (3.00, time.localtime()), (4.00, time.localtime())]

        tt = TemperatureTracker()
        result = tt.average_from(temp_data)
        self.assertEqual(result, 2.5)


    def test_minimum_all_different(self):
        """Test that the minimum temperature and time are calculated correctly when all
                input is the same"""
        temp_data = [(1.00, time.localtime()), (2.00, time.localtime()),
                     (3.00, time.localtime()), (4.00, time.localtime())]

        tt = TemperatureTracker()
        result = tt.minimum_from(temp_data)
        self.assertEqual(result[0], 1.0)
        self.assertEqual(temp_data[0][1], result[1])


    def test_minimum_all_same(self):
        """Test that the minimum temperature and time are calculated correctly when all
                        input is the same"""

        temp_data = [(3.00, time.localtime()), (3.00, time.localtime()),
                     (3.00, time.localtime()), (3.00, time.localtime())]

        tt = TemperatureTracker()
        result = tt.minimum_from(temp_data)
        self.assertEqual(result[0], 3.0)
        self.assertEqual(temp_data[3][1], result[1])


    def test_maximum_all_different(self):
        """Test that the maximum temperature and time are calculated correctly when all
                        input is different"""

        temp_data = [(92.00, time.localtime()), (102.00, time.localtime()),
                     (83.00, time.localtime()), (104.30, time.localtime())]

        tt = TemperatureTracker()
        result = tt.maximum_from(temp_data)
        self.assertEqual(result[0], 104.3)
        self.assertEqual(temp_data[3][1], result[1])


    def test_maximum_all_same(self):
        """Test that the maximum temperature and time are calculated correctly when all
                        input is the same"""

        temp_data = [(83.00, time.localtime()), (83.00, time.localtime()),
                     (83.00, time.localtime()), (83.00, time.localtime()), (83.00, time.localtime())]

        tt = TemperatureTracker()
        result = tt.maximum_from(temp_data)
        self.assertEqual(result[0], 83.0)
        self.assertEqual(temp_data[3][1], result[1])


    # def test_check_true(self):
    #     """Test that the temperature has exceeded safe values--positive test case"""
    #
    #     temp_data = [(83.00, time.localtime()), (83.00, time.localtime()),
    #                  (83.00, time.localtime()), (83.00, time.localtime()), (83.00, time.localtime())]
    #
    #     tt = TemperatureTracker()
    #     result = tt.check_from(temp_data)
    #     self.assertEqual(result, True)
    #
    #
    # def test_check_false(self):
    #     """Test that the temperature has exceeded safe values--negative test case"""
    #
    #     temp_data = [(3.00, time.localtime()), (2.00, time.localtime()),
    #                  (3.00, time.localtime()), (6.00, time.localtime()), (81.00, time.localtime())]
    #
    #     tt = TemperatureTracker()
    #     result = tt.check_from(temp_data)
    #     self.assertEqual(result, False)


    def test_get_start_true(self):
        """Test that the start value can be returned if the tracker has started
            --positive test case"""

        tt = TemperatureTracker()
        tt.start()
        self.assertIsNotNone(tt.get_start())


    def test_get_start_false(self):
        """Test that the start value cannot be returned if the tracker hasn't started
            --negative test case"""

        tt = TemperatureTracker()
        self.assertIsNone(tt.get_start())


    def test_get_stop_true(self):
        """Test that the stop value can be returned if the tracker has been stopped
            --positive test case"""

        tt = TemperatureTracker()
        tt.stop()
        self.assertIsNotNone(tt.get_stop())


    def test_get_stop_false(self):
        """Test that the stop value cannot be returned if the tracker hasn't stopped
            --negative test case"""

        tt = TemperatureTracker()
        self.assertIsNone(tt.get_stop())


    def test_count_when_data_present(self):
        """Test that we can get the count if there is temperature data
         -- positive test case"""
        temp_data = [(1.00, time.localtime()), (2.00, time.localtime()),
                     (3.00, time.localtime()), (4.00, time.localtime())]

        tt = TemperatureTracker(temp_data)
        result = tt.count_from(temp_data)
        self.assertEqual(result, 4)


    def test_count_when_data_is_not_present(self):
        """Test that we can't get the count if there isn't temperature data
         -- negative test case"""

        temp_data = []

        tt = TemperatureTracker()
        result = tt.count_from(temp_data)
        self.assertEqual(result, 0)


    def test_temperatures_when_data_present(self):
        """Test that temperature data can be retrieved when there is data
         --positive test case"""

        temp_data = [(1.00, time.localtime()), (2.00, time.localtime()),
                     (3.00, time.localtime()), (4.00, time.localtime())]

        tt = TemperatureTracker(temp_data)
        result = tt.temperatures()
        for i in range(0, len(result)):
            self.assertEqual(result[i][0], temp_data[i][0])
            self.assertEqual(result[i][1], temp_data[i][1])


    def test_temperatures_when_data_is_not_present(self):
        """Test that temperature data can't be retrieved when there isn't data
         --negative test case"""

        tt = TemperatureTracker()
        result = tt.temperatures()
        self.assertEqual(result, [])


    def test_update_from(self):
        temp_data = [(1.00, time.localtime()), (2.00, time.localtime()),
                     (3.00, time.localtime()), (4.00, time.localtime())]

        temp_data2 = [(1.00, time.localtime()), (2.00, time.localtime()),
                     (3.00, time.localtime()), (4.00, time.localtime()), (6.00, time.localtime())]

        tt = TemperatureTracker(temp_data)
        tt.update_from((5.00, time.localtime()), temp_data)
        self.assertEqual(5, len(tt.temperatures()))

        # test overwriting the list with an empty list and appending a new reading
        tt.update_from((5.00, time.localtime()), [])
        self.assertEqual(1, len(tt.temperatures()))

        tt.update_from((5.00, time.localtime()), temp_data2)
        self.assertEqual(6, len(tt.temperatures()))



if __name__ == '__main__':
    unittest.main()