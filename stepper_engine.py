from time import sleep
import RPi.GPIO as GPIO
import warnings
import multiprocessing

class StepperEngine:
	# defining constants
	__DIR = 5   # Direction GPIO Pin
	__STEP = 6  # Step GPIO Pin
	__CW = 0     # Clockwise Rotation
	#CCW = 1    # Counterclockwise Rotation (not in use)
	__SPR = 1600   # Steps per Revolution (360 / 7.5)
	__step_count = __SPR
	__delay = .0001

	def start(self, error_event):
		warnings.filterwarnings("ignore", category=RuntimeWarning)
		self.__error_event = error_event
		try:
			self.__setup()
		except Exception as e:
			pass
			#print("setup",str(e))
		try:
			self.__loop()
		except Exception as e:
			pass
			#print("loop",str(e))

	def __setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.__DIR, GPIO.OUT)
		GPIO.setup(self.__STEP, GPIO.OUT)
		GPIO.output(self.__DIR, self.__CW)

	def __loop(self):
		while True:
			if self.__error_event.is_set():
				self.unstuck_marbles(3)
				self.__error_event.clear()
			for x in range(self.__step_count):
					GPIO.output(self.__STEP, GPIO.HIGH)
					sleep(self.__delay)
					GPIO.output(self.__STEP, GPIO.LOW)
					sleep(self.__delay)

	def destroy(self):
		try:
			GPIO.output(self.__STEP, GPIO.LOW)
			GPIO.cleanup()
		except:
			pass

	def unstuck_marbles(self, rounds):
		self.destroy()
		self.__CW = 1
		self.__setup()
		for x in range(rounds):
			for y in range(self.__step_count):
					GPIO.output(self.__STEP, GPIO.HIGH)
					sleep(self.__delay)
					GPIO.output(self.__STEP, GPIO.LOW)
					sleep(self.__delay)
		self.destroy()
		self.__CW = 0
		self.__setup()