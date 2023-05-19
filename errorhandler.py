from stepperengine import Stepperengine
import multiprocessing
from multiprocessing import Event
import time

class Errorhandler:
    
    engine_process = multiprocessing.Process()
    
    def fix_engine(self, errorEvent, engine_process: multiprocessing.Process, engine: Stepperengine):
        while True:
            time.sleep(5)
            errorEvent.wait()
            engine_process.terminate()
            time.sleep(1)
            if engine.unstuck_marbles(3):
                pass
            #fix_engine_process.start()
            #fix_engine_process.join()
            #fix_engine_process.terminate()
            errorEvent.clear()
            time.sleep(1)
            self.engine_process = multiprocessing.Process(target=engine.start)
            self.engine_process.start()    