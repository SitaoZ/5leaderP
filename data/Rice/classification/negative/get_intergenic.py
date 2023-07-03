import random
import pandas as pd 
from Bio import SeqIO
from Bio.Seq import Seq

random.seed(1)

def reverse_comp(seq):
    s = Seq(seq)
    s_rc = str(s.reverse_complement())
    return s_rc
    
fasta = {}
for record in SeqIO.parse('msu7.fa', 'fasta'):
    fasta[record.id] = str(record.seq)



genome = {}
with open('All_isoforms_V1.0.gff', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip() 
        if len(line) == 0:
            continue
        array = line.split('\t')
        if array[2] == 'gene':
            start, end = int(array[3]), int(array[4])
            gene_id = array[8].split(";")[0].replace('ID=', '')
            strand = array[6]
            if array[0] not in genome.keys():
                genome[array[0]] = [(gene_id, start, end, strand)]
            else:
                genome[array[0]].append((gene_id, start, end, strand))

threshold = 512
out = open('negative_data.csv', 'w')
for chrom in genome.keys():
    gene_list = genome[chrom]
    for i in range(len(gene_list)):
        gene = gene_list[i]
        strand = gene[3]
        if i == 0 :
            if strand == '+':
                # start
                intergenic = gene[1] - 0
                if intergenic > 2*threshold:
                    if (intergenic - 3*threshold) > 0:
                        r_start = gene[1] - 3*threshold
                        if r_start-512 < 0: continue
                        for r in random.sample(range(r_start-512, r_start), 3):
                            seq = fasta[chrom][r : r+512]
                            out.write('first_gene'+gene[0]+","+seq+"\n")
            else:
                # reverse and end 
                right = gene_list[i+1]
                intergenic = right[1] - gene[2]
                if intergenic > 2*threshold:
                    if (intergenic - 3*threshold) > 0:
                        r_start = gene[2] + 3*threshold
                        for r in random.sample(range(r_start, r_start+512), 3):
                            if r - 512 < 0:
                                continue
                            seq = fasta[chrom][r-512 : r]
                            seq = reverse_comp(seq)
                            out.write('first_gene_reverse'+gene[0]+","+seq+"\n")
        elif i == len(gene_list) - 1:
            if strand == "+":
                # start
                left = gene_list[i-1]
                # intergenic = len(fasta[chrom]) - gene[1]
                intergenic = gene[1] - left[2]
                if intergenic > 2*threshold:
                    if (intergenic - 3*threshold) > 0:
                        r_start = gene[1] - 3*threshold
                        for r in random.sample(range(r_start-512, r_start), 3):
                            seq = fasta[chrom][r : r+512]
                            out.write('last_gene'+gene[0]+","+seq+"\n")
            else:
                intergenic = len(fasta[chrom]) - gene[1]
                if intergenic > 2*threshold:
                    if (intergenic - 3*threshold) > 0:
                        r_start = gene[2] + 3*threshold
                        if r_start > len(fasta[chrom]):
                            continue
                        for r in random.sample(range(r_start, r_start+512), 3):
                            seq = fasta[chrom][r-512 : r]
                            seq = reverse_comp(seq)
                            out.write('last_gene_reverse'+gene[0]+","+seq+"\n")
        else:
            if strand == "+": 
                # start 
                left = gene_list[i-1]
                intergenic = gene[1] - left[2]
                if intergenic > 2*threshold:
                    if (intergenic - 3*threshold) > 0:
                        r_start = gene[1] - 3*threshold
                        for r in random.sample(range(r_start-512, r_start), 3):
                            seq = fasta[chrom][r : r+512]
                            out.write(left[0]+"_"+gene[0]+","+seq+"\n")
            else:
                right = gene_list[i+1]
                intergenic = right[1] - gene[2]
                if intergenic > 2*threshold:
                    if (intergenic - 3*threshold) > 0:
                        r_start = gene[2] + 3*threshold
                        for r in random.sample(range(r_start, r_start+512), 3):
                            seq = fasta[chrom][r-512 : r]
                            seq = reverse_comp(seq)
                            out.write(gene[0]+"_"+right[0]+","+seq+"\n")
out.close()
