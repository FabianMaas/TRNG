from time import sleep
import RPi.GPIO as GPIO
import warnings
from multiprocessing import Event

class StepperEngine:
	__DIR = 5   # Direction GPIO Pin
	__STEP = 6  # Step GPIO Pin
	__CW = 0     # Clockwise Rotation
	#CCW = 1    # Counterclockwise Rotation (not in use)
	__step_count = 1600   # Steps per Revolution
	__delay = .0001	# Turning speed

	def start(self, error_event: Event):
		"""
		Starts the whole process with setting up the GPIO and
		runs the engine until the reset functions gets called.

		Params:
		- error_event: a object of the type Event from multiprocessing library
		"""
		warnings.filterwarnings("ignore", category=RuntimeWarning)
		self.__error_event = error_event
		try:
			self.__setup()
		except Exception as e:
			print("EXCEPTION from engine setup: " + str(e))
			pass
		try:
			self.__loop()
		except Exception as e:
			print("EXCEPTION from engine loop: " + str(e))
			pass

	def __setup(self):
		"""
		Sets up the physical location of the GPIO pins
		and their behavior. 
		"""
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.__DIR, GPIO.OUT)
		GPIO.setup(self.__STEP, GPIO.OUT)
		GPIO.output(self.__DIR, self.__CW)

	def __loop(self):
		"""
		Starts the whole process with setting up the GPIO and
		runs the engine until the reset functions gets called.

		Params:
		- error_event: a object of the type Event from multiprocessing library
		"""
		while True:
			#print("Resetter:"+ str(self.__error_event.is_set()))
			if self.__error_event.is_set():
				self.unstuck_marbles(5)
				self.__error_event.clear()
			for x in range(self.__step_count):
					GPIO.output(self.__STEP, GPIO.HIGH)
					sleep(self.__delay)
					GPIO.output(self.__STEP, GPIO.LOW)
					sleep(self.__delay)

	def reset(self):
		"""
		The endless run of the engine will be reseted with a call of this function.
		"""
		try:
			GPIO.output(self.__STEP, GPIO.LOW)
			GPIO.cleanup()
		except:
			pass

	def unstuck_marbles(self, rounds):
		"""
		If there are marbles stuck in front of the lift
		call this function to let the engine spin backwards for x rounds.

		Params:
		- rounds: An integer to tell how many rounds the engine will be spinning backwards.
		"""
		self.reset()
		self.__CW = 1
		self.__setup()
		for x in range(rounds):
			for y in range(self.__step_count):
					GPIO.output(self.__STEP, GPIO.HIGH)
					sleep(self.__delay)
					GPIO.output(self.__STEP, GPIO.LOW)
					sleep(self.__delay)
		self.reset()
		self.__CW = 0
		self.__setup()