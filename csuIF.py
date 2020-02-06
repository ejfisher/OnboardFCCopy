import csuGPS
import csuI2C
import csuDM
import csuTX
import time

timeA = ["Hours", "Minutes", "Seconds"]
gpsD = ["Latitude", "Longitude", "Altitude", "Speed", "TAD", "HD"]
gpsQ = ["Quality", "# of Satellites"]
axis = ["X", "Y", "Z"]
mplA = ["Pressure", "Altitude", "Temperature"]
headers = [timeA, gpsD, gpsQ, axis, axis, axis, mplA]
dNames = ['Time.csv', 'gpsData.csv', 'gpsQuality.csv', 'acc.csv', 'mag.csv', 'gyro.csv', 'mpl.csv']

initTime = time.monotonic()
csuGPS.init()
csuI2C.init()
csuTX.init()
for i in range(7):
		csuDM.init(dNames[i], headers[i])
# Return Tuples for aquire are in the format
# time = (utc-hr, utc-min, utc-sec)
#gpsData = (Latitude, Longitude, Altitude, Speed, TAD, HD)
#gpsQuality = (fix-quality, # of Sattelites)
lTime = time.monotonic()
loopStart = lTime
for i in range(6069):
	gpsLock, gpsTime, gpsData,gpsQuality = csuGPS.acquire()
	acc, mag, gyro, mpl  = csuI2C.acquire()
	print(gpsData)
	bigData = [gpsTime, gpsData, gpsQuality, acc, mag, gyro, mpl]
	dString = csuDM.formatString(bigData)
	#print(type(dString))
	#print(dString)
	#Take the aquired data and output to a file
	for i in range(7):
		csuDM.write(dNames[i], bigData[i])
		#print("writing to the file")

	#display data aquired
	print('=' * 60)  # Print a separator line.
	print('Time: {0[0]}:{0[1]}:{0[2]} '.format(gpsTime))
	print('=' * 60)  # Print a separator line.
	#print('Acceleration (m/s^2): ({0[0]},{0[1]},{0[2]})'.format(acc))
	#print('Magnetometer (uTesla): ({0[0]},{0[1]},{0[2]})'.format(mag))
	#print('Gyroscope (radians/s): ({0[0]},{0[1]},{0[2]})'.format(gyro))
	#print('=' * 60)  # Print a separator line.
	print('Latitude: {0[0]:} degrees\nLongitude: {0[1]} degrees\nAltitude: {0[2]} meters'.format(gpsData))
	print('Fix quality: {0[0]}\n# satellites: {0[1]}'.format(gpsQuality))
	#print('=' * 60)  # Print a separator line.
	#print('Pressure: {0[0]} pascals\nAltitude: {0[1]} meters\nTemperature: {0[2]} degrees Celsius'.format(mpl))
	


	#guarantees LORA packet is sent at LEAST 1 second apart. 
	currentTime = time.monotonic()
	
	
	csuTX.transmit(dString)

print('=' * 60)  # Print a separator line.
print("Time to initialize: " + str(loopStart - initTime))
print('Time to loop: ' + str(currentTime - loopStart))
print('Total time Executing: ' + str(currentTime - initTime))
print('=' * 60)  # Print a separator line.