#coding=UTF8

import time
import re
import collections
import requests
import uniout
from lxml import etree



##################################################
# Settings
##################################################

MAIN_URL = "http://ep.kuas.edu.tw/"
POST_URL = "http://ep.kuas.edu.tw/EPortfolio/EPDefaultPage.aspx"
ACTIVE_URL="http://ep.kuas.edu.tw/EPortfolio/Activity/ActivitySystem.aspx"

username     = "1102108131"
password     = "6019"

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0"


def login():
	try:
		session = requests.session()
		response = session.get(POST_URL , headers = headers)
	except Exception, e:
		raise e

	payload = collections.OrderedDict()
	raw_data = ['__EVENTTARGET','','__EVENTARGUMENT','',
				'__VIEWSTATE', '',
				'ctl00$LoginForm1$TbLoginId', username,
				'ctl00$LoginForm1$TbLoginPW', password,
				'ctl00$LoginForm1$BtLogin','登入',
				'ctl00$ContentPlaceHolder1$HFUrlPath','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl00$HF1','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl00$HF2','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl00$HF3','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl00$HFAnnId','7',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl01$HF1','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl01$HF2','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl01$HF3','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl01$HFAnnId','6',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl02$HF1','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl02$HF2','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl02$HF3','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl02$HFAnnId','5',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl03$HF1','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl03$HF2','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl03$HF3','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl03$HFAnnId','4',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl04$HF1','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl04$HF2','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl04$HF3','',
				'ctl00$ContentPlaceHolder1$DataListPost$ctl04$HFAnnId','3',
				'ctl00$BlockUIShowFlag','',
				'ctl00$HFBlockTimeOut','']

	
	for x in xrange(0,len(raw_data),2):
		payload[raw_data[x]] = raw_data[x+1]
		
	root = etree.HTML(response.content)
	for i in root.xpath("//input"):
		if i.attrib['name'] == '__VIEWSTATE':
			payload['__VIEWSTATE'] = i.attrib['value']
		if i.attrib['name'] == '__EVENTVALIDATION':
			payload['__EVENTVALIDATION'] = i.attrib['value']
			
		
	# Setting Headers
	headers['Accept'] = "zh-tw,en-us;q=0.7,en;q=0.3"
	headers['Accept-Encoding'] = "gzip, deflate"
	headers['Referer'] = "http://ep.kuas.edu.tw/EPortfolio/EPDefaultPage.aspx"
	headers['Connection'] = "keep-alive"
	
	
	# RePost Data
	response = session.post(POST_URL , data = payload, headers = headers)
	
	root = etree.HTML(response.text)
	result = root.xpath("//span[@id = 'LoginForm1_LbLoginName']")
	
	
	if result:
		print u"Login Success! %s" % (result[0].text)
		print response.request.headers['Cookie']
		return 1
	else:
		print u"Login Falied!"
		return 0


if __name__ == '__main__':
	login()

