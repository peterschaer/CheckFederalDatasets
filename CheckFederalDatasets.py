import urllib2
from bs4 import BeautifulSoup
import tempfile
import os
import FederalTopic

federalDataURL = "http://data.geo.admin.ch/"
#~ tempDir = tempfile.mkdtemp()
#~ print "Temp-Dir: " + tempDir

def getTopicList():
	f = urllib2.urlopen(federalDataURL)
	soup = BeautifulSoup(f)

	dataDiv = soup.find_all("div", class_="data")[0]
	#~ print dataDiv

	topics = []

	links = dataDiv.find_all("a")
	for link in links:
		topics.append(link.get_text())
		
	return topics

def downloadReadme(topics):
	readmes = []
	for t in topics:
		topicURL = federalDataURL + (t)
		topicURLReadme = topicURL + "/readme.txt"
		tempFile = os.path.join(tempDir, t + "_readme.txt")
		f = urllib2.urlopen(topicURLReadme)
		with open(tempFile, "wb") as code:
			code.write(f.read())
		readmes.append(tempFile)
	return readmes

#~ def extractMD5(readme):
	#~ print readme

federalTopics = getTopicList()
for f in federalTopics:
	ft = FederalTopic.FederalTopic(f, federalDataURL + f)
	print ft.tempFile
	
#~ federalTopicsReadme = downloadReadme(federalTopics)

#~ for f in federalTopicsReadme:
	#~ md5 = extractMD5(f)

#~ TODO: delete Tempdir