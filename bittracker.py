#--------------------------------------------------- LICENSE ---------------------------------------------------------------------
# BitTracker
#Copyright (C) 2014 by Sourav Basu <souravbasu17@gmail.com>
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#--------------------------------------------------- LICENSE ---------------------------------------------------------------------

#!/usr/bin/python
import sys,re
import argparse
import pynotify
import urllib2
import threading
import time
from bs4 import BeautifulSoup

url = "http://www.coindesk.com/price/" 
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
count = 0 
currentValue = ""
unocoin = False

# Using CoinDesk
def getfromCoinDesk(soup):
	div = soup.find(name="div",attrs = {'class':'bpi-value bpiUSD'}).text
	# get %change
	change_down = soup.find(name="div", attrs = {'class':'bpi-change changeUSD data-down'})
	change_up = soup.find(name="div", attrs = {'class':'bpi-change changeUSD data-up'})
	change = "0.0 %"
	if change_down is not None:
		change = change_down.text
	elif change_up is not None:
		change = "+"+change_up.text
	data = div+" "+change	
	getBitValue("CoinDesk Valuation: ", data)

# Get UnoCoin Data
def unocoindata():
	soup = pingForData("https://www.unocoin.com/",hdr)
	div = soup.find('div',{'class':'col-lg-12 col-sm-12'})
	#div.replace_with('')
	print div

# Get process data
def getBitValue(title,data):
	notify(title, data)
	if unocoin:
		#unocoindata()
		print "UnoCoin not supported right now. Coming Soon!"
	soup= pingForData(url, hdr)
	threading.Timer(60, getfromCoinDesk,[soup]).start()

# Add a desktop notification	
def notify(title,msg):
	pynotify.init("Get Bitcoins")
	notif = pynotify.Notification (title,msg)
	notif.show()

# Ping for data
def pingForData(url, hdr):
	req = urllib2.Request(url,headers=hdr)
	soup = BeautifulSoup(urllib2.urlopen(req))
	return soup

parser = argparse.ArgumentParser(description='Track BitCoin Values')
parser.add_argument('--uno', help='pass "1" to get INR value from unocoin.com', required=False)
#parser.add_argument('-b','--bar', help='Description for bar argument', required=True)
args = vars(parser.parse_args())
if args['uno'] == '1':
	unocoin = True

soup= pingForData(url, hdr)
getfromCoinDesk(soup)
