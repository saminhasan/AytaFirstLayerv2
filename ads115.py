import Adafruit_ADS1x15
from threading import Thread
from time import time, sleep

class ADC:
	def __init__(self, GAIN=1, data_rate=128):
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
