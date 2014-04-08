# -*- coding: latin-1 -*-
import urllib2
import tempfile
import os
import shutil
import hashlib
import sqlite3

#~ TODO: wenn Status changed => neuen MD5-Wert in DB speichern
#~ configDB parametrisieren

class FederalTopic():
	def __init__(self, name, URL):
		self.name = name
		self.url = URL
		self.ReadmeFile = ""
		self.tempDir = ""
		self.ReadmeContent =""
		self.oldMD5 = ""
		self.newMD5 = ""
		self.configDB = r"C:\Daten\Repos\CheckFederalDatasets\federalTopicsConf.sqlite"
		self.status = "unassigned"

		self.__downloadReadme__()
		self.__getMD5FromReadme_()
		self.__deleteTempDir__()
		self.__getMD5FromDB__()
		self.__compareMD5__()
		
	def __downloadReadme__(self):
		topicURLReadme = self.url + "/readme.txt"
		self.tempDir = tempfile.mkdtemp()
		self.ReadmeFile = os.path.join(self.tempDir, self.name + "_readme.txt")
		f = urllib2.urlopen(topicURLReadme)
		with open(self.ReadmeFile, "wb") as code:
			code.write(f.read())
		
	def __getFileContent__(self):
		readmeFile = open(self.ReadmeFile, "r")
		self.ReadmeContent = readmeFile.read()
		readmeFile.close()
		
	def __getMD5FromReadme_(self):
		self.__getFileContent__()
		searchString = "MD5Checksum:"
		checkSumLength = 32
		text = self.ReadmeContent
		index = text.index(searchString) + len(searchString)
		#~ Es müssen genau 32 Zeichen für die Checksumme aus dem String extrahiert werden
		#~ Einige Readmes haben am Schluss noch Zeilenumbrüche
		self.newMD5 = text[index:index+checkSumLength]
		
	def __deleteTempDir__(self):
		shutil.rmtree(self.tempDir)
		
	def __getMD5FromDB__(self):
		connection = sqlite3.connect(self.configDB)
		sql = "SELECT md5 from federalTopics WHERE topic='" + self.name + "'"
		cursor = connection.cursor()
		self.oldMD5 = cursor.execute(sql).fetchone()[0]
		cursor.close()
		connection.close()
		
	def __compareMD5__(self):
		if self.oldMD5 == self.newMD5:
			self.status = "unchanged"
		else:
			self.status = "changed"
		