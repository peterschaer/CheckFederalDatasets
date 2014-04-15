# -*- coding: latin-1 -*-
import urllib2
import tempfile
import os
import shutil
import hashlib
import sqlite3

class FederalTopic():
	def __init__(self, name, URL, DB):
		self.name = name
		self.url = URL
		self.ReadmeFile = ""
		self.tempDir = ""
		self.ReadmeContent =""
		self.oldMD5 = ""
		self.newMD5 = ""
		self.configDB = DB
		self.status = "UNASSIGNED"

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
		#~ Es wird nicht der MD5-String aus der Datei gelesen, sondern über die gesamte readme.txt-Datei der MD5-Hash gebildet.
		#~ Wenn sich irgendetwas in der readme.txt-Datei ändert, wird das bemerkt.
		self.__getFileContent__()
		md5 = hashlib.md5()
		md5.update(self.ReadmeContent)
		self.newMD5 = md5.hexdigest()
		
	def __deleteTempDir__(self):
		shutil.rmtree(self.tempDir)
		
	def __getMD5FromDB__(self):
		conn = sqlite3.connect(self.configDB)
		sql = "SELECT md5 from federalTopics WHERE topic='" + self.name + "'"
		resultRow = conn.execute(sql).fetchone()
		conn.close()
		#~ Ein leeres Resultat bedeutet einen neuen Datensatz
		self.oldMD5 = "UNDEFINED"
		if resultRow is not None:
			self.oldMD5 = resultRow[0]
		
	def __updateDBMD5__(self):
		#~ nur wenn der Status geändert hat, muss die Tabelle aktualisiert werden
		sql = ""
		if self.status != "UNCHANGED":
			if self.status == "CHANGED":
				sql = "UPDATE federalTopics SET md5='" + self.newMD5 + "' WHERE topic='" + self.name + "'"
			elif self.status == "NEW":
				sql = "INSERT INTO federalTopics(topic, md5) VALUES ('" + self.name + "','" + self.newMD5 + "')"
			conn = sqlite3.connect(self.configDB)
			conn.execute(sql)
			conn.commit()
			conn.close()
		
	def __compareMD5__(self):
		if self.oldMD5 == "UNDEFINED":
			self.status = "NEW"
		else:
			if self.oldMD5 == self.newMD5:
				self.status = "UNCHANGED"
			else:
				self.status = "CHANGED"
		self.__updateDBMD5__()