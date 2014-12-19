import sys
import threading
import urllib2
from xml.dom import minidom

import search

if (len(sys.argv) > 2):
	key = sys.argv[1]
	seq = sys.argv[2]
else:
	print("Expects: [artist] [sequence]");
	exit()

def clean_str(n):
	s = ""
	for c in n:
		if c == ' ':
			s += '+'
		elif c in ".,:;/\\'\"()!@$%^&*":
			continue
		else:
			s += unicode.lower(c)
	return s


url = "http://lyrics.wikia.com/api.php?action=lyrics&artist="+key+"&fmt=xml&func=getSong"
data = urllib2.urlopen(url)
songs = data.read()

xml = minidom.parseString(songs)
itemlist = xml.getElementsByTagName('item')
processedlist = []
threadlist = []

for item in itemlist:
	name = clean_str(item.firstChild.nodeValue)
	if (name not in processedlist):
		processedlist.append(name)

import time
starttime = time.time();
for song in processedlist:
	search.search(key, song, seq)
	#thread = threading.Thread(target=search.search(key, song, seq))
	#threadlist.append(thread)
	#thread.start()

print "TIME: "+str(time.time()-starttime)
