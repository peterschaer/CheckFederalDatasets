import urllib2
from bs4 import BeautifulSoup
import tempfile
import os

federalDataURL = "http://data.geo.admin.ch/"
tempDir = tempfile.mkdtemp()
print tempDir

def getTopicList():
	f = urllib2.urlopen(federalDataURL)
	soup = BeautifulSoup(f)

	dataDiv = soup.find_all("div", class_="data")[0]
	#~ print dataDiv

	federalTopics = []

	links = dataDiv.find_all("a")
	for link in links:
		federalTopics.append(link.get_text())
		
	return federalTopics
	
topics = getTopicList()
for t in topics:
	topicURL = federalDataURL + (t)
	topicURLReadme = topicURL + "/readme.txt"
	print topicURL
	tempFile = os.path.join(tempDir, t + "_readme.txt")
	f = urllib2.urlopen(topicURLReadme)
	with open(tempFile, "wb") as code:
		code.write(f.read())
	