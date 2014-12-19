import urllib2
import xml.etree.ElementTree as ET

response = urllib2.urlopen('http://lyrics.wikia.com/api.php?action=lyrics&artist=David%20Bowie&fmt=xml&func=getSong')
xml = response.read()

root = ET.fromstring(xml)

for child in root:
	if child.tag == 'artist':
		print child.text
	if child.tag == 'albums':
		for album in child:
			if album.tag == 'album':
				albumTitle = album.text
			if album.tag == 'year':
				print '\n---'+albumTitle+('('+album.text+')' if album.text != None else '')+'---'
			if album.tag == 'songs':
				for song in album:
					print song.text
