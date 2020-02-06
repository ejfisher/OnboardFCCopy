import time
import busio
import digitalio
import board
import adafruit_rfm9x

def init():
	global rfm9x

	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)\
	#these board pins may change
	cs = digitalio.DigitalInOut(board.D5) 
	reset = digitalio.DigitalInOut(board.D6)
	try:
		rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
		#remove this later, for testing purposes only
		print("rfm9x module detected!")
	except RuntimeError as error:
		print("Module Not Found")	

def transmit(dString):
	#remove print statements later this is for testing
	print("Attempting to transmit")
	try:
		rfm9x.send(dString)
		print("Transmitted successfully: " + str(dString))
	except:
		print("whoops couldnt transmit that one")
	