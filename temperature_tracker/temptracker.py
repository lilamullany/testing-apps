from gpiozero import CPUTemperature
import time


"""Update the argument list with the current CPU temperature"""
def update(list):
    cpu = CPUTemperature()
    new_reading = (cpu.temperature, time.localtime())
    list.append(new_reading)


"""Print out a summary of the temperature readings including average
temperature, the number of readings, the maximum temperature and the
time the maximum temperature reading occurred."""
def summary(list):

    # calculate average temperature
    total_temp = 0.0
    count = 0
    max_temp = 0.0
    max_temp_time = time.localtime()

    for i in range(0, len(list)):
        current_temp = list[i][0]
        total_temp = total_temp + current_temp
        count = count + 1

        # track the maximum temperature
        if current_temp > max_temp:
            max_temp = current_temp
            max_temp_time = list[i][1]

    average_temp = total_temp / count
    print("The average temperature over {} readings was {:1.2f}C/{:1.2f}F".format(count, average_temp, (((average_temp * (9/5))+32))))
    print("The maximum temperature reading was {:1.2f}C/{:1.2f}F at time {}".format(max_temp,(((max_temp * (9/5))+32)), time.strftime('%Y-%m-%d %H:%M:%S', max_temp_time)))