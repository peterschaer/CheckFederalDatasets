# -*- coding: latin-1 -*-
import urllib2
from bs4 import BeautifulSoup
import tempfile
import os
import FederalTopic
import codecs
import smtplib
from email.mime.text import MIMEText

logFile = "@(LogFileName)"
federalDataURL = "@(#var.FEDERALURL)"
configDB = r"@(#var.CONFIGDB)"
mailaddresses = r"@(#var.MAILADDRESSES)"

log = codecs.open("@(LogFileName)", "w","iso-8859-1")

#~ TODO: Benachrichtigung wenn etwas geändert (z.B. per Mail)
def notifyStatus(topics, toaddrs):
	#~ Input-String muss gesplittet werden, da sendmail (s. unten) eine Liste erwartet
	toaddrsList = toaddrs.split(";")

	message = "UNCHANGED\t= keine Veraenderung im Datensatz\nCHANGED\t= Datensatz wurde aktualisiert\nADDED\t\t= neuer Datensatz\n\n"
	for topic in topics:
		message = message + topic.status + ": " + topic.name + "\n"
	
	msg = MIMEText(message)
	msg['Subject'] = "Statusmeldung data.geo.admin.ch"
	msg['From'] = "noreply_syncserv@bve.be.ch"
	#~ Hier muss ein String übergeben werden
	msg['To'] = toaddrs
	
	s = smtplib.SMTP('mailhub.be.ch')
	#~ Hier muss eine Liste übergeben werden (To-Adressen)
	s.sendmail(msg['From'], toaddrsList, msg.as_string())
	s.quit()

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

notifyStatus(federalTopicsSorted, mailaddresses)

if len(federalTopicsSorted)==0:
	log.write(u"Script failed")
else:
	log.write(u"Script was SUCCESSFUL")

log.close()
	
	