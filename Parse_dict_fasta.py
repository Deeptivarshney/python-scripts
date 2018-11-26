import os
from Bio import SeqIO

MainDir = '/home/deepti/Documents/test_data'
OutDir = '/home/deepti/Documents/test_data_output'


if os.path.exists(MainDir):
	for d1 in os.listdir(MainDir): 

		Dir1 = os.path.join(MainDir, d1) 
		d ={}
		m ={}
		if os.path.exists(OutDir):
			outd1 = os.path.join(OutDir, d1)
			os.makedirs(outd1+'_output')
			outd2 = os.path.join(outd1+'_output')
			outputfasta = open(os.path.join(outd2, d1+'.fasta'), 'w')
			outputlog = open(os.path.join(outd2, d1+'.log.txt'), 'w')
	
			
			for d2 in os.listdir(Dir1):
				Dir2 = os.path.join(Dir1, d2)
				#print(Dir2)
				for files in os.listdir(Dir2):
					filePath= Dir2+"/"+files
					#print(filePath)
					fh = open(filePath)
					for seq_record in SeqIO.parse(fh, 'fasta'):
						seq = str(seq_record.seq)
						if seq not in d:
							d[seq] = []
						d[seq].append(seq_record.id)
						logVar=seq_record.id+"\t"+files
						#print(logVar)
						if seq_record.id not in m:
							m[seq_record.id] = []
						m[seq_record.id].append(files)
				fh.close()  #output.fasta
			
			for seqs, ids in d.items(): 
				#print(seqs,ids)
				outputfasta.write('>'+'#'.join(ids)+'\n'+ seqs +'\n')
				
			for ids, filenames in m.items():
				#print(ids,filenames)
				#print(type(filenames))
				#uniqFileNames= list(set(filenames))
				#print(ids,"\t",uniqFileNames)
				outputlog.write(ids+'\t'+Dir2+'/'+','.join(filenames)+'\n')               
