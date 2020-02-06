import time
import board
import busio
import serial
import adafruit_gps



def init():
	# for a computer, use the pyserial library for uart access
	global uart
	global gps
	uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)

	# Create a GPS module instance.
	gps = adafruit_gps.GPS(uart, debug=False)     # Use UART/pyserial

	# Turn on the basic GGA and RMC info (what you typically want)
	gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')


	# Set update rate to once a second (1hz) which is what you typically want.
	gps.send_command(b'PMTK220,1000')
	# This would be twice a second (2hz, 500ms delay):
	# gps.send_command(b'PMTK220,500')	

def acquire():
	global gps
	global uart
	gpsTime = [0, 0, 0]
	gpsData = [0, 0, 0, 0, 0, 0]
	gpsQuality = [0, 0]
	# Make sure to call gps.update() every loop iteration and at least twice
	# as fast as data comes from the GPS unit (usually every second).
	gps.update()
	if not gps.has_fix:
		gps.update()
		print("waiting for fix")
		time.sleep(0.1)
	if not gps.has_fix:
		gps.update()
		print("waiting for fix")
		time.sleep(0.1)
	if not gps.has_fix:
		gps.update()
		print("waiting for fix")
		time.sleep(0.1)
	if not gps.has_fix:
		gps.update()
		print("waiting for fix")
		time.sleep(0.1)
	if not gps.has_fix:
		gps.update()
		print("waiting for fix")
		time.sleep(0.1)
	if gps.has_fix:
		#Data tuple of GPS UTC Timelock (Hours, Minutes, Seconds)
		gpsTime = [gps.timestamp_utc.tm_hour, gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec]
		#Data Tuple of (Latitude, Longitude, Altitude, Speed, TAD, HD)
		gpsData = [gps.latitude, gps.longitude, gps.altitude_m, gps.speed_knots, gps.track_angle_deg, gps.horizontal_dilution]
		#Data Tuple of (Fix Quality, # of satellites)
		gpsQuality = [gps.fix_quality, gps.satellites]
	
	return True, gpsTime, gpsData, gpsQuality