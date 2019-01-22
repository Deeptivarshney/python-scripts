import argparse
import json
import os
from ete3 import NCBITaxa
ncbi = NCBITaxa()

from Bio import SeqIO


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--indir', '--i', '-i', metavar="DIRECTORY", type=str, default="ncbi_blast_result",
                    help='Files with Blast results [DEFAULT: %(default)s]')
parser.add_argument('--genus_taxid', '-genus_taxid', dest='genus_taxid', type=int,  default=1386,
                    help='Taxonomy ID of query group of organisms [DEFAULT: %(default)s]')
parser.add_argument('--species_taxid', '-species_taxid', dest='species_taxid', type=int,  default=1390,
                    help='Taxonomy ID of query of species [DEFAULT: %(default)s]')
parser.add_argument('--fastadir', '--fastadir','-f', metavar="DIRECTORY", type=str, default="ncbi_bacteria_split",
                    help='input directory with genus subdirectories [DEFAULT: %(default)s]')
parser.add_argument('--outdir', '--o', '-o', metavar="DIRECTORY", type=str, default="ncbi_bacteria_blast_result-parse",
                    help='output directory to save results [DEFAULT: %(default)s]')
args = parser.parse_args()

CountRes = {}

if not os.path.exists(args.indir):
    print('Input Blast directory {} does not exists.'.format(args.indir))
    exit()


    
for Blastresultfile in os.listdir(args.indir):
    #print(args.genus_taxid, args.species_taxid)
    BlastresultfilePath = args.indir+"/"+Blastresultfile
    split_file_NM = Blastresultfile.split('_')
    Species_id = split_file_NM[0].split('.')
    if int(Species_id[0])== int(args.species_taxid):
        #print(Species_id,'>>>>',Blastresultfile,' from list of blast results', args.genus_taxid, args.species_taxid)
        
        IN_GENUS_PATH = os.path.join(args.fastadir, str(args.genus_taxid))
        Species_dirname = str(args.species_taxid)
        fastaName = str(args.species_taxid)+'.'+Species_id[1]+'.faa.'+Species_id[2]
        FastafilePath = os.path.join(IN_GENUS_PATH,Species_dirname,fastaName)
        #print(FastafilePath+ ' 1')
        
        names = ncbi.get_taxid_translator([Species_id[0]])
        lineage = ncbi.get_lineage(int(Species_id[0]))
        for i in lineage:
            rank = ncbi.get_rank([i])
            if rank[i] == 'species':
                species_ID = i
                SPName = names[species_ID]
                #print(SPName)
                
        #parsing the fasta File(Read fasta to dictionary)
        idcount = []
        fasta = {}
        #print(FastafilePath + 'lev 2 ' + Blastresultfile)
        fastaOpen = open(FastafilePath)
        for fastaline in fastaOpen:
            #print(fastaline)
            if fastaline.startswith('>'):
                #print(fastaline)
                ids = fastaline.split()[0].lstrip('>')
                fasta[ids] = []
                idcount.append(ids)
                #print(len(idcount))
                
        #Parsing the blast result
        blast = {}
        #blast results file in BlastoutputDir
        if Blastresultfile.endswith('blastp.txt'):
            #print('blast parsing>>> ',Blastresultfile)
            fh = open(BlastresultfilePath)
            for line in fh:
                splitline = line.rstrip( ).split("\t")
                queryid = splitline[0]
                dbline = splitline[1].split('|')
                dbval=dbline[1]
                #print(dbline[1])
                evalue = float(splitline[-2])
                
                if evalue < 10.0:
                    if queryid not in blast:
                        blast[queryid] = []
                    blast[queryid].append((dbval, evalue))
        #for k,v in blast.items():
        #print(k,v)
        fh.close()
        
        orphan=[]
        for queryid in fasta:
            if queryid in blast:
                TRG = True
                #print(queryid,blast[queryid])
                for value in blast[queryid]:
                    subtxid = value[0]
                    querytaxid = str(args.species_taxid)
                    if querytaxid != subtxid:
                        TRG = False
                if TRG:
                    #print("qid is TRG "+queryid)
                    orphan.append(queryid)
            else:
                #print("qid is TRG else "+queryid)
                orphan.append(queryid)
            
        uniqueListOrphan = set(orphan)
        percentage = len(uniqueListOrphan)/len(idcount)*100.0
        Out1 = str(species_ID)+'\t'+str(SPName)+'\t'+str(len(uniqueListOrphan))+'\t'+str(len(idcount))+'\t'+str(("%.2f" % percentage))+'%'+'\t'+str('|'.join(uniqueListOrphan))
        #print(Out1)
        
        if args.species_taxid in CountRes:
            CountRes[args.species_taxid].append(Out1)
        else:
            CountRes[args.species_taxid] = [Out1]
#1390	Bacillus amyloliquefaciens	2	1000	0.20%	taxid_1390_043444|taxid_1390_043157                

for k ,v  in CountRes.items():
    #print(type(k),v)
    sumofTRG = 0
    sumoftotalgene = 0
    TRGgenes =[]
    #gid = set()
    gname = set()
    
    for i in v:
        split_v = i.split("\t")
        #print(split_v)
        
        if split_v[0] == str(k):
            #print(split_v[0])
            #gid.add(split_v[0])
            gname.add(split_v[1])
            sumofTRG = sumofTRG + int(split_v[2])
            sumoftotalgene = sumoftotalgene + int(split_v[3])
            if split_v[5]:
                TRGgenes.append(split_v[5])
    
    percentageofTRGs = sumofTRG/sumoftotalgene*100.0
    print(str(k) +'\t'+ str(''.join(gname))+ '\t'+ str(sumofTRG) +'\t'+str(sumoftotalgene) +'\t'+ str(("%.2f" %percentageofTRGs))+'%'+'\t'+ str('|'.join(TRGgenes)))



