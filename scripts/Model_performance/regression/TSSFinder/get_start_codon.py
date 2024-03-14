import re
from collections import defaultdict, namedtuple

record = namedtuple('record', ['chr','source', 'type','start', 'end', 'score', 'strand', 'phase', 'attribute'])

def utr3_type(file_format):
    '''
    parameter:
     file_format: the file format of genome annotation file 
                  for creating database
    return: 
     utr3 type string
    '''
    if file_format == 'gff':
        return 'three_prime_UTR'
    elif file_format == 'gtf':
        # return 'three_prime_utr'
        return 'three_prime_UTR'
    else:
        sys.stderr.write("parameter --style/-s should be assign \n")
        sys.exit(1)

def utr5_type(file_format):
    '''
    parameter:
     file_format: the file format of genome annotation file 
                  for creating database
    return:
     utr5 type string
    '''
    if file_format == 'gff':
        return 'five_prime_UTR'
    elif file_format == 'gtf':
        # return 'five_prime_utr'
        return 'five_prime_UTR'
    else:
        sys.stderr.write("parameter --style/-s should be assign \n")
        sys.exit(1)

def gff_feature_dict(file_path, file_type):
    """
    parse gff genome feature file
      param: 
          file_path: gff/gtf path
          file_type: gff or gtf
      return:
          feature dict
          transcript2gene dict
    """
    t_pat = re.compile(r'ID=(\S+?);')
    g_pat = re.compile(r'Parent=(\S+?);')
    five_prime = utr5_type(file_type)
    three_prime = utr3_type(file_type)
    g_dict = dict()
    t2g = dict()
    all_gene = set()
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip()
            if not line.endswith(";"):
                line = line + ';'
            array = line.split('\t')
            array[3], array[4] = int(array[3]), int(array[4])
            f_type = array[2]
            if 'gene' in f_type:
                gene = t_pat.search(array[8]).group(1)
                if not g_dict.get(gene):
                    g_dict[gene] = defaultdict(dict)
                    g_dict[gene]['gene'] = record._make(array)
                else:
                    if not g_dict[gene].get('gene'):
                        g_dict[gene]['gene'] = record._make(array)
            if f_type == 'miRNA':
                continue
            if 'RNA' in f_type or 'transcript' in f_type:
                if 'gene' in f_type:
                    continue
                ts = t_pat.search(array[8]).group(1)
                gene = g_pat.search(array[8]).group(1)
                t2g[ts] = gene
                all_gene.add(gene)
                if not g_dict.get(gene):
                    g_dict[gene] = defaultdict(dict)
                    g_dict[gene][ts] = defaultdict(dict)
                else:
                    g_dict[gene][ts] = defaultdict(dict)
                g_dict[gene][ts]["mRNA"] = record._make(array)
                g_dict[gene][ts]["CDS"] = []
                g_dict[gene][ts]["exon"] = []
                g_dict[gene][ts][five_prime] = []
                g_dict[gene][ts][three_prime] = []
            elif f_type == 'CDS':
                tss = g_pat.search(array[8]).group(1)
                for ts in tss.split(','):
                    if g_dict.get(ts):
                        continue
                    if not t2g.get(ts):
                        continue
                    gene = t2g[ts]
                    if gene not in all_gene:
                        continue
                    g_dict[gene][ts]["CDS"].append(record._make(array))
            elif f_type == 'exon':
                tss = g_pat.search(array[8]).group(1)
                for ts in tss.split(','):
                    if g_dict.get(ts):
                        continue
                    if not t2g.get(ts):
                        continue
                    gene = t2g[ts]
                    if gene not in all_gene:
                        continue
                    if not g_dict[gene][ts].get('exon'):
                        g_dict[gene][ts]["exon"] = []
                    g_dict[gene][ts]["exon"].append(record._make(array))
            elif f_type == five_prime:
                tss = g_pat.search(array[8]).group(1)
                for ts in tss.split(','):
                    if not t2g.get(ts):
                        continue
                    gene = t2g[ts]
                    if gene not in all_gene:
                        continue
                    g_dict[gene][ts][five_prime].append(record._make(array))
            elif f_type == three_prime:
                tss = g_pat.search(array[8]).group(1)
                for ts in tss.split(','):
                    if not t2g.get(ts):
                        continue
                    gene = t2g[ts]
                    if gene not in all_gene:
                        continue
                    g_dict[gene][ts][three_prime].append(record._make(array))
            elif f_type == 'stop_codon':
                g_dict[gene][ts]['stop_codon'] = record._make(array)
            else:
                pass
    # check
    for g in g_dict:
        for t in g_dict[g]:
            if t == 'gene':
                continue
            if not g_dict[g][t].get('mRNA'):
                g_dict[g][t]['mRNA'] = g_dict[g]['gene']
    return g_dict, t2g


# 坐标信息来至于 aS_aTSS_isoform_Arabidopsis.gff
# g_dict, t2g = gff_feature_dict('All_isoforms_Arabidopsis.gff', 'gff')
g_dict, t2g = gff_feature_dict('aS_aTSS_isoform_Arabidopsis.gff', 'gff')
# g_dict, t2g = gff_feature_dict('/home/zhusitao/AI/TSS_Predict/ath/TSARC_TSSPlant_TransPrise/TSSFinder/ath/output_athaliana.model_1/Araport11_GFF3_genes_transposons.Mar92021.gff', 'gff')

# g_dict, t2g = gff_feature_dict('aS_isoform_Arabidopsis.gff', 'gff')
# g_dict, t2g = gff_feature_dict('Araport11_GFF3_genes_transposons.Mar92021.gff', 'gff')
cc = 0
with open('ath_start_codons.bed', 'w') as out, open('tss_start_codon.txt', 'w') as out2, open('tss_start_end.txt', 'w') as out3:
    for gene in g_dict.keys():
        for transcript in g_dict[gene].keys():
            if transcript == "gene":
                continue
            mRNA = g_dict[gene][transcript]['mRNA']
            strand = mRNA.strand
            if not g_dict[gene][transcript].get('CDS'):
                continue
            if strand == '-':
                start_codon = g_dict[gene][transcript]['CDS'][-1].end
                print(*[mRNA.chr, start_codon, start_codon+1, transcript, 1, strand], file=out, sep='\t')
                print(*[mRNA.chr, mRNA.end, start_codon, transcript, strand], file=out2, sep='\t')
                print(*[mRNA.chr, mRNA.start, mRNA.end, transcript, strand], file=out3, sep='\t')
            else:
                start_codon = g_dict[gene][transcript]['CDS'][0].start
                print(*[mRNA.chr, start_codon, start_codon+1, transcript, 1, strand], file=out, sep='\t')
                print(*[mRNA.chr, mRNA.start, start_codon, transcript, strand], file=out2, sep='\t')
                print(*[mRNA.chr, mRNA.start, mRNA.end, transcript, strand], file=out3, sep='\t')
