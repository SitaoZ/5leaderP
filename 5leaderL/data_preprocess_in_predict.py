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
    parser.add_argument('-o', '--output_file_path', type=str,
                        help='output file for TSAR predict')
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
         out.write("Locus,Strand,Start,End,Seq\n")
         for line in f:
             line = line.strip()
             # chrom, start, end, name, ., strand
             arr = line.split('\t')
             chrom, start, end = arr[0], int(arr[1]), int(arr[2])
             ts_id, strand = arr[3], arr[5]
             if strand == '+':
                 if start + 256 > len(genome[chrom]) or start - 256 < 0:
                     continue
                 seq = genome[chrom][start-256 : start+256]
             else:
                 if end + 256  > len(genome[chrom]) or end - 256 < 0 :
                     continue
                 seq = genome[chrom][end-256 : end+256]
                 seq = str(Seq(seq).reverse_complement())
             outline = ",".join([ts_id, strand, str(start), str(end), seq])
             out.write(outline+'\n')

if __name__ == '__main__':
    main()
