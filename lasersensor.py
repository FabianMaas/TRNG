import RPi.GPIO as GPIO
import os, time
import queue
import threading
import random
import models

class Lasersensor:

    q = queue.Queue()
    tmp_arr = []
    active = False
    finished = False


    # def producer(self):
    #     for i in range(10000):
    #         random_number = random.randint(0, 1)
    #         self.q.put(random_number)
    #         print("Eingefügt:", i)
    #         time.sleep(0.1)
    #         if not self.active:
    #             break


    def write_byte(self, app):
        while True:
            tmp_rand_arr = []
            #print("Size:", self.q.qsize()) 
            if (self.q.qsize() >= 8):
                tmp_rand_arr.clear()
                count = 0
                while count < 8:
                    try:
                        tmp = self.q.get()
                        tmp_rand_arr.append(tmp)
                        count += 1
                        #print("Entnommen:", tmp)
                    except:
                        pass

                tmp_string = "".join(str(x) for x in tmp_rand_arr)

                with app.app_context():
                    new_byte = models.Randbyte(value=tmp_string) 
                    models.db.session.add(new_byte)
                    models.db.session.commit()
            time.sleep(1) 
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


    def producer(self):
        RECEIVER_PIN1 = 23
        RECEIVER_PIN2 = 24
        RECEIVER_PIN3 = 18
        RECEIVER_PIN4 = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(RECEIVER_PIN1, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN1, GPIO.RISING, callback=self._callback_func1, bouncetime=50)
        
        GPIO.setup(RECEIVER_PIN2, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN2, GPIO.RISING, callback=self._callback_func2, bouncetime=50)

        GPIO.setup(RECEIVER_PIN3, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN3, GPIO.RISING, callback=self._callback_func3, bouncetime=50)

        GPIO.setup(RECEIVER_PIN4, GPIO.IN)
        GPIO.add_event_detect(RECEIVER_PIN4, GPIO.RISING, callback=self._callback_func4, bouncetime=50)

        try:
            while self.active:
                time.sleep(0.1)
        except:
            GPIO.remove_event_detect(RECEIVER_PIN1)
            GPIO.remove_event_detect(RECEIVER_PIN2)
            GPIO.remove_event_detect(RECEIVER_PIN3)
            GPIO.remove_event_detect(RECEIVER_PIN4)

    def _callback_func1(self, channel):
        if GPIO.input(channel):
            self.q.put(0)
            print("first: 0")

    def _callback_func2(self, channel):
        if GPIO.input(channel):
            self.q.put(1)
            print("first: 1")
    
    def _callback_func3(self, channel):
        if GPIO.input(channel):
            self.q.put(0)
            print("second: 0")

    def _callback_func4(self, channel):
        if GPIO.input(channel):
            self.q.put(1)
            print("second: 1")
