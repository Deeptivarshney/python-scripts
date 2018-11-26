import os
import json
import subprocess
import zipfile
import tarfile
import re

from ete3 import NCBITaxa
ncbi = NCBITaxa()

url = 'ftp://ftp.ensemblgenomes.org/pub/bacteria/release-41/fasta'
genus_taxid = 1386


fh = open('species_metadata_EnsemblBacteria.json')
metadata = json.load(fh)
fh.close()

d = {}
n=0
oh = open('logfile.txt', 'w')
for d in metadata:
    db = d["core"]["dbname"]
    assembly = d["assembly"]["assembly_name"]
    organism_id = d['organism_id']
    organism_name = d["organism"]["name"]
    organism_url = d["organism"]["url_name"]
    taxid = d["organism"]["taxonomy_id"]
    species_taxid = d["organism"]["species_taxonomy_id"]
    assembly = d["assembly"]["assembly_default"]
    is_reference = d["organism"]["is_reference"]
    strain = d["organism"]["strain"]
    taxid2name = ncbi.get_taxid_translator([int(taxid)])
    ncbi_name = taxid2name[taxid]
    lineage = ncbi.get_lineage(int(taxid))
    ncbi_taxid = lineage[-1]
    if genus_taxid in lineage:
        dbbreak = db.rstrip('\n').split('_')
        #print(dbbreak[:3])
        ftp_url = url+'/'+dbbreak[0]+'_'+dbbreak[1]+'_'+dbbreak[2]+'/'+organism_url+'/pep/*.gz'
        #ftp_url = '{}/{}_{}_{}/{}/pep/*.gz'.format(dbbreak[0], dbbreak[1], dbbreak[2], organism_url)
        #print(ftp_url)
        subprocess.call("wget "+ftp_url.lower(), shell=True)

        # Establish the name of downloaded file
        for f in os.listdir('./'):
            if f.startswith(organism_url) and f.endswith('.fa.gz'):
                downloaded_file = f
										 
				                 

        directory1_path = './{}.{}/'.format(genus_taxid, "Bacillus")
        directory2_name = '{}'.format(ncbi_taxid)
        directory3_name = '{}.{}.{}'.format(ncbi_taxid, organism_id, organism_url)
        
        directory3_path = os.path.join(directory1_path, directory2_name, directory3_name)
        if not os.path.exists(directory3_path):
            os.makedirs(directory3_path)
            
        cmd = 'mv {} {}'.format(downloaded_file, directory3_path)
        os.system(cmd)
        cmd1 = 'gunzip '+directory3_path+'/'+downloaded_file
        os.system(cmd1)
        print(str(genus_taxid)+'***'+str(ncbi_taxid)+'***'+str(organism_id)+'***'+downloaded_file+'***'+directory3_path)
        
oh.write('{}****{}****{}'.format(organism_id, organism_url, directory3_path))
