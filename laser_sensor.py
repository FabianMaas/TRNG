import RPi.GPIO as GPIO
import os, time, datetime
import random
import models
import multiprocessing


class LaserSensor:

    __queue_top = multiprocessing.Queue()
    __queue_bottom = multiprocessing.Queue()
    __is_running = False
    __top_down = False
    __bottom_down = False
    __list_top = []
    __list_bottom = []

    def write_to_db(self, rest_api, error_event: multiprocessing.Event):
        """
        Checks the data queues constantly and writes to the db,
        if the queue reaches 8 Bit.

        Params: 
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
            print("Bottom down: " + str(self.__bottom_down))
            print("Top down: " + str(self.__top_down))


            tmp_rand_arr = []

            if ((self.__queue_top.qsize() >= 8 and not self.__top_down) or (self.__queue_bottom.qsize() >= 8 and not self.__bottom_down)):
                tmp_rand_arr.clear()

                if (not self.__bottom_down) and self.__queue_bottom.qsize() > self.__queue_top.qsize():
                    count = 0
                    while (not self.__list_bottom) and count < 8:
                        try:
                            tmp = self.__queue_bottom.get()
                            tmp_rand_arr.append(tmp)
                            self.__list_bottom.append(tmp)

                            if len(self.__list_bottom) >= 32:
                                print("DEBUG bottom-list: " + str(self.__list_bottom))
                                if self.__list_bottom.count(0) > 30 or self.__list_bottom.count(1) > 30:
                                    self.__bottom_down = True   
                                    continue

                                self.__list_bottom.pop(0)

                            count += 1
                        except Exception as e:
                            print("EXCEPTION from top queue write: " + str(e))
                            pass    
                elif (not self.__top_down) and self.__queue_top.qsize() > self.__queue_bottom.qsize():
                    count = 0
                    while (not self.__list_bottom) and count < 8:
                        try:
                            tmp = self.__queue_top.get()
                            tmp_rand_arr.append(tmp)
                            self.__list_top.append(tmp)
                            
                            if len(self.__list_top) >= 32:
                                print("DEBUG top-list: " + str(self.__list_top))
                                if self.__list_top.count(0) > 30 or self.__list_top.count(1) > 30:
                                    self.__top_down = True  
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
            if not self.__is_running:
                break

    def setStopFlag(self):
        self.__is_running = False

    def setStartFlag(self):
        self.__is_running = True

    def getIsActive(self):
        return self.__is_running

    def start(self):
        try:
            self.__loop()
        except Exception as e:
            print("EXCEPTION from queue loop: " + str(e))
            pass


    def __loop(self):
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
            while self.__is_running:

                if(self.__top_down):
                    GPIO.remove_event_detect(RECEIVER_PIN1)
                    GPIO.remove_event_detect(RECEIVER_PIN2)

                if(self.__bottom_down):
                    GPIO.remove_event_detect(RECEIVER_PIN3)
                    GPIO.remove_event_detect(RECEIVER_PIN4)
                    
                time.sleep(0.1)
        except:
            GPIO.remove_event_detect(RECEIVER_PIN1)
            GPIO.remove_event_detect(RECEIVER_PIN2)
            GPIO.remove_event_detect(RECEIVER_PIN3)
            GPIO.remove_event_detect(RECEIVER_PIN4)


    def __callback_func1(self, channel):
        if GPIO.input(channel):
            if(not self.__top_down):
                self.__queue_top.put(0)
                '''
                microsecond = bin(datetime.datetime.now().microsecond)
                bits = microsecond[len(microsecond)-2:]
                for bit in bits:
                    self.__queue_top.put(bit)
                '''
                print("first: 0")         

    def __callback_func2(self, channel):
        if GPIO.input(channel):
            if(not self.__top_down):
                self.__queue_top.put(1)
                '''
                microsecond = bin(datetime.datetime.now().microsecond)
                bits = microsecond[len(microsecond)-2:]
                for bit in bits:
                    self.__queue_top.put(bit)
                '''
                print("first: 1")
    
    def __callback_func3(self, channel):
        if GPIO.input(channel):
            if(not self.__bottom_down):
                self.__queue_bottom.put(0)
                '''
                microsecond = bin(datetime.datetime.now().microsecond)
                
                bits = microsecond[len(microsecond)-2:]
                for bit in bits:
                    self.__queue_bottom.put(bit)
                '''
                print("second: 0")

    def __callback_func4(self, channel):
        if GPIO.input(channel):
            if(not self.__bottom_down):
                self.__queue_bottom.put(1)
                '''
                microsecond = bin(datetime.datetime.now().microsecond)
                bits = microsecond[len(microsecond)-2:]
                for bit in bits:
                    self.__queue_bottom.put(bit)
                '''
                print("second: 1")