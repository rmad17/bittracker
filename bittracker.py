import sys
import pynotify
import urllib2
from bs4 import BeautifulSoup

url = "http://www.coindesk.com/price/" 
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
req = urllib2.Request(url,headers=hdr)
soup = BeautifulSoup(urllib2.urlopen(req))
def getBitValue(soup):
	# get data div for BitCoin Value
	div = soup.find(name="div",attrs = {'class':'bpi-value bpiUSD'}).text
	data= "CurrentValuation: "+div
	print data
	notify(div)
	#notify-send data
	# get down change div
	down_div = soup.find(name="div", attrs={'class': 'percent data-down'})
	print "-",down_div,"%"

def notify(div):
	pynotify.init("Get Bitcoins")
	notif = pynotify.Notification ("Current Valuation ",div)
	notif.show()
getBitValue(soup)
	
