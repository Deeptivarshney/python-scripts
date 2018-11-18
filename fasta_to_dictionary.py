# Run: python fasta_to_dictionary.py >out.fasta ##DV
# Python program for creating the dictionary from fasta file  & identify the identical sequences

from collections import defaultdict
import re

tmp = defaultdict(list)

file = open("single_line.fasta", "r")

for line in file:
	if line.startswith(">"):
		line = line.split(" ")[0].strip() # remove the all characters after first space
		ids = line
	else:
		tmp[line.strip("\n")].append(ids.rstrip())

for k in tmp:
	tmp[k]=[s.replace('>', '') for s in tmp[k]] # replace the '>' with none
	#print(k+"\n"+','.join(map(str,tmp[k])))
	#print((map(str,tmp[k]))+"\n"+','.join(k))
	#print('>'+'_'.join(map(str,tmp[k]))+'\n'+k)
	print('>'+'_'.join(map(str,tmp[k]))+'\n'+k) # join the list and string 
	
