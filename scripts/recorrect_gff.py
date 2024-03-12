#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: recorrect_gff.py
date: 2022/2/15 3:43 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

import re 
from collections import OrderedDict

#gene_id "MSTRG.1"; transcript_id "AT1G01010.1"; ref_gene_id "AT1G01010";


def gene_id(string):
    patt = re.compile(r'gene_id "(\S+)";')
    searched = patt.search(string)
    return searched.group(1)

def transcript_id(string):
    patt = re.compile(r'transcript_id "(\S+)";')
    searched = patt.search(string)
    return searched.group(1)


def ref_gene_id(string):
    patt = re.compile(r'ref_gene_id "(\S+)";')
    searched = patt.search(string)
    if searched:
        return searched.group(1)
    else:
        return None

def long_ts(a_dict):
    max_len = 0
    max_id = None
    for ts in a_dict.keys():
        length = a_dict[ts][1] - a_dict[ts][0]
        if max_len < length:
            max_len = length
            max_id = ts
    return max_id, a_dict[max_id]

def adjacent_ts(a_dict, max_region):
    switch = False
    for ts in a_dict.keys():
        start, end = a_dict[ts]
        if max_region[0] <= start and end <= max_region[1]:
            switch = True
    return switch

def overlap_range(x, y):
    assert isinstance(x, list)
    assert isinstance(y, list)
    x_set = set(range(x[0], x[1]+1))
    y_set = set(range(y[0], y[1]+1))
    intersect = x_set.intersection(y_set)
    ratio = len(intersect)/len(y_set)
    if ratio >= 0.4 :
        return True
    else:
        return False


ts = []
od = dict()
for chrom in ['Chr1', 'Chr2', 'Chr3', 'Chr4', 'Chr5', 'ChrC', 'ChrM']:
    od[chrom] = OrderedDict()


i = 0 
with open('ath_merge.gtf', 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            continue
        arr = line.split('\t')
        if arr[2] == "transcript":
            #print(line)
            chrom = arr[0]
            start = int(arr[3])
            end = int(arr[4])
            gene = gene_id(line)
            transcript = transcript_id(line)
            ref_gene = ref_gene_id(line)
            #print(gene,transcript)
            #if ref_gene is not None:
            #    continue
            if od[chrom].get(gene):
                od[chrom][gene][transcript] = [start,end] 
            else:
                od[chrom][gene] = {transcript:[start,end]}
            i += 1 
            #if i == 200:
            #    break 
#print(od)

for chrom in od.keys():
    gene_list = list(od[chrom].keys())
    for i,key in enumerate(od[chrom].keys()):
        if i == 0 :
            continue
        if i == len(gene_list)-1:
            continue
        dict_before = od[chrom][gene_list[i-1]]
        # sb, eb = long_ts(dict_before)[1]
        a_dict = od[chrom][key]
        max_id = long_ts(a_dict)[0]
        s, e = long_ts(a_dict)[1]
        dict_after = od[chrom][gene_list[i+1]]
        # sa, ea = long_ts(dict_after)[1]
        if "AT" in max_id:
            continue
        if adjacent_ts(dict_before, [s, e]) or adjacent_ts(dict_after, [s, e]):
            print(max_id)
        #if overlap_range([s,e],[sb,eb]) : #or overlap_range([s, e], [sa, ea]):
        #    print(max_id)
