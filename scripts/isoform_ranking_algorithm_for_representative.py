#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: get_abundance_transcript.py
date: 2022/3/30 4:54 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''


import os
import glob
import pandas as pd

def t2g():
    gff_path = '/home/zhusitao/database/plant/ath/merge_gff/01.merge/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/GeneID/All_isoforms_V1.0_GeneID_transformed.gff'
    tr2gene = dict()
    with open(gff_path, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            arr = line.split('\t')
            if 'RNA' in arr[2] or 'transcript' in arr[2]:
                a = arr[8].split(";")
                tr, gene = a[0], a[1]
                tr = tr.replace('ID=', '')
                gene = gene.replace('Parent=', '')
                if not tr2gene.get(tr):
                    tr2gene[tr] = gene
    return tr2gene

def oneSample(filePath):
    sample = pd.read_csv(filePath, sep='\t')
    filePath = os.path.basename(filePath)
    sample_id = filePath.replace('.isoforms.results','')
    dfs = []
    for gene, group in sample.groupby(by = 'gene_id'):
        group = group.sort_values(by=['FPKM'], ascending=True) # 首先组内从小到大排列
        # group.loc[:,sample_id] = range(1, group.shape[0]+1)
        # 同一个基因的不同转录本整体在82个样本中整体排布，根据轶和的定义排列，同组的相同的值
        group.loc[:,sample_id] = group['FPKM']
        dfs.append(group)
    out = pd.concat(dfs)
    return out[['transcript_id',sample_id]]

def kw_rank(df, tr2gene):
    """实现轶和检验的排序（轶次）"""
    df = df.drop(['gene_id'], axis=1)
    values_id = df.columns[1:]
    df = pd.melt(df, id_vars=['transcript_id'], value_vars=values_id) 
    # df.loc[:,'gene_id'] = df.transcript_id.apply(lambda x : x.split('.')[0])
    df.loc[:,'gene_id'] = df.transcript_id.apply(lambda x : tr2gene[x])
    df.loc[:,"rank"] = df.groupby('gene_id')['value'].rank()
    df = df[['transcript_id', 'variable', 'rank']]
    df = (df.pivot_table(index=['transcript_id'], columns='variable', values='rank').reset_index())
    return df 


def sampleThreshold(data_frame, tr2gene):
    shape = data_frame.shape
    # data_frame.loc[:,'gene_id'] = data_frame.transcript_id.apply(lambda x:x.split('.')[0])
    data_frame.loc[:,'gene_id'] = data_frame.transcript_id.apply(lambda x: tr2gene[x])
    out = pd.DataFrame()
    for gene, group in data_frame.groupby(by = 'gene_id'):
        group = kw_rank(group, tr2gene)
        out = pd.concat([group, out], axis=0)
    return out

def samplePath(Paths):
    files = glob.glob(Paths)
    return files

def integrateSample(sampleFiles):
    tr2gene = t2g()
    total = pd.DataFrame(columns=['transcript_id'])
    for sample in sampleFiles:
        sample_df = oneSample(sample)
        total = total.merge(sample_df, on = 'transcript_id', how='outer')
    total = total.fillna(0)
    # threshold 80%
    total = sampleThreshold(total, tr2gene)
    total.loc[:,'Rank'] = total.iloc[:,1:].sum(axis=1)
    # total.loc[:, 'gene_id'] = total.transcript_id.apply(lambda x:x.split('.')[0])
    total.loc[:, 'gene_id'] = total.transcript_id.apply(lambda x: tr2gene[x])
    # add Index column
    dfs = []
    for gene, group in total.groupby(by = 'gene_id'):
        group = group.sort_values(by=['Rank'], ascending=False) # 首先组内从大到小排列, Rank越大，index越高(值越小)，频率越高
        group.loc[:,'Index'] = range(1, group.shape[0]+1)
        # 同一个基因的不同转录本整体在82个样本中整体排布，根据轶和的定义排列，同组的相同的值，相同的值取平均轶
        dfs.append(group)
    total = pd.concat(dfs)
    total.to_csv('zz_kw_whole_transcripts_rank.csv', index=False)
    # represent
    total = pd.read_csv('zz_kw_whole_transcripts_rank.csv')
    represent = total.iloc[total.groupby('gene_id')['Rank'].idxmax()]
    represent.to_csv('zz_kw_represent_transcripts.csv', index=False)



def main():
    Paths = '../pysradb_downloads_*/*/*/assemble/13.All_isoforms_rsem/*.isoforms.results.M'
    sampleFiles = samplePath(Paths)
    print('样本数：',len(sampleFiles))
    integrateSample(sampleFiles)



if __name__ == '__main__':
    main()
