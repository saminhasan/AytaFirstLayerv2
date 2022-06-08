#!/usr/bin/env python3
import os
import sys
import socket
import pandas as pd
from gy88 import GY88
from neo6m import GPS
from ads115 import ADC
from ssd1306 import OLED
from threading import Thread
from datetime import datetime
from utils import get_ip, check_sensors
from time import time,sleep, perf_counter


class Recorder:
	def __init__(self):
		self.path = os.getcwd()
		self.log_path = self.path + '/Data/'
		print("Application started")
		self.record = False
		self.gy88 = GY88()
		self.neo6m = GPS()
		self.adc = ADC()
		self.oled = OLED()
		self.update_oled()
		self.logging_frequency = 5.0 # Hz
		self.logging_period = 1.0 / self.logging_frequency # s
		self.init_log()
		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def init_log(self):
		self.data_log = {
		'timestamp':[], 'gps_timestamp': [],  'latitude': [], 'latitude_error': [], 'longitude': [], 'longitude_error': [], 'altitude': [], 'altitude_error': [],
		'velocity': [], 'velocity_error': [],  'heading': [], 'heading_error': [], 'magnetic_declination': [], 'nsat': [],
		'imu_timestamp': [], 'ax': [], 'ay': [], 'az': [], 'gx': [], 'gy': [], 'gz': [],
		'compass_timestamp': [], 'compass_heading': [],
		'barometer_timestamp': [], 'temperature': [], 'pressure': [], 'barometer_altitude': [],
		'adc_timestamp': [], 'A0': [], 'A1': [], 'A2': [], 'A3': [],
		'heart_rate' : [], 'battery_voltage' : []
		}

	def start(self):
		self.record = True
		return {'status':'started'}

	def stop(self, save_log=True):
		self.record = False
		data_log = self.data_log
		dataframe = pd.DataFrame([data_log])
		now = datetime.now()
		dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
		if save_log:
			dataframe.to_csv(self.log_path + dt_string + '.csv', index=False,header=True)
		self.init_log()
		return data_log

	def run(self):
		previous_timestamp = 0.0
		oled_timer = 0.0
		while True:
			timestamp = perf_counter()
			if (timestamp - oled_timer) > 0.5:
				self.update_oled()
				oled_timer = timestamp
			if (timestamp - previous_timestamp) > self.logging_period:
				if self.record:
					self.log_data()
			sleep(0.02)
			previous_timestamp = timestamp

	def log_data(self):
		self.data_log['timestamp'].append (time())
		gps_data = self.neo6m.get_gps_data()
		#print(gps_data)
		gy88_data = self.gy88.get_all_data()
		#print(gy88_data)
		adc_data = self.adc.get_adc_data()
		#print(adc_data)
		battery_voltage = self.calc_battery_voltage()
		BPM = self.calc_bpm(adc_data['A0'])
		self.data_log['gps_timestamp'].append (gps_data['gps_timestamp'])
		self.data_log['latitude'].append (gps_data['latitude'])
		self.data_log['latitude_error'].append (gps_data['latitude_error'])
		self.data_log['longitude'].append (gps_data['longitude'])
		self.data_log['longitude_error'].append (gps_data['longitude_error'])
		self.data_log['altitude'].append (gps_data['altitude'])
		self.data_log['altitude_error'].append (gps_data['altitude_error'])
		self.data_log['velocity'].append (gps_data['velocity'])
		self.data_log['velocity_error'].append (gps_data['velocity_error'])
		self.data_log['heading'].append (gps_data['heading'])
		self.data_log['heading_error'].append (gps_data['heading_error'])
		self.data_log['magnetic_declination'].append (gps_data['magnetic_declination'])
		self.data_log['nsat'].append (gps_data['nsat'])
		self.data_log['imu_timestamp'].append (gy88_data['imu']['imu_timestamp'])
		self.data_log['ax'].append (gy88_data['imu']['ax'])
		self.data_log['ay'].append (gy88_data['imu']['ay'])
		self.data_log['az'].append (gy88_data['imu']['az'])
		self.data_log['gx'].append (gy88_data['imu']['gx'])
		self.data_log['gy'].append (gy88_data['imu']['gy'])
		self.data_log['gz'].append (gy88_data['imu']['gz'])
		self.data_log['compass_timestamp'].append (gy88_data['compass']['compass_timestamp'])
		self.data_log['compass_heading'].append (gy88_data['compass']['compass_heading'])
		self.data_log['barometer_timestamp'].append (gy88_data['barometer']['barometer_timestamp'])
		self.data_log['temperature'].append (gy88_data['barometer']['temperature'])
		self.data_log['pressure'].append (gy88_data['barometer']['pressure'])
		self.data_log['barometer_altitude'].append (gy88_data['barometer']['barometer_altitude'])
		self.data_log['adc_timestamp'].append (adc_data['adc_timestamp'])
		self.data_log['A0'].append (adc_data['A0'])
		self.data_log['A1'].append (adc_data['A1'])
		self.data_log['A2'].append (adc_data['A2'])
		self.data_log['A3'].append (adc_data['A3'])
		self.data_log['battery_voltage'].append (battery_voltage)
		self.data_log['heart_rate'].append (BPM)

	def update_oled(self):
		#  TODO : add wlan mode info
		ip_addr = "IP : " + str(get_ip())

		network_status = ""
		if '192.168.' in ip_addr:
			network_status = "Device Connected"
		elif '10.41.0.1' in ip_addr:
			network_status = "SSID : commitup-371"
		elif '127.0.0.1' in ip_addr:
			network_status = "Switching Wlan mode"
		adc_data = self.adc.get_adc_data()
		battery_voltage = str(self.calc_battery_voltage())
		heart_rate = str(self.calc_bpm(adc_data['A0']))

		data3 = "Batt:" + battery_voltage + ' ' + " BPM:" + heart_rate
		recording_status = str('State:Idle')
		if self.record:
			recording_status = str('State:Rec ')
		#print(recording_status)
		#  TODO : add faulty sensor info
		sensor_flag = all(value == True for value in check_sensors().values())
		if sensor_flag:
			sensor_stauts = " Log:" + str('OK')
		else:
			sensor_stauts = " Log:" + str('Flt')
		data4 = str(recording_status + sensor_stauts)
		#print(data4)
		self.oled.display_data = {'1': ip_addr, '2': network_status, '3': data4, '4': data3}
		self.oled.show_data()

	def calc_bpm(self, A0):

		## TODO :place holder for bpm calculation code
		return A0

	def calc_battery_voltage(self):
		## TODO :place holder for battery_voltage calculation code
		#print('calc_battery_voltage')
		return round(self.adc.read_voltage(), 2)


if __name__ == '__main__':
	print(__file__)
	r = Recorder()
	sleep(5.0)
	start_time = time()
	try:
		print(r.start())
		while True:
			sleep(1.0)
			if (time() - start_time) > 3000000000000.0:
				break
			else:
				pass
		r.oled.clear_oled()
		r.stop(save_log=False)
	except KeyboardInterrupt:
		r.oled.clear_oled()
		print(r.stop())
		sys.exit(0)
