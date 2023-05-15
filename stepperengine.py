from time import sleep
import RPi.GPIO as GPIO
import warnings

class Stepperengine:
	# defining constants
	DIR = 20   # Direction GPIO Pin
	STEP = 21  # Step GPIO Pin
	CW = 1     # Clockwise Rotation
	CCW = 0    # Counterclockwise Rotation
	SPR = 1600   # Steps per Revolution (360 / 7.5)
	step_count = SPR
	delay = .0001

	def start(self):
		warnings.filterwarnings("ignore", category=RuntimeWarning)
		try:
			self.setup()
		except:
			pass
		try:
			self.loop()
		except:
			pass

	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.DIR, GPIO.OUT)
		GPIO.setup(self.STEP, GPIO.OUT)
		GPIO.output(self.DIR, self.CW)

	def loop(self):
		while True:
			for x in range(self.step_count):
					GPIO.output(self.STEP, GPIO.HIGH)
					sleep(self.delay)
					GPIO.output(self.STEP, GPIO.LOW)
					sleep(self.delay)

	def destroy(self):
		try:
			GPIO.output(self.STEP, GPIO.LOW)
			GPIO.cleanup()
		except:
			pass