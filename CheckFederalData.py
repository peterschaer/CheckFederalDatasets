import urllib2
from bs4 import BeautifulSoup

federalDataURL = "http://data.geo.admin.ch/"

f = urllib2.urlopen(federalDataURL)
soup = BeautifulSoup(f)

dataDiv = soup.find_all("div", class_="data")
print dataDiv