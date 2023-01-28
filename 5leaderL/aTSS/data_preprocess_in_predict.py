import random
import argparse 
import numpy as np 
import pandas as pd 
from Bio import SeqIO
from Bio.Seq import Seq

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of aTSS Predict')

    parser.add_argument('-b', '--transcript_bed_file', type=str,
                        help='transcript bed file contians chrom, start, end, name, ., strand')
    parser.add_argument('-g', '--genome_fasta_file', type=str,
                        help='genome fasta file')
    parser.add_argument('-s', '--sample_size',default=4, type=int,
                        help='sample selection size (default: 4)')
    parser.add_argument('-o', '--output_file_path', type=str,
                        help='output file for aTSS predict')
    return parser.parse_args()


def seqFilter(seq, chars=['N','Y','S','K','R','W']):
    """
    Remove none[ATGC] characters
    :param seq: sequence
    :param Non_chars: character removed
    :return:
    """
    if any(char in seq for char in chars):
        # contain all non char
        return False
    else:
        # not contain
        return True

def seq2matrix(seq):
    """
    ATGC sequence to one hot matrix
    :param seq: sequence
    :return: numpy matrix
    """
    matrix = np.zeros((4, len(seq)))
    seq = seq.upper()
    for pos in range(len(seq)):
        if seq[pos] == 'A':
            matrix[0, pos] = 1
        elif seq[pos] == 'C':
            matrix[1, pos] = 1
        elif seq[pos] == 'G':
            matrix[2, pos] = 1
        elif seq[pos] == 'T':
            matrix[3, pos] = 1
        else:
            continue
    return matrix

def readGenome(path):
    genome = {}
    for record in SeqIO.parse(path, 'fasta'):
        chrom = record.id
        seq = str(record.seq)
        genome[chrom] = seq
    return genome


def main():
    random.seed(11)
    config = parse_args()
    print(config)
    genome = readGenome(config.genome_fasta_file)
    with open(config.transcript_bed_file, 'r') as f, open(config.output_file_path, 'w') as out:
         out.write("Locus,Seq,Label,Start,End\n")
         for line in f:
             line = line.strip()
             # chrom, start, end, name, ., strand
             arr = line.split('\t')
             chrom, start, end = arr[0], int(arr[1]), int(arr[2])
             ts_id, strand = arr[3], arr[5]
             for i in random.sample(range(50, 150), config.sample_size):
             # for i in [150]: #random.sample(range(1, 150), config.sample_size):
             # for i in [139, 143, 87, 109]:
                 label = i
                 if strand == '+':
                     p = start - i
                     if p < 0 :
                         break 
                     if p + 512 > len(genome[chrom]):
                         break 
                     seq = genome[chrom][p : p+512]
                 else:
                     p = end + i
                     if p - 512 <0:
                         break
                     if p > len(genome[chrom]):
                         break 
                     seq = genome[chrom][p-512 : p]
                     seq = str(Seq(seq).reverse_complement())
                 outline = ",".join([ts_id, seq, str(label), str(start), str(end)])
                 out.write(outline+'\n')

if __name__ == '__main__':
    main()
