import sys
import pynotify
import urllib2
import threading
import time
from bs4 import BeautifulSoup

url = "http://www.coindesk.com/price/" 
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
session_high = 0.0
session_low = 0.0
startSession = False
count = 10 


# Get values from parsed data
def getBitValue(soup, startSession, session_low, session_high, count):
	# get data div for BitCoin Value
	div = soup.find(name="div",attrs = {'class':'bpi-value bpiUSD'}).text
	#print div
	# get %change
	change_down = soup.find(name="div", attrs = {'class':'bpi-change changeUSD data-down'})
	change_up = soup.find(name="div", attrs = {'class':'bpi-change changeUSD data-up'})
	change = "0.0 %"
	if change_down is not None:
		change = "-"+change_down.text
	elif change_up is not None:
		change = "+"+change_up.text
	#print change
	print "Current Valuation: ",div," ",change
	print "Count:",count
	print startSession
	if startSession is False:
		session_low = div
		session_high = div
	else:
		if div>session_high:
			session_high = div
			notify("Session high! Sell now!", session_high+" "+change)
		else:
			session_low =div
			notify("Session low! Buy now!", session_low+" "+change)
		count = count + 10	
	startSession = True;
	if count % 20 == 0:
		print "notify called"
		notify("Current Valuation ", div+" "+change)
	threading.Timer(count, pingForData,[url, hdr, True]).start()

# Add a desktop notification	
def notify(title,msg):
	pynotify.init("Get Bitcoins")
	notif = pynotify.Notification (title,msg)
	notif.show()

# Ping for data
def pingForData(url, hdr, startSession):
	req = urllib2.Request(url,headers=hdr)
	soup = BeautifulSoup(urllib2.urlopen(req))
	getBitValue(soup, startSession, session_low, session_high, count)

pingForData(url, hdr, False)
