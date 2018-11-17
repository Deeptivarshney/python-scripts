from collections import defaultdict
import re

tmp = defaultdict(list)

file = open("test.fasta", "r")

for line in file:
	if line.startswith(">"):
		ids = line
	else:
		tmp[line.strip("\n")].append(ids.rstrip())


#print(tmp)
for k in tmp:
	tmp[k]=[s.replace('>', '') for s in tmp[k]]
	print(k+"\t"+','.join(map(str,tmp[k])))
	
