#!/usr/bin/env python3
import os
import time
from gps import*
import threading
import pandas as pd
from datetime import datetime
class Recorder:
	def __init__ (self):
		self.gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
		self.data = {'latitude':[], 'longitude':[], 'altitude':[], 'velocity':[], 'heading':[], 'time':[], 'latitude_error':[], 'longitude_error':[], 'altitude_error':[], 'velocity_error':[], 'heading_error':[],}
		self.path = os.getcwd()
		self.log_path = self.path + '/Data/'
		print("Application started")
		self.record = False
		self.thread = threading.Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()


	def start(self):
		self.record = True
		return {'status':'started'}


	def run(self):
		while True:
			print(f' State : {self.record},  Time = {time.time()}',end='\r')
			nx = self.gpsd.next()
			# https://gpsd.gitlab.io/gpsd/gpsd_json.html
			if nx['class'] == 'TPV':
				latitude = getattr(nx,'lat', float("NaN"))
				latitude_error = getattr(nx,'epx', float("NaN"))

				longitude = getattr(nx,'lon', float("NaN"))
				longitude_error = getattr(nx,'epy', float("NaN"))

				altitude = getattr(nx,'alt', float("NaN"))
				altitude_error = getattr(nx,'epv', float("NaN"))

				velocity = getattr(nx,'speed', float("NaN"))
				velocity_error = getattr(nx,'eps', float("NaN"))

				heading = getattr(nx,'track', float("NaN"))
				heading_error = getattr(nx,'epd', float("NaN"))

				#print(float(getattr(nx,'', float("NaN"))))
				#print (" longitude = " + str(longitude) + ", latitude = " + str(latitude)+ ", altitude = " + str(altitude) + " m , vel  = " + str(velocity) + " m/s , GPS Heading = " + str(heading) + " degrees",end='\r')
				if self.record:
					self.data['latitude'].append (latitude)
					self.data['latitude_error'].append (latitude_error)

					self.data['longitude'].append(longitude)
					self.data['longitude_error'].append(longitude_error)

					self.data['altitude'].append(altitude)
					self.data['altitude_error'].append(altitude_error)

					self.data['velocity'].append(velocity)
					self.data['velocity_error'].append(velocity_error)

					self.data['heading'].append(heading)
					self.data['heading_error'].append(heading_error)

					self.data['time'].append(time.time())

	def stop(self):
		self.record = False
		data = self.data
		dataframe = pd.DataFrame([data])
		now = datetime.now()
		dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
		dataframe.to_csv(self.log_path + dt_string + '.csv', index=False,header=True)
		self.data = {'latitude':[], 'longitude':[], 'altitude':[], 'velocity':[], 'heading':[], 'time':[], 'latitude_error':[], 'longitude_error':[], 'altitude_error':[], 'velocity_error':[], 'heading_error':[],}

		return data



if __name__ == '__main__':
	print(__file__)
	r = Recorder()

	try:
		print(r.start())
		while True:
			pass
	except KeyboardInterrupt:
		print(r.stop())
