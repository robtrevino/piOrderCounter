import RPi.GPIO as GPIO
import time
from decimal import Decimal, ROUND_DOWN
import requests

updateTime = 300 # 5 minutes between updates
apiKey = '<your key goes here>'
password = '<your password goes here>'
url = 'https://<your url>.myshopify.com/admin/orders/count.json'

def truncateDecimal(d, places =0):
	return d.quantize(Decimal(10) ** -places, rounding=ROUND_DOWN)

GPIO.setmode(GPIO.BOARD)
 
# GPIO ports for the 7seg pins
#segments =  [26,12,22,18,16,8,15]  #to rotate
segments = [18,16,8,26,12,22,15]

 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, False)
 
# GPIO ports for the digit 0-3 pins 
#digits = [7,3,5] #to rotate
digits = [5,3,7] 
 
GPIO.setup(digits, GPIO.OUT)
GPIO.output(digits, True)

 
nums = {' ':[False,False,False,False,False,False,False],
    '0':[True,True,True,True,True,True,False],
    '1':[False,True,True,False,False,False,False],
    '2':[True,True,False,True,True,False,True],
    '3':[True,True,True,True,False,False,True],
    '4':[False,True,True,False,False,True,True],
    '5':[True,False,True,True,False,True,True],
    '6':[True,False,True,True,True,True,True],
    '7':[True,True,True,False,False,False,False],
    '8':[True,True,True,True,True,True,True],
    '9':[True,True,True,True,False,True,True]}

	
	
def showNumber(num):
	breakout = [truncateDecimal(Decimal(num%1000 /100))
						,truncateDecimal(Decimal(num%100 / 10))
						,num%10]	
	
	segmentsState = [False,False,False,False,False,False,False]
	for eachDigit in range(3):
		digitsState = [False,False,False]
		digitsState[eachDigit] = True
		for loop in range(7):
			segmentsState[loop] = not nums[str(breakout[eachDigit])][loop]
		GPIO.output(digits+segments,digitsState+segmentsState)
		time.sleep(0.004)
	
try:
	while True:
		r = requests.get(url, auth=(apiKey, password))
		response = r.json()
		count = response['count']
		start = time.time()
		while True:
			showNumber(count)
			if time.time() - start >= updateTime:
				break;
			
			
finally:
	GPIO.cleanup()
