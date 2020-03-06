from gpiozero import CPUTemperature
import time


class TemperatureTracker:
    # TODO: Can either uncomment or remove these from final commit
    # "{:1.2f}C/{:1.2f}F at time {}".format(min_temp, (((min_temp * (9 / 5)) + 32)), time.strftime('%Y-%m-%d %H:%M:%S', min_temp_time))
    # "{:1.2f}C/{:1.2f}F at time {}".format(max_temp, (((max_temp * (9 / 5)) + 32)), time.strftime('%Y-%m-%d %H:%M:%S',max_temp_time))
    # "{:1.2f}C/{:1.2f}F".format(average_temp, (((average_temp * (9 / 5)) + 32)))

    def __init__(self, temp_list=[]):
        self.temp_list = temp_list
        # TODO: I think you can remove all these properties, just rerun the functions that provide their
        # values when needed.
        self.max = 0.0,
        self.max_temp_time = time.localtime(),
        self.min = 0.0,
        self.min_temp_time = time.localtime(),
        self.ave = 0.0,
        self.start_timestamp = None,
        self.stop_timestamp = None,
        self.temp_count = 0

    # TODO: Recommend reworking this function to return a tuple with the min. temp from the list
    def minimum(self, temp_list):
        """
        TODO: Add NumpPy styled docstrings: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html

        Get the minimum temperature listed from a... 

        Params
        -------
        temp_list
            A list of...
        Returns
        -------


        """
        # TODO: Alt solution if returning a tuple:
        result = temp_list[0][0]
        for temp, time in temp_list:
            if temp < result.temperature:
                result = temp
        return result

        # min_temp = temp_list[0][0]
        # min_temp_time = time.localtime()

        # for i in range(0, len(temp_list)):
        #     current_temp = temp_list[i][0]

        #     # track the maximum temperature
        #     if current_temp < min_temp:
        #         min_temp = current_temp
        #         min_temp_time = temp_list[i][1]

        # # update the instance variables
        # self.min_temp_time = min_temp_time
        # self.min = min_temp

        # return min_temp

    # TODO: Can we do method overloading in Python?
    def minimum(self):
        """
        TODO: Simple description
        """
        # TODO: Alt option if only using a temp_list property for your class
        return minimum(self, self.temp_list)[0]

        # min_temp = self.temp_list[0][0]
        # min_temp_time = time.localtime()

        # for i in range(0, len(self.temp_list)):
        #     current_temp = self.temp_list[i][0]

        #     # track the maximum temperature
        #     if current_temp < min_temp:
        #         min_temp = current_temp
        #         min_temp_time = self.temp_list[i][1]

        # # update the instance variables
        # self.min_temp_time = min_temp_time
        # self.min = min_temp

        # return min_temp

    def maximum(self, temp_list):
        '''
        TODO: Simple description
        '''
        max_temp = 0.0
        max_temp_time = time.localtime()

        for i in range(0, len(temp_list)):
            current_temp = temp_list[i][0]

            # track the maximum temperature
            if current_temp > max_temp:
                max_temp = current_temp
                max_temp_time = temp_list[i][1]

        # update the instance variables
        self.max_temp_time = max_temp_time
        self.max = max_temp

        return max_temp

    def maximum(self):
        """
        TODO: Simple description
        """
        max_temp = 0.0
        max_temp_time = time.localtime()

        for i in range(0, len(self.temp_list)):
            current_temp = self.temp_list[i][0]

            # track the maximum temperature
            if current_temp > max_temp:
                max_temp = current_temp
                max_temp_time = self.temp_list[i][1]

        # update the instance variables
        self.max_temp_time = max_temp_time
        self.max = max_temp

        return max_temp

    def update(self, temp_list):
        """Updates the input argument list with the current CPU temperature
        as well as the current time.

        TODO: Expand Docstring
        """

        cpu = CPUTemperature()
        new_reading = (cpu.temperature,  time.localtime())
        temp_list.append(new_reading)
        self.temp_list = temp_list
        self.temp_count = len(temp_list)

    def update(self):
        """Updates the object argument list with the current CPU temperature
        as well as the current time.

        TODO: Expand Docstring
        """

        cpu = CPUTemperature()
        new_reading = (cpu.temperature, time.localtime())
        self.temp_list.append(new_reading)
        self.temp_count = len(self.temp_list)

    def average(self, temp_list):
        """
        TODO: Simple description
        """
        total_temp = 0.0
        count = 0

        # calculate average temperature
        for i in range(0, len(temp_list)):
            current_temp = temp_list[i][0]
            total_temp = total_temp + current_temp
            count = count + 1

        average_temp = total_temp / count
        return average_temp

    def average(self):
        """
        TODO: Simple description
        """
        total_temp = 0.0
        count = 0

        # calculate average temperature
        for i in range(0, len(self.temp_list)):
            current_temp = self.temp_list[i][0]
            total_temp = total_temp + current_temp
            count = count + 1

        average_temp = total_temp / count
        return average_temp

    def count(self, temp_list):
        count = len(temp_list)
        return count

    def count(self):
        count = len(self.temp_list)
        return count

    def temperatures(self):
        """
        TODO: Docstring
        """
        return self.temp_list

    def start(self):
        """
        TODO: Simple description
        """
        self.start_timestamp = time.localtime()

    def stop(self):
        """
        TODO: Simple description 
        """
        self.stop_timestamp = time.localtime()

        # def stop_tracker(temp_data):
        # temp_data['stop_timestamp'] = time.localtime()

    def summary(self, temp_list):
        """Prints out a summary of the temperature readings in easy to read format.

        Includes average temperature, the number of readings,
        the maximum temperature and the minimum temperature.

        TODO: Expand to Docstring

        """
        temp_dict = {}

        # first make sure all readings are up to date
        temp_dict['average'] = self.average(temp_list)
        temp_dict['minimum'] = self.min(temp_list)
        temp_dict['maximum'] = self.max(temp_list)
        temp_dict['count'] = self.count(temp_list)
        temp_dict['start_timestamp'] = self.start_timestamp
        temp_dict['stop_timestamp'] = self.start_timestamp

        if temp_dict['start_timestamp'] is None:
            return "The temperature tracker has not yet been started"
        else:
            summary_string = "The temperature tracker was started at: " + \
                             time.strftime('%Y-%m-%d %H:%M:%S',
                                           temp_dict['start_timestamp']) + "\n"
            summary_string += "A total of " + \
                str(temp_dict['count']) + " have been gathered\n"
            summary_string += "The readings so far are: \n"

            for i in range(0, len(self.temp_list)):
                summary_string += "\t\t" + "{:1.2f}C/{:1.2f}F at time {}\n".format(temp_list[i][0],
                                                                                   (((temp_list[i][0] * (9 / 5)) + 32)),
                                                                                   time.strftime('%Y-%m-%d %H:%M:%S', temp_list[i][1])) + "\n"

            summary_string += "The average temperature was: {:1.2f}C/{:1.2f}F".format(
                temp_dict['average'], (((temp_dict['average'] * (9 / 5)) + 32))) + "\n"

        return summary_string

    def summary(self):
        """Prints out a summary of the temperature readings in easy to read format.

        Includes average temperature, the number of readings,
        the maximum temperature and the minimum temperature.

        TODO: Expand Docstring

        """

        temp_dict = {}

        # first make sure all readings are up to date
        temp_list = self.temp_list
        temp_dict['average'] = self.average()
        temp_dict['minimum'] = self.minimum()
        temp_dict['maximum'] = self.maximum()
        temp_dict['count'] = self.count()
        temp_dict['start_timestamp'] = self.start_timestamp
        temp_dict['stop_timestamp'] = self.start_timestamp

        #time.strptime(temp_list[i][1], '%Y-%m-%d %H:%M:%S')

        if temp_dict['start_timestamp'] is None:
            return "The temperature tracker has not yet been started"
        else:
            summary_string = "The temperature tracker was started at: " + \
                             time.strftime('%Y-%m-%d %H:%M:%S',
                                           temp_dict['start_timestamp']) + "\n"
            summary_string += "A total of " + \
                str(temp_dict['count']) + " have been gathered\n"
            summary_string += "The readings so far are: \n"

            for i in range(0, len(self.temp_list)):
                summary_string += "\t\t" + "{:1.2f}C/{:1.2f}F at time {}\n".format(temp_list[i][0],
                                                                                   (((temp_list[i][0] * (9 / 5)) + 32)),
                                                                                   time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                                 temp_list[i][1])) + "\n"

            summary_string += "The average temperature was: {:1.2f}C/{:1.2f}F".format(temp_dict['average'], (
                ((temp_dict['average'] * (9 / 5)) + 32))) + "\n"

        return summary_string
