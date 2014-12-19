import sys
import urllib2
from xml.dom import minidom

def next_space(s, p):
	loc = p
	for c in s[p:]:
		if (unicode.isspace(c)):
			return loc
		loc += 1
	return loc

def search(artist, track, seq):
	print("searching "+track)

	akey = "17826649999271fa8a03b08ea02f49c1" # API display key
	burl = "http://test.lyricfind.com/api_service/lyric.do"
	url = burl+"?apikey="+akey+"&reqtype=default&trackid=artistname:"+artist+",trackname:"+track
	data = urllib2.urlopen(url)
	song = data.read()

	xml = minidom.parseString(song)
	response = xml.getElementsByTagName('response')[0].getAttributeNode('code')
	code = int(response.nodeValue) # API response code

	if code == 102:
	#	print("API102: Instrumental")
		return
	elif code >= 202 and code <= 207:
	#	print("API"+str(code)+": Unavailable")
		return

	lyrics = xml.getElementsByTagName('lyrics')[0].firstChild.nodeValue

	space = 1
	ignore = 0
	seqcount = 0
	startloc = -1
	loc = 0
	for c in lyrics:
		loc += 1
		if c.isspace():
			space = 1
		elif c == '(' or c == ')':
			ignore = not ignore
		elif c == '"' or c == '\'':
			continue
		elif not c in "()><,./\\?" and space == 1:
			space = 0
			if (unicode.lower(c) == seq[seqcount]):
				if (startloc == -1):
					startloc = loc-1
				seqcount += 1
				if (seqcount == len(seq)):
					snippet = lyrics[startloc:-(len(lyrics)-next_space(lyrics, loc))]
					print("***MATCH*** "+track+":"+str(loc)+": "+snippet)
					startloc = -1
					seqcount = 0
			else:
				startloc = -1
				seqcount = 0

# DEV
if (len(sys.argv) > 3):
	search(sys.argv[1], sys.argv[2], sys.argv[3])
