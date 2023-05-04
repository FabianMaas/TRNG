#import RPi.GPIO as GPIO
import os, time
import queue
import threading
import random

class Lasersensor:

    q = queue.Queue()
    tmp_arr = []
    active = False
    finished = False


    def consumer(self,numBits):
        while True:
            print("Size:", self.q.qsize()) 
            if (self.q.qsize() >= numBits):
                self.tmp_arr.clear()
                count = 0
                while count < numBits:
                    try:
                        tmp = self.q.get()
                        self.tmp_arr.append(tmp)
                        count += 1
                        print("Entnommen:", tmp)
                    except:
                        pass
                self.finished = True
                break
            time.sleep(1) 


    def producer(self):
        for i in range(10000):
            random_number = random.randint(0, 1)
            self.q.put(random_number)
            print("Eingefügt:", i)
            time.sleep(0.1)
            if not self.active:
                break


    def getCurrentRandomArr(self):
        return self.tmp_arr

    def setStopFlag(self):
        self.active = False

    def setStartFlag(self):
        self.active = True

    def getIsActive(self):
        return self.active
    
    def getFinished(self):
        return self.finished

    def setNotFinished(self):
        self.finished = False


    # def producer(self):
    #     RECEIVER_PIN1 = 23
    #     RECEIVER_PIN2 = 24
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setwarnings(False)
        
    #     GPIO.setup(RECEIVER_PIN1, GPIO.IN)
    #     GPIO.add_event_detect(RECEIVER_PIN1, GPIO.RISING, callback=self._callback_func1, bouncetime=200)
        
    #     GPIO.setup(RECEIVER_PIN2, GPIO.IN)
    #     GPIO.add_event_detect(RECEIVER_PIN1, GPIO.RISING, callback=self._callback_func2, bouncetime=200)

    #     try:
    #         while self.active:
    #             time.sleep(0.1)
    #     except:
    #         GPIO.remove_event_detect(RECEIVER_PIN1)
    #         GPIO.remove_event_detect(RECEIVER_PIN2)

    
    # def _callback_func1(self, channel):
    #     if GPIO.input(channel):
    #         self.q.put(0)
    #         print("Eingefügt: 0")

    # def _callback_func2(self, channel):
    #     if GPIO.input(channel):
    #         self.q.put(1)
    #         print("Eingefügt: 1")
