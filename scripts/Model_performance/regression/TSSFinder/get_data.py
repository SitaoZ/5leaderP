# All_isoforms_Arabidopsis.gff 用的是最新的，
# 因此其他三个软件需要去除12个转录本

tss_codon = dict()
with open('tss_start_codon.txt', 'r') as f:
    for line in f:
        # Chr1    3631    3760    AT1G01010.1     +
        # chrom tss start_codon locus strand
        line = line.strip()
        array = line.split('\t')
        tss_codon[array[3]] = array
i = 0
# mRNA.chr, start_codon, start_codon+1, transcript, 1, strand
with open('predict_peak.csv', 'r') as f, open('input_predict.bed', 'w') as out:
    for line in f.readlines()[1:]:
        line = line.strip()
        array = line.split(',')
        ts = array[5]
        if tss_codon.get(ts):
            pass
            chrom, tss, start_codon, locus, strand = tss_codon[ts]
            start_codon = int(start_codon)
            # out.write("\t".join([chrom, str(start_codon), str(start_codon+1), locus, '1', strand])+'\n')
            out.write("\t".join([chrom, str(start_codon-1), str(start_codon), locus, '1', strand])+'\n') # bed position
        else:
            print(ts)
            i += 1
       
print(i)
