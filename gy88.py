from mpu import Mpu
from hmc import Hmc
from bmp import Bmp
from threading import Thread
import time

class GY88:
	def __init__(self):
		self.gy88_data = {'imu' : None, 'compass' : None, 'barometer' : None}
		self.mpu = Mpu(0x68)
		self.hmc = Hmc()
		self.bmp = Bmp(0x77)
		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def run(self):
		while True:
			self.gy88_data['imu'] = self.mpu.get_mpu_data()
			self.gy88_data['compass'] = self.hmc.get_compass_heading()
			self.gy88_data['barometer'] = self.bmp.get_barometer_data()
			#print(self.gy88_data)
			time.sleep(0.01)

	def get_all_data(self):
		gy88_data = self.gy88_data
		self.gy88_data = {'imu' : None, 'compass' : None, 'barometer' : None}
		#print(gy88_data)
		return gy88_data


if __name__ == '__main__':
	from time import perf_counter, sleep
	try:
		#mpu = Mpu(0x68)
		# http://magnetic-declination.com/Great%20Britain%20(UK)/Harrogate#
		#hmc = Hmc(gauss = 4.7, declination = (-2,5))
		#bmp = Bmp(0x77)
		gy88 = GY88()
		while True:
			start=perf_counter()
			#print("IMU (ax, ay, az), (gx, gy, gz) : ", mpu.get_all_data())
			#print("Compass (Mintue, Second): " , str(hmc.degrees(hmc.heading())))
			#print("Barometer (Temperature, Pressure, Altitude) : ",  bmp.get_temp(),  bmp.get_pressure(),bmp.get_altitude())
			data = gy88.get_all_data()
			print(data)
			sleep(1.0)
			end  = perf_counter()
			frequency =  1.0/(end- start)
			#print(" frequency : ", frequency)
			#break
	except KeyboardInterrupt:
		print("User Interrupt")
		exit()
