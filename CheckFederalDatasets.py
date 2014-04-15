# -*- coding: latin-1 -*-
import urllib2
from bs4 import BeautifulSoup
import tempfile
import os
import FederalTopic
import codecs

logFile = "@(LogFileName)"
federalDataURL = "@(#var.FEDERALURL)"
configDB = r"@(#var.CONFIGDB)"

log = codecs.open("@(LogFileName)", "w","iso-8859-1")

#~ TODO: Benachrichtigung wenn etwas geändert (z.B. per Mail)

def getTopicList():
	topics = []
		
	f = urllib2.urlopen(federalDataURL)
	soup = BeautifulSoup(f)
	dataDiv = soup.find_all("div", class_="data")[0]
	links = dataDiv.find_all("a")
	
	for link in links:
		topics.append(link.get_text())
		
	return topics

federalTopicNames = getTopicList()
federalTopics = []
for f in federalTopicNames:
	ft = FederalTopic.FederalTopic(f, federalDataURL + f, configDB)
	federalTopics.append(ft)

#~ Nach Status sortieren
federalTopicsSorted = sorted(federalTopics, key=lambda FederalTopic: FederalTopic.status)
for ft in federalTopicsSorted:
	print ft.status + ": " + ft.name + " (" + ft.oldMD5 + " " + ft.newMD5 + ")"

if len(federalTopicsSorted)==0:
	log.write(u"Script failed")
else:
	log.write(u"Script was SUCCESSFUL")

log.close()
	
	