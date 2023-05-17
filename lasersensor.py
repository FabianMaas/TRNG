import RPi.GPIO as GPIO
import os, time
import random
import models
import multiprocessing
class Lasersensor:

    q = multiprocessing.Queue()
    is_running = False

    # def producer(self):
    #     for i in range(10000):
    #         random_number = random.randint(0, 1)
    #         self.q.put(random_number)
    #         print("Eingefügt:", i)
    #         time.sleep(0.1)
    #         if not self.active:
    #             break


    def write_to_db(self, app):
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
            

    def setStopFlag(self):
        self.is_running = False

    def setStartFlag(self):
        self.is_running = True

    def getIsActive(self):
        return self.is_running

    def start(self):
        try:
            self.loop()
        except:
            pass

    # namen ändern in loop()
    def loop(self):
        RECEIVER_PIN1 = 19
        RECEIVER_PIN2 = 13
        RECEIVER_PIN3 = 26
        RECEIVER_PIN4 = 12

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
            while self.is_running:
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
