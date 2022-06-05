import Adafruit_ADS1x15
from threading import Thread
from time import time, sleep

class ADC:
	def __init__(self, GAIN=2/3, data_rate=128):
		self.adc = Adafruit_ADS1x15.ADS1115()
		self.GAIN = GAIN
		self.data_rate = data_rate
		self.adc_data = {'adc_timestamp' : float("NaN"), 'A0' : float("NaN"), 'A1' : float("NaN"), 'A2' : float("NaN"), 'A3' : float("NaN")}
		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def run(self):
		while True:
			values = [0]*4
			for i in range(4):
				# Read the specified ADC channel using the previously set gain value.
				# Choose a gain of 1 for reading voltages from 0 to 4.09V.
				# Or pick a different gain to change the range of voltages that are read:
				#  - 2/3 = +/-6.144V
				#  -   1 = +/-4.096V
				#  -   2 = +/-2.048V
				#  -   4 = +/-1.024V
				#  -   8 = +/-0.512V
				#  -  16 = +/-0.256V
				# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

				#This line is calling the read_adc() function from the ADS1x15 Python library.  
				#The function takes one parameter, the channel number to read (a value of 0 to 3), 
				#and optionally a gain value (the default is 1). 
				#As a result the function will return the current ADC value of that channel.
				values[i] = self.adc.read_adc(i, gain=self.GAIN)
				# Note you can also pass in an optional data_rate parameter that controls
				# the ADC conversion time (in samples/second). Each chip has a different
				# set of allowed data rate values, see datasheet Table 9 config register
				#DR bit values.
				#values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
				# Each value will be a 12 or 16 bit signed integer value depending on the
				# ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
				# Print the ADC values.
				#print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
			self.adc_data['A0'] = values[0]
			self.adc_data['A1'] = values[1]
			self.adc_data['A2'] = values[2]
			self.adc_data['A3'] = values[3]
			self.adc_data['adc_timestamp'] = time()
			sleep(0.05)

	def read_voltage(self):
		value = self.adc.read_adc(1, gain=self.GAIN)
		v_lim = self.scale(self.GAIN, 1.0, 16.0, 4.096, 0.256)
		voltage = self.scale(value, -32768, 32767, -v_lim, v_lim)
		return voltage

	def scale(self,x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

	def get_adc_data(self):
		adc_data = self.adc_data
		return adc_data


if __name__ == '__main__':
	import sys
	try:
		adc = ADC()
		while True:
			data = adc.get_adc_data()
			print(data)
			sleep(1.0)
	except KeyboardInterrupt:
		print("\nUser Interrupt")
		sys.exit(0)

