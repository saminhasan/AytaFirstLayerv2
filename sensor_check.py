import os
import board
import busio

gps_addr = '/dev/serial0'
mpu_addr = '0x68'
hmc_addr = '0x1e'
bmp_addr = '0x77'
adc_addr = '0x48'
oled_addr = '0x3c'

def check_sensors(verbose=False):
	sensor_health = {'gps': True, 'imu': False, 'compass': False, 'baro': False, 'adc': False, 'oled': False}
	i2c = busio.I2C(board.SCL, board.SDA)
	addresses = [hex(x) for x in i2c.scan()]
	if os.path.exists(gps_addr):
		#print("GPS connected")
		sensor_health['gps'] = True
	if mpu_addr in addresses:
		#print('IMU connected')
		sensor_health['imu'] = True
	if hmc_addr in addresses:
		#print('compass connected')
		sensor_health['compass'] = True
	if bmp_addr in addresses:
		#print('barometer connected')
		sensor_health['baro'] = True
	if adc_addr in addresses:
		#print('ADC connected')
		sensor_health['adc'] = True
	if oled_addr in addresses:
		sensor_health['oled'] = True
		#print('OLED connected')

	if len(addresses) == 5:
		if verbose:
			print("All i2c Devices connected")
	#print(sensor_health)
	return sensor_health

if __name__ == '__main__':
	sensor_status = check_sensors(True)
	print(sensor_status)
