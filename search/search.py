import sys

with open ("temp.txt", "r") as myfile:
	data=myfile.read();

if (len(sys.argv) > 1):
	seq = sys.argv[1];
else:
	print("No argument!");
	exit();

space = 0;
ignore = 0;
seqcount = 0;
startloc = -1;
loc = 0;
for c in data:
	if c.isspace():
		space = 1;
	elif c == '(' or c == ')':
		ignore = not ignore;
	elif not c in "()><,./\\" and space == 1:
		print(c);
		space = 0;
		if (str.lower(c) == seq[seqcount]):
			if (startloc == -1):
				startloc = loc;
			#print("SEQCOUNT = "+str(seqcount)+", LEN = "+str(len(seq))+"\n");
			seqcount += 1;
			if (seqcount == len(seq)):
				print("MATCH loc = "+str(startloc));
				startloc = -1;
				seqcount = 0;
		else:
			startloc = -1;
			seqcount = 0;
	loc += 1;
