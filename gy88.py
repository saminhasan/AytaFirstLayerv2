from mpu import Mpu
from hmc import Hmc
from bmp import Bmp
import time
class GY88:
	def __init__(self):
		self.mpu = Mpu(0x68)
		# http://magnetic-declination.com/Great%20Britain%20(UK)/Harrogate#
		self.hmc = Hmc(gauss = 4.7, declination = (-2,5))
		self.bmp = Bmp(0x77)
		self.start = time.perf_counter()
	def get_all_data(self):
		return[self.mpu.get_all_data(), self.hmc.heading(), self.bmp.get_all_data()]

if __name__ == '__main__':
	timer = []
	start = time.time()
	try:
		#mpu = Mpu(0x68)
		# http://magnetic-declination.com/Great%20Britain%20(UK)/Harrogate#
		#hmc = Hmc(gauss = 4.7, declination = (-2,5))
		#bmp = Bmp(0x77)
		gy88 = GY88()
		while True:
			start=time.perf_counter()
			#print("IMU (ax, ay, az), (gx, gy, gz) : ", mpu.get_all_data())
			#print("Compass (Mintue, Second): " , str(hmc.degrees(hmc.heading())))
			#print("Barometer (Temperature, Pressure, Altitude) : ",  bmp.get_temp(),  bmp.get_pressure(),bmp.get_altitude())
			print(gy88.get_all_data())
			end  = time.perf_counter()
			print(" frequency : ", 1.0/(end- start))
			timer.append(end- start)
	except KeyboardInterrupt:
		print("User Interrupt")
		print(timer)
		exit()
