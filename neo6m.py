from gps import*
from threading import Thread

class GPS:
	def __init__(self):
		self.gps_data = {'latitude' : float("Nan"), 'latitude_error' : float("Nan"), 'longitude' : float("Nan"), 'longitude_error' : float("Nan"), 'altitude' : float("Nan"), 'altitude_error' : float("Nan"), 'velocity' : float("Nan"), 'velocity_error' : float("Nan"), '' : float("Nan"), 'heading' : float("Nan"), 'heading_error' : float("Nan"), 'magnetic_declination' : float("Nan"),'nsat' : float(0)}
		self.gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
		self.thread = Thread(target=self.run)
		self.thread.daemon = True
		self.thread.start()

	def run(self):
		while True:
			nx = self.gpsd.next()
			nsat = 0
			# https://gpsd.gitlab.io/gpsd/gpsd_json.html
			if nx['class'] == 'SKY':
				#print("SKY")
				for SAT in nx['satellites']:
					if SAT['used'] == True:
						nsat += 1
				self.gps_data['nsat'] = nsat
				#print(nsat)
			if nx['class'] == 'TPV':
				#print("TPV")
				self.gps_data['latitude'] = getattr(nx,'lat', float("NaN"))
				self.gps_data['latitude_error'] = getattr(nx,'epx', float("NaN"))
				self.gps_data['longitude'] = getattr(nx,'lon', float("NaN"))
				self.gps_data['longitude_error'] = getattr(nx,'epy', float("NaN"))
				self.gps_data['altitude'] = getattr(nx,'alt', float("NaN"))
				self.gps_data['altitude_error'] = getattr(nx,'epv', float("NaN"))
				self.gps_data['velocity'] = getattr(nx,'speed', float("NaN"))
				self.gps_data['velocity_error'] = getattr(nx,'eps', float("NaN"))
				self.gps_data['heading'] = getattr(nx,'track', float("NaN"))
				self.gps_data['heading_error'] = getattr(nx,'epd', float("NaN"))
				self.gps_data['magnetic_declination'] = getattr(nx,'magvar', float("NaN"))

	def get_gps_data(self):
		gps_data = self.gps_data
		self.gps_data = {'latitude' : float("Nan"), 'latitude_error' : float("Nan"), 'longitude' : float("Nan"), 'longitude_error' : float("Nan"), 'altitude' : float("Nan"), 'altitude_error' : float("Nan"), 'velocity' : float("Nan"), 'velocity_error' : float("Nan"), '' : float("Nan"), 'heading' : float("Nan"), 'heading_error' : float("Nan"), 'magnetic_declination' : float("Nan"), 'nsat' : float(0)}
		return gps_data


if __name__ == '__main__':
	from time import sleep
	try:
		neo6m = GPS()
		while True:
			data = neo6m.get_gps_data()
			if data['nsat'] != 0 and data['heading'] != float("NaN"):
				print(data)
			sleep(0.02)
	except KeyboardInterrupt:
		print("\nUser Interrupt")
		exit()
