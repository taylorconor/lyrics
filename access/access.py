import sys
import urllib2
from xml.dom import minidom

if (len(sys.argv) > 1):
	key = sys.argv[1];
else:
	print("No argument!");
	exit();

def clean_str(n):
	s = "";
	for c in n:
		if c == ' ':
			s += '+';
		elif c in ".,:;/\\'\"()!@$%^&*":
			continue;
		else:
			s += str.lower(str(c));
	return s;


url = "http://lyrics.wikia.com/api.php?action=lyrics&artist="+key+"&fmt=xml&func=getSong";
data = urllib2.urlopen(url);
songs = data.read();

print(songs);

xml = minidom.parseString(songs);
itemlist = xml.getElementsByTagName('item');
processedlist = [];

for item in itemlist:
	name = clean_str(item.firstChild.nodeValue);
	if (name not in processedlist):
		processedlist.append(name);

for song in processedlist:
	print(song);
