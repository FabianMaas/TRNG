"""
This file provides the LaserSensor class for controlling a laser sensor using Raspberry Pi GPIO pins.

The LaserSensor class allows reading sensor data, writing data to a database, and managing event-based callbacks for sensor events. 
It utilizes the RPi.GPIO library for GPIO pin manipulation, the time library for delays and timing calculations, 
the datetime library for time-based operations, the random library for generating random bits, 
the models module for interacting with the database, and the multiprocessing library for event handling.

Imports:
- datetime: Provides classes for manipulating dates and times.
- models: Contains the data models for the application.
- multiprocessing: Supports the execution of multiple processes in parallel.
- os: Provides a way of using operating system-dependent functionality.
- random: Generates random numbers and provides random selection functionality.
- RPi.GPIO: Allows control of Raspberry Pi GPIO pins.
- time: Provides various time-related functions.

Classes:
- LaserSensor: Controls a laser sensor and manages data reading and writing.
"""


import datetime
import models.models as models
import multiprocessing
import os
import random
import RPi.GPIO as GPIO
import time


class LaserSensor:
    """
    Represents a laser sensor controlled using Raspberry Pi GPIO pins.\n
    Attributes:
    - __queue_top (multiprocessing.Queue): A queue for storing data from the top laser sensor.
    - __queue_bottom (multiprocessing.Queue): A queue for storing data from the bottom laser sensor.
    - __top_down (bool): A flag indicating if the top laser sensor is currently down.
    - __bottom_down (bool): A flag indicating if the bottom laser sensor is currently down.
    - __list_top (list): A list for tracking data from the top laser sensor.
    - __list_bottom (list): A list for tracking data from the bottom laser sensor.\n
    Methods:
    - start(self): Starts the sensor and begins monitoring the queues.
    - write_to_db(self, rest_api, error_event: multiprocessing.Event): Constantly checks the data queues and writes to the database when the queue reaches 8 bits.
    - __loop(self): Main loop for monitoring the laser sensors.
    - __callback_func1(self, channel): Callback function for handling events from the first laser sensor.
    - __callback_func2(self, channel): Callback function for handling events from the second laser sensor.
    - __callback_func3(self, channel): Callback function for handling events from the third laser sensor.
    - __callback_func4(self, channel): Callback function for handling events from the fourth laser sensor.
    - __add_time_based_random_bits(self, queue): Adds time-based random bits to the specified queue.
    """
    __queue_top = multiprocessing.Queue()
    __queue_bottom = multiprocessing.Queue()
    __top_down = multiprocessing.Event
    __bottom_down = multiprocessing.Event
    __list_top = []
    __list_bottom = []


    def start(self):
        """
        Starts the laser sensor and begins monitoring the queues.\n
        Parameters:
        - self: The current instance of the class.
        """
        try:
            self.__loop()
        except Exception as e:
            print("EXCEPTION from queue loop: " + str(e))
            pass


    def write_to_db(self, rest_api, error_event: multiprocessing.Event):
        """
        Checks the data queues constantly and writes to the db,
        if the queue reaches 8 Bit.\n
        Parameters:
        - self: The current instance of the class.
        - rest_api is an flask instance object.
        - error_event is an object of the type Event from multiprocessing library.
        """
        last_executed_time = datetime.datetime.now()
        while True:
            current_time = datetime.datetime.now()
            difference = current_time - last_executed_time
            datetime.timedelta(0, 4, 316543)
            
            """
            if no bits going to be generated within 15 seconds an error object will be set to true.
            The error object is needed to let the engine turn backwards to fix stuck marbles.
            """
            if difference.total_seconds() > 15:
                error_event.set()               
                last_executed_time = datetime.datetime.now()
            

            print("Bottom queue size: " + str(self.__queue_bottom.qsize()))
            print("Top queue size: " + str(self.__queue_top.qsize()))
            #print("Bottom down: " + str(self.__bottom_down.is_set()))
            #print("Top down: " + str(self.__top_down.is_set()))


            tmp_rand_arr = []

            if ((self.__queue_top.qsize() >= 8 and not self.__top_down.is_set()) or (self.__queue_bottom.qsize() >= 8 and not self.__bottom_down.is_set())):
                tmp_rand_arr.clear()

                if (not self.__bottom_down.is_set()) and self.__queue_bottom.qsize() > self.__queue_top.qsize():
                    print("first if---------------------------------")
                    count = 0
                    while (not self.__bottom_down.is_set()) and count < 8:
                        try:
                            tmp = self.__queue_bottom.get()
                            tmp_rand_arr.append(tmp)
                            self.__list_bottom.append(tmp)

                            if len(self.__list_bottom) >= 32:
                                print("DEBUG bottom-list: " + str(self.__list_bottom))
                                if self.__list_bottom.count(0) > 30 or self.__list_bottom.count(1) > 30:
                                    self.__bottom_down.set() 
                                    continue

                                self.__list_bottom.pop(0)

                            count += 1
                        except Exception as e:
                            print("EXCEPTION from top queue write: " + str(e))
                            pass    
                elif (not self.__top_down.is_set()) and self.__queue_top.qsize() > self.__queue_bottom.qsize():
                    print("second if---------------------------------")
                    count = 0
                    while (not self.__top_down.is_set()) and count < 8:
                        try:
                            tmp = self.__queue_top.get()
                            tmp_rand_arr.append(tmp)
                            self.__list_top.append(tmp)
                            
                            if len(self.__list_top) >= 32:
                                print("DEBUG top-list: " + str(self.__list_top))
                                if self.__list_top.count(0) > 30 or self.__list_top.count(1) > 30:
                                    self.__top_down.set()
                                    continue

                                self.__list_top.pop(0)

                            count += 1
                        except Exception as e:
                            print("EXCEPTION from top queue write: " + str(e))
                            pass

                tmp_string = "".join(str(x) for x in tmp_rand_arr)
                if len(tmp_string) != 0:
                    with rest_api.app_context():
                        new_byte = models.Randbyte(value=tmp_string) 
                        models.db.session.add(new_byte)
                        models.db.session.commit()
                    last_executed_time = datetime.datetime.now()
            
            time.sleep(1) 


    def __loop(self):
        """
        Main loop for monitoring the laser sensors.\n
        This function sets up GPIO pins for receiving signals from the laser sensors and adds event detection callbacks.
        It continuously runs in a loop, checking the status of the laser sensors and removing event detection as needed.
        The loop also includes a sleep period of 0.1 seconds between iterations.\n
        Parameters:
        - self: The current instance of the class.\n
        Pin Configuration:
        - RECEIVER_PIN1: GPIO pin 19
        - RECEIVER_PIN2: GPIO pin 13
        - RECEIVER_PIN3: GPIO pin 26
        - RECEIVER_PIN4: GPIO pin 12\n
        Callback Functions:
        - __callback_func1: Callback function for handling events from the first laser sensor.
        - __callback_func2: Callback function for handling events from the second laser sensor.
        - __callback_func3: Callback function for handling events from the third laser sensor.
        - __callback_func4: Callback function for handling events from the fourth laser sensor.
        """
        RECEIVER_PIN1 = 19
        RECEIVER_PIN2 = 13
        RECEIVER_PIN3 = 26
        RECEIVER_PIN4 = 12

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(RECEIVER_PIN1, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN1, GPIO.RISING, callback=self.__callback_func1, bouncetime=50)
        
        GPIO.setup(RECEIVER_PIN2, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN2, GPIO.RISING, callback=self.__callback_func2, bouncetime=50)

        GPIO.setup(RECEIVER_PIN3, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN3, GPIO.RISING, callback=self.__callback_func3, bouncetime=50)

        GPIO.setup(RECEIVER_PIN4, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN4, GPIO.RISING, callback=self.__callback_func4, bouncetime=50)

        try:
            while True:

                if(self.__top_down.is_set()):
                    GPIO.remove_event_detect(RECEIVER_PIN1)
                    GPIO.remove_event_detect(RECEIVER_PIN2)

                if(self.__bottom_down.is_set()):
                    GPIO.remove_event_detect(RECEIVER_PIN3)
                    GPIO.remove_event_detect(RECEIVER_PIN4)
                    
                time.sleep(0.1)
        except:
            GPIO.remove_event_detect(RECEIVER_PIN1)
            GPIO.remove_event_detect(RECEIVER_PIN2)
            GPIO.remove_event_detect(RECEIVER_PIN3)
            GPIO.remove_event_detect(RECEIVER_PIN4)


    def __callback_func1(self, channel):
        """
        Callback function for handling events from the first laser sensor.\n
        This function is called when a rising edge event is detected on the specified channel.
        It checks the status of the laser sensor and adds the corresponding value to the top laser sensor queue.
        Optionally, additional time-based random bits can be added using the __add_time_based_random_bits function.
        It also prints a message indicating the value added to the queue.\n
        Parameters:
        - self: The current instance of the class.\n
        - channel: The GPIO channel on which the event was detected.
        """
        if GPIO.input(channel):
            if(not self.__top_down.is_set()):
                self.__queue_top.put(0)
                # optional more bits with additional time factor
                # self.__add_time_based_random_bits(self.__queue_top)
                print("first: 0")         


    def __callback_func2(self, channel):
        """
        Callback function for handling events from the second laser sensor.\n
        This function is called when a rising edge event is detected on the specified channel.
        It checks the status of the laser sensor and adds the corresponding value to the top laser sensor queue.
        Optionally, additional time-based random bits can be added using the __add_time_based_random_bits function.
        It also prints a message indicating the value added to the queue.\n
        Parameters:
        - self: The current instance of the class.\n
        - channel: The GPIO channel on which the event was detected.
        """
        if GPIO.input(channel):
            if(not self.__top_down.is_set()):
                self.__queue_top.put(1)
                # optional more bits with additional time factor
                # self.__add_time_based_random_bits(self.__queue_top)
                print("first: 1")
    
    
    def __callback_func3(self, channel):
        """
        Callback function for handling events from the third laser sensor.\n
        This function is called when a rising edge event is detected on the specified channel.
        It checks the status of the laser sensor and adds the corresponding value to the bottom laser sensor queue.
        Optionally, additional time-based random bits can be added using the __add_time_based_random_bits function.
        It also prints a message indicating the value added to the queue.\n
        Parameters:
        - self: The current instance of the class.\n
        - channel: The GPIO channel on which the event was detected.
        """
        if GPIO.input(channel):
            if(not self.__bottom_down.is_set()):
                self.__queue_bottom.put(0)
                # optional more bits with additional time factor
                # self.__add_time_based_random_bits(self.__queue_bottom)
                print("second: 0")


    def __callback_func4(self, channel):
        """
        Callback function for handling events from the third laser sensor.\n
        This function is called when a rising edge event is detected on the specified channel.
        It checks the status of the laser sensor and adds the corresponding value to the bottom laser sensor queue.
        Optionally, additional time-based random bits can be added using the __add_time_based_random_bits function.
        It also prints a message indicating the value added to the queue.\n
        Parameters:
        - self: The current instance of the class.\n
        - channel: The GPIO channel on which the event was detected.
        """
        if GPIO.input(channel):
            if(not self.__bottom_down.is_set()):
                self.__queue_bottom.put(1)
                # optional more bits with additional time factor
                # self.__add_time_based_random_bits(self.__queue_bottom)
                print("second: 1")


    def __add_time_based_random_bits(self, queue):
        """
        Adds time-based random bits to the specified queue.\n
        This function generates random bits based on the current microsecond value and adds them to the given queue.
        It retrieves the microsecond value using the datetime module, converts it to a binary string, and extracts the last two digits.
        It then iterates over each bit in the extracted string and adds it to the queue.\n
        Parameters:
        - self: The current instance of the class.\n
        - queue: The queue to which the random bits will be added.
        """
        microsecond = bin(datetime.datetime.now().microsecond)
        bits = microsecond[len(microsecond)-2:]
        for bit in bits:
            queue.put(bit)