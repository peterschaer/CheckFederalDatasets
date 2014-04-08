import urllib2
import tempfile
import os
import shutil

class FederalTopic():
	def __init__(self, name, URL):
		self.name = name
		self.url = URL
		self.tempFile = ""
		self.tempDir = ""
		self.oldMD5 = ""
		self.newMD5 = ""

		self.__downloadReadme__()
		self.__deleteTempDir__()
		
	def __downloadReadme__(self):
		topicURLReadme = self.url + "/readme.txt"
		self.tempDir = tempfile.mkdtemp()
		self.tempFile = os.path.join(self.tempDir, self.name + "_readme.txt")
		f = urllib2.urlopen(topicURLReadme)
		with open(self.tempFile, "wb") as code:
			code.write(f.read())
		
	def __extractMD5Checksum__(self):
		readmeFile = open(self.tempFile, "r")
		
		readmeFile.close()
		
	def __deleteTempDir__(self):
		shutil.rmtree(self.tempDir)
		