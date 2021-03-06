import smbus
from threading import Thread
from time import time, sleep
from math import pi, floor, atan2

class Hmc:

	__scales = {
		0.88: [0, 0.73],
		1.30: [1, 0.92],
		1.90: [2, 1.22],
		2.50: [3, 1.52],
		4.00: [4, 2.27],
		4.70: [5, 2.56],
		5.60: [6, 3.03],
		8.10: [7, 4.35],
	}

	def __init__(self, port=1, address=0x1E, gauss=1.3, declination=(0,0)):
		self.compass_data = {'compass_timestamp' : float("NaN"),'compass_heading' : float("NaN")}
		self.bus = smbus.SMBus(port)
		self.address = address

		(degrees, minutes) = declination
		self.__declDegrees = degrees
		self.__declMinutes = minutes
		self.__declination = (degrees + minutes / 60) * pi / 180

		(reg, self.__scale) = self.__scales[gauss]
		#self.bus.write_byte_data(self.address, 0x00, 0x37)
		#self.bus.write_byte_data(self.address, 0x00, 0x6a)
		#self.bus.write_byte_data(self.address, 0x00, 0x6b)
		self.bus.write_byte_data(self.address, 0x00, 0x70) # 8 Average, 15 Hz, normal measurement
		self.bus.write_byte_data(self.address, 0x01, reg << 5) # Scale
		self.bus.write_byte_data(self.address, 0x02, 0x00) # Continuous measurement
		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def declination(self):
		return (self.__declDegrees, self.__declMinutes)

	def twos_complement(self, val, len):
		# Convert twos compliment to integer
		if (val & (1 << len - 1)):
			val = val - (1<<len)
		return val

	def __convert(self, data, offset):
		val = self.twos_complement(data[offset] << 8 | data[offset+1], 16)
		if val == -4096: return None
		return round(val * self.__scale, 4)

	def axes(self):
		data = self.bus.read_i2c_block_data(self.address, 0x00)
		#print map(hex, data)
		x = self.__convert(data, 3)
		y = self.__convert(data, 7)
		z = self.__convert(data, 5)
		return (x,y,z)

	def heading(self):
		(x, y, z) = self.axes()
		try:
			headingRad = atan2(y, x)
		except Exception:
			headingRad = 0.0
		headingRad += self.__declination

		# Correct for reversed heading
		if headingRad < 0:
			headingRad += 2 * pi

		# Check for wrap and compensate
		elif headingRad > 2 * pi:
			headingRad -= 2 * pi

		# Convert to degrees from radians
		headingDeg = headingRad * 180 / pi
		return headingDeg

	def degrees(self, headingDeg):
		degrees = floor(headingDeg)
		minutes = round((headingDeg - degrees) * 60)
		return (degrees, minutes)

	def run(self):
		while True:
			self.compass_data['compass_timestamp'] = time()
			self.compass_data['compass_heading'] = self.heading()
			sleep(0.05)

	def get_compass_heading(self):
		compass_data = self.compass_data
		#self.compass_data = {'compass_heading' : float("NaN")}
		return compass_data

	def __str__(self):
		(x, y, z) = self.axes()
		return "Axis X: " + str(x) + "\n" \
			   "Axis Y: " + str(y) + "\n" \
			   "Axis Z: " + str(z) + "\n" \
			   "Declination: " + self.degrees(self.declination()) + "\n" \
			   "Heading: " + self.degrees(self.heading()) + "\n"


if __name__ == '__main__':
	import sys
	from time import sleep
	try:
		hmc = Hmc()
		while True:
			data = hmc.get_compass_heading()
			print(data)
			sleep(1.0)
	except KeyboardInterrupt:
				print("\nUser Interrupt")
				sys.exit(0)
