"""
This file controls a stepper motor using Raspberry Pi GPIO pins.

It provides the StepperEngine class, which allows starting, stopping, and controlling the motor's rotation. 
The class utilizes the RPi.GPIO library for GPIO pin manipulation and the multiprocessing library for event handling.

Imports:
- multiprocessing.Event: Provides event-based communication between processes.
- RPi.GPIO: Provides access to the Raspberry Pi's GPIO pins for controlling the motor.
- time: Provides sleep functionality for controlling the delay between motor steps.
- warnings: Allows filtering and ignoring runtime warnings.

Classes:
- StepperEngine: Controls the stepper motor and handles its rotation.
"""


from multiprocessing import Event
import RPi.GPIO as GPIO
from time import sleep
import warnings


class StepperEngine:
	"""
	The StepperEngine class controls a stepper motor using Raspberry Pi GPIO pins.\n
	Attributes:
	- __DIR (int): The GPIO pin number for the direction of rotation.
	- __STEP (int): The GPIO pin number for the step signal.
	- __CW (int): The value representing clockwise rotation.
	- __step_count (int): The number of steps per revolution.
	- __delay (float): The delay between steps, controlling the turning speed.\n
	Methods:
	- start(self, error_event: Event): Starts the engine and runs it until termination.
 	- reset(self): Resets the engine's operation.
	- __setup(self): Sets up the GPIO pins and their behavior.
	- __loop(self): Executes a loop that continuously rotates the motor in a forward direction.
	- __reverse_engine(self, rounds): Spins the engine backwards for a specified number of rounds.
	"""
	__DIR = 5   # Direction GPIO Pin
	__STEP = 6  # Step GPIO Pin
	__CW = 0     # Clockwise Rotation
	#CCW = 1    # Counterclockwise Rotation (not in use)
	__step_count = 1600   # Steps per Revolution
	__delay = .0001	# Turning speed


	def start(self, error_event: Event):
		"""
		Starts the whole process with setting up the GPIO Pins and
		runs the engine until the engine process gets terminated.\n
		Parameters:
  		- self: The current instance of the class.
		- error_event: a object of the type Event from multiprocessing library
		"""
		warnings.filterwarnings("ignore", category=RuntimeWarning)
		self.__error_event = error_event
		
		try:
			self.__reset()
		except Exception as e:
			print("EXCEPTION from engine reset: " + str(e))
			pass
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


	def __reset(self):
		"""
		The endless run of the engine will be reseted with a call of this function.\n
  		Parameters:
		- self: The current instance of the class.
		"""
		try:
			GPIO.output(self.__STEP, GPIO.LOW)
			GPIO.cleanup()
		except:
			pass


	def __setup(self):
		"""
		Sets up the physical location of the GPIO pins
		and their behavior.\n
		Parameters:
		- self: The current instance of the class.
		"""
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.__DIR, GPIO.OUT)
		GPIO.setup(self.__STEP, GPIO.OUT)
		GPIO.output(self.__DIR, self.__CW)


	def __loop(self):
		"""
		Executes a loop that continuously rotates a motor in a forward direction,
		while monitoring for any error events. If an error event is detected, the motor
		is reversed for a specified duration and the error event is cleared.\n
		Parameters:
		- self: The current instance of the class.
		"""
		while True:
			if self.__error_event.is_set():
				self.__reverse_engine(5)
				self.__error_event.clear()
			for x in range(self.__step_count):
					GPIO.output(self.__STEP, GPIO.HIGH)
					sleep(self.__delay)
					GPIO.output(self.__STEP, GPIO.LOW)
					sleep(self.__delay)


	def __reverse_engine(self, rounds):
		"""
		If there are marbles stuck in front of the lift
		call this function to let the engine spin backwards for x rounds.\n
		Parameters:
  		- self: The current instance of the class.
		- rounds: An integer to tell how many rounds the engine will be spinning backwards.
		"""
		self.__reset()
		self.__CW = 1
		self.__setup()
		for x in range(rounds):
			for y in range(self.__step_count):
					GPIO.output(self.__STEP, GPIO.HIGH)
					sleep(self.__delay)
					GPIO.output(self.__STEP, GPIO.LOW)
					sleep(self.__delay)
		self.__reset()
		self.__CW = 0
		self.__setup()