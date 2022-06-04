from mpu6050 import Mpu
from hmc5883l import Hmc
from bmp180 import Bmp
from threading import Thread
import time

class GY88:
	def __init__(self):
		self.gy88_data = {'imu' : None, 'compass' : None, 'barometer' : None}
		self.mpu = Mpu()
		self.hmc = Hmc()
		self.bmp = Bmp()
		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def run(self):
		while True:
			self.gy88_data['imu'] = self.mpu.get_mpu_data()
			self.gy88_data['compass'] = self.hmc.get_compass_heading()
			self.gy88_data['barometer'] = self.bmp.get_barometer_data()
			time.sleep(0.1)


	def get_all_data(self):

		gy88_data = self.gy88_data
		return gy88_data


if __name__ == '__main__':
	import sys
	from time import perf_counter, sleep
	try:
		gy88 = GY88()
		while True:
			start=perf_counter()
			data = gy88.get_all_data()
			print(data)
			sleep(1.0)
			end	 = perf_counter()
			frequency =	 1.0/(end- start)
			print(" frequency : ", frequency)
			#break
	except KeyboardInterrupt:
		print("User Interrupt")
		sys.exit(0)
