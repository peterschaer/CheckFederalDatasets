# -*- coding: latin-1 -*-
import urllib2
from bs4 import BeautifulSoup
import tempfile
import os
import FederalTopic

federalDataURL = "http://data.geo.admin.ch/"

#~ TODO: Benachrichtigung wenn etwas geändert (z.B. per Mail)
#~ TODO: federalDataURL als Input-Parameter

def getTopicList():
	topics = []
		
	f = urllib2.urlopen(federalDataURL)
	soup = BeautifulSoup(f)
	dataDiv = soup.find_all("div", class_="data")[0]
	links = dataDiv.find_all("a")
	
	for link in links:
		topics.append(link.get_text())
		
	return topics

federalTopics = getTopicList()
for f in federalTopics:
	ft = FederalTopic.FederalTopic(f, federalDataURL + f)
	print f + "," + ft.newMD5 + "  " + ft.oldMD5 + " Status: " + ft.status