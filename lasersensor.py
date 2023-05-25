import os, time
import random
import models
import multiprocessing
class Lasersensor:

    q = multiprocessing.Queue()
    is_running = False


    def producer(self):
        for i in range(100000):
            random_number = random.randint(0, 1)
            self.q.put(random_number)
            print("Eingefügt:", i)
            time.sleep(0.05)
            if not self.is_running:
                break


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
            if not self.is_running:
                break
            

    def setStopFlag(self):
        self.is_running = False


    def setStartFlag(self):
        self.is_running = True


    def getIsActive(self):
        return self.is_running
