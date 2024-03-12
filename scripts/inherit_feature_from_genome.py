#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: inherit_feature_from_genome.py
date: 2022/2/13 4:54 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

import re
import pandas as pd 
from collections import defaultdict

"""
$ less araport11.gff | awk '$3!="CDS"' | awk '$3!="exon"' | grep -v "^#" | grep AT5G52797.1
Chr5	Araport11	miRNA	21395545	21395565	.	-	.	ID=AT5G52797.1;geneID=AT5G52797
Chr5	Araport11	miRNA	21395604	21395624	.	-	.	ID=AT5G52797.1;geneID=AT5G52797
(base) zhusitao@localhost 20:12:06  ^w^ /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_lift  
$ less araport11.gff | awk '$3!="CDS"' | awk '$3!="exon"' | grep -v "^#" | grep ATMG00650.1
ChrM	Araport11	transcript	207580	215562	.	-	.	ID=ATMG00650.1;geneID=ATMG00650
ChrM	Araport11	transcript	361637	361939	.	+	.	ID=ATMG00650.1;geneID=ATMG00650
(base) zhusitao@localhost 20:12:17  ^w^ /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_lift  
$ less araport11.gff | awk '$3!="CDS"' | awk '$3!="exon"' | grep -v "^#" | grep ATMG01170.1
ChrM	Araport11	transcript	49423	50580	.	+	.	ID=ATMG01170.1;geneID=ATMG01170
ChrM	Araport11	transcript	264467	265516	.	-	.	ID=ATMG01170.1;geneID=ATMG01170
(base) zhusitao@localhost 20:12:26  ^w^ /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_lift  
$ less araport11.gff | awk '$3!="CDS"' | awk '$3!="exon"' | grep -v "^#" | grep ATMG01275.1
ChrM	Araport11	transcript	58315	234132	.	+	.	ID=ATMG01275.1;geneID=ATMG01275
ChrM	Araport11	transcript	82935	83321	.	-	.	ID=ATMG01275.1;geneID=ATMG01275
(base) zhusitao@localhost 20:12:35  ^w^ /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_lift  
$ less araport11.gff | awk '$3!="CDS"' | awk '$3!="exon"' | grep -v "^#" | grep ATMG01320.1
ChrM	Araport11	transcript	92819	98042	.	-	.	ID=ATMG01320.1;geneID=ATMG01320
ChrM	Araport11	transcript	161832	163357	.	+	.	ID=ATMG01320.1;geneID=ATMG01320
"""

def get_gene_id(string):
    return string.split(';')[1].replace('geneID=', '')

def get_ts_id(string):
    return string.split(';')[0].replace('ID=', '')

gff_path = 'araport11.gff'
ts_feature = dict() # 记录每个转录本在基因组注释文件中的注释类比（mRNA, miRNA ...） 
refer_cds = dict()  # 记录注释文件中每个transcript的CDS, 保留的是GFF中CDS的全部信息
# 记录每个转录本的基因和注释类型
with open(gff_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        arr = line.split('\t')
        if arr[2] == "exon":
            continue
        if arr[2] == "CDS":
            # Parent=AT1G01010.1
            name = arr[8].replace('Parent=', '')
            if refer_cds.get(name):
                refer_cds[name].append(arr)
            else:
                refer_cds[name] = [arr]
            continue
        # ID=AT1G01010.1;geneID=AT1G01010
        feature = arr[2]
        gene = get_gene_id(arr[8])
        ts = get_ts_id(arr[8])
        if not ts_feature.get(ts):
            ts_feature[ts] = (gene, feature)
        else:
            ts_feature[ts] = (gene, feature)

assembly_feature = dict()
# gffcompare info 记录匹配关系
# 匹配关系中是x和s的不能继承(方向相反了)
geneid_transform = dict() # 记录参考基因ID和组装基因ID的字典
tsid_transform = dict() # 记录transcript id的转换关系

# MSTRG.x 基因id和 AT基因id相互均存在 一对多的现象
# e.g. AT1G01620, MSTRG.71
compare_info = 'gffcompare.ath_final.gtf.tmap'
with open(compare_info, 'r') as f:
    for line in f.readlines()[1:]:
        line = line.strip()
        # ref_gene_id     ref_id  class_code      qry_gene_id     qry_id
        # AT1G01010       AT1G01010.1     =       MSTRG.1 AT1G01010.1
        arr = line.split('\t')
        class_code = arr[2] # 用于 class_code s x的过滤
        ref_gene_id, ref_id = arr[0], arr[1]
        qry_gene_id, qry_id = arr[3], arr[4]
        if not assembly_feature.get(qry_id):
            if ts_feature.get(ref_id):
                # 如果ref_id已经存在 (class code 为非u的)
                assembly_feature[qry_id] = (qry_gene_id, ts_feature[ref_id][1], class_code) 
                # gene_id, feature; ts_feature[ts] = (gene, feature)
            else:
                # - 比较对象的class code u
                assembly_feature[qry_id] = (qry_gene_id, ref_id, class_code) # gene_id, refer_id
        else:
            pass
        # ts 对应关系已经验证，全部是一一对
        if not tsid_transform.get(qry_id):
            tsid_transform[qry_id] = [ref_gene_id, ref_id, class_code, qry_gene_id]
        # qry_gene_id 一对多, 除去strand相反的，相反的不能继承
        if class_code not in ['x', 's', 'k']:
            if not geneid_transform.get(qry_gene_id):
                geneid_transform[qry_gene_id] = [ref_gene_id]
            else:
                geneid_transform[qry_gene_id].append(ref_gene_id)

print('geneid_transform =,', len(geneid_transform))

def gene_id_gtf(string):
    # transcript_id "AT1G01010.1"; gene_id "MSTRG.1"
    patt = re.compile(r'gene_id "(\S+)"')
    matched = patt.search(string)
    return matched.group(1)

def ts_id_gtf(string):
    # transcript_id "AT1G01010.1"; gene_id "MSTRG.1"
    patt = re.compile(r'transcript_id "(\S+)";')
    matched = patt.search(string)
    return matched.group(1)


# inherit feature to ath_final.gtf
assembly_gene = dict() # 记录组装出来的基因的区间大小[最左边，最右边]
assembly_geneid = dict() # 该字典没有使用, 写程序测试时用过
to_ath_geneid = dict()   # 该字典没有使用, 写程序测试时用过
assembly_exon = dict() # 记录组装出来的exon信息，GFF中的exon整行信息
assembly_gtf = 'ath_final.gtf'
# 获取gene region基因信息，最长区间
with open(assembly_gtf, 'r') as f:
    # get gene region info (longest transcript position)
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        arr = line.split('\t')
        gene = gene_id_gtf(arr[8])
        strand = arr[6]
        start, end = int(arr[3]), int(arr[4])
        ts = ts_id_gtf(arr[8])
        if arr[2] == 'transcript':
            geneid_from_ts = ".".join(ts.split('.')[:-1])
            if assembly_gene.get(gene):
                if start < assembly_gene[gene][0]:
                    assembly_gene[gene][0] = start
                if end > assembly_gene[gene][1]:
                    assembly_gene[gene][1] = end
            else:
                assembly_gene[gene] = [start, end]
            # assembly_geneid 包括 AT和MSTRG开头的
            if assembly_geneid.get(gene):
                tg = ".".join(ts.split('.')[:-1])
                assembly_geneid[gene].add(tg)
            else:
                tg = ".".join(ts.split('.')[:-1])
                assembly_geneid[gene] = {tg}
        else:
            # exon 
            if assembly_exon.get(ts):
                assembly_exon[ts].append(arr)
            else:
                assembly_exon[ts] = [arr] 
    ii = 0
    for gene in assembly_geneid.keys():
        if len(assembly_geneid[gene]) == 1:
            # AT or MTSRG
            to_ath_geneid[gene] = list(assembly_geneid[gene])[0]
        else:
            # both AT and MTSRG exist or two AT exist
            # e.g. MSTRG.2 {'AT1G01020', 'AT1G01030'} 
            pass


# gene CDS exon UTR from transcoder
trans_decoder_dict = dict() # transcoder 预测的全部信息 gene:mRNA/CDS/exon/utr
ts2gene = dict()
gene_dict = dict()
with open('../../../../04.decoder/transdecoder/transdecoder.gff3', 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue
        arr = line.split('\t')
        if arr[2] == 'gene':
            #ID=AT1G02228;
            gene_id = arr[8].split(";")[0].replace("ID=", "")
            if not trans_decoder_dict.get(gene_id):
                trans_decoder_dict[gene_id] = defaultdict(dict)
            arr[8] = arr[8].split(";")[0]
            gene_dict[gene_id] = arr
        if arr[2] == 'mRNA':
            # ID=AT1G02228.1.p1;Parent=AT1G02228;
            arr[8] = ';'.join(arr[8].split(";")[:2])
            gene_id = arr[8].split(";")[1].replace("Parent=", "")
            ts_id = arr[8].split(";")[0].replace("ID=", "")
            # replace p.1
            ts_id = re.sub(".p\d", "", ts_id)
            if gene_id in trans_decoder_dict.keys():
                trans_decoder_dict[gene_id][ts_id] = defaultdict(dict)
                trans_decoder_dict[gene_id][ts_id]['mRNA'] = arr
                ts2gene[ts_id] = gene_id
                trans_decoder_dict[gene_id][ts_id]["CDS"] = []
                trans_decoder_dict[gene_id][ts_id]["exon"] = []
                trans_decoder_dict[gene_id][ts_id]["five_prime_UTR"] = []
                trans_decoder_dict[gene_id][ts_id]["three_prime_UTR"] = []
        if arr[2] == 'five_prime_UTR':
            # ID=AT1G06357.1.p1.utr5p1;Parent=AT1G06357.1.p1
            utr5_id = arr[8].split(";")[0].replace("ID=", "")
            ts_id = arr[8].split(";")[1].replace("Parent=", "")
            # replace p.1
            ts_id = re.sub(".p\d", "", ts_id)
            gene_id = ts2gene[ts_id]
            if trans_decoder_dict.get(gene_id):
                if trans_decoder_dict[gene_id].get(ts_id):
                    trans_decoder_dict[gene_id][ts_id]["five_prime_UTR"].append(arr)

        if arr[2] == 'three_prime_UTR':
            # ID=AT1G06357.1.p1.utr3p1;Parent=AT1G06357.1.p1
            utr3_id = arr[8].split(";")[0].replace("ID=", "")
            ts_id = arr[8].split(";")[1].replace("Parent=", "")
            # replace p.1
            ts_id = re.sub(".p\d", "", ts_id)
            gene_id = ts2gene[ts_id]
            if trans_decoder_dict.get(gene_id):
                if trans_decoder_dict[gene_id].get(ts_id):
                    trans_decoder_dict[gene_id][ts_id]["three_prime_UTR"].append(arr)

        if arr[2] == 'CDS':
            # ID=cds.AT1G04143.1.p1;Parent=AT1G04143.1.p1
            cds_id = arr[8].split(";")[0].replace("ID=", "")
            ts_id = arr[8].split(";")[1].replace("Parent=", "")
            # replace p.1
            ts_id = re.sub(".p\d", "", ts_id)
            gene_id = ts2gene[ts_id]
            if trans_decoder_dict.get(gene_id):
                if trans_decoder_dict[gene_id].get(ts_id):
                    trans_decoder_dict[gene_id][ts_id]["CDS"].append(arr)
        if arr[2] == 'exon':
            # ID=AT1G06357.1.p1.exon1;Parent=AT1G06357.1.p1
            exon_id = arr[8].split(";")[0].replace("ID=", "")
            ts_id = arr[8].split(";")[1].replace("Parent=", "")
            # replace p.1
            ts_id = re.sub(".p\d", "", ts_id)
            gene_id = ts2gene[ts_id]
            if trans_decoder_dict.get(gene_id):
                if trans_decoder_dict[gene_id].get(ts_id):
                    trans_decoder_dict[gene_id][ts_id]["exon"].append(arr)


print('MSTRG.4 ',trans_decoder_dict['MSTRG.4'])

def overlap_range(x, y):
    assert isinstance(x, list)
    assert isinstance(y, list)
    x_set = set(range(x[0], x[1]+1))
    y_set = set(range(y[0], y[1]+1))
    if y_set.issubset(x_set):
        return True
    else:
        return False

def add_five_prime_utr(exons, cdss, strand):
    # exons, cdss is 2D list
    # CDS is subset of exon
    exon_position = []
    for exon in exons:
        start, end = int(exon[3]), int(exon[4])
        exon_position.append([start, end])
    exon_position = sorted(exon_position, key=lambda e: e[0]) # min -> max
    cds_position = []
    for cds in cdss:
        start, end = int(cds[3]), int(cds[4])
        cds_position.append([start, end])
    cds_position = sorted(cds_position, key=lambda c: c[0])   # min -> max
    utr5_position = []
    if strand == "+":
        for i,exon in enumerate(exon_position):
            cds_init = cds_position[0]
            cds_end = cds_position[-1]
            if overlap_range(exon, cds_init) is True:
                # cds region is subset of exon region
                if exon[0] == cds_init[0]:
                    # no utr5
                    pass
                else:
                    utr5_position.append([exon[0], cds_init[0]-1])
                break
            else:
                utr5_position.append(exon)
    else:
        for i,exon in enumerate(exon_position[::-1]):
            cds_init =  cds_position[-1]
            cds_end = cds_position[0]
            if overlap_range(exon, cds_init) is True:
                if exon[1] == cds_init[1]:
                    # not utr5
                    pass
                else:
                    utr5_position.append([cds_init[1]+1, exon[1]])
                break
            else:
                utr5_position.append(exon)

    return utr5_position


def add_three_prime_utr(exons, cdss, strand):
    # exons, cdss is 2D list
    # CDS is subset of exon
    exon_position = []
    for exon in exons:
        start, end = int(exon[3]), int(exon[4])
        exon_position.append([start, end])
    exon_position = sorted(exon_position, key=lambda e: e[0]) # min -> max
    cds_position = []
    for cds in cdss:
        start, end = int(cds[3]), int(cds[4])
        cds_position.append([start, end])
    cds_position = sorted(cds_position, key=lambda c: c[0])   # min -> max
    utr3_position = []
    if strand == "+":
        for i,exon in enumerate(exon_position[::-1]):
            cds_init =  cds_position[0]
            cds_end = cds_position[-1]
            if overlap_range(exon, cds_end) is True:
                # cds region is subset of exon region
                if exon[1] == cds_end[1]:
                    # no utr3
                    pass
                else:
                    utr3_position.append([cds_end[1]+1, exon[1]])
                break
            else:
                utr3_position.append(exon)
    else:
        for i,exon in enumerate(exon_position):
            cds_init =  cds_position[-1]
            cds_end = cds_position[0]
            if overlap_range(exon, cds_end) is True:
                # if exon[0] == cds_init[0]:
                if exon[0] == cds_end[0]:
                    # not utr3
                    pass
                else:
                    utr3_position.append([exon[0] ,cds_end[0]-1])
                break 
            else:
                utr3_position.append(exon)

    return utr3_position


cds_final = pd.read_csv('../../../../04.decoder/cpc2/CDS_final_list.csv', header=None) # from GFF3 stat
cds_final.columns = ['TranscriptID']
cds_final_set = set(cds_final.TranscriptID.to_list())

line_count = 0
pass_count = 0
gene_to_ref = set()
gene_to_tair = set()
gene_to_assem = set()
gene_mRNA = set()
gene_mRNA2 = set()
delete_protein = set()

def get_transcript_anno(ts_id, assembly_feature, ts_feature):
    if ts_feature.get(ts_id):
        return ts_feature[ts_id][1]
    else:
        if assembly_feature.get(ts_id):
            if assembly_feature[ts][1] != "-":
                return assembly_feature[ts_id][1]
            else:
                return 'transcript'



with open(assembly_gtf, 'r') as f, open('ath_inherit.gff', 'w') as out:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        arr = line.split('\t')
        gene = gene_id_gtf(arr[8])
        ts = ts_id_gtf(arr[8])
        geneid_from_ts = ".".join(ts.split('.')[:-1])
        strand = arr[6]
        # info from araport11
        if arr[2] == 'transcript':
            if ts in cds_final_set:
                line_count += 1
            class_code = assembly_feature[ts][2]
            # gene info 主要是边界大小的确定
            if assembly_gene.get(gene):
                gene_to_ref.add(gene)
                gene_arr = line.split('\t')
                if "AT" in gene_arr[8]:
                    # transcript_id "AT1G01010.1"; gene_id "MSTRG.1"
                    # transcript_id "AT1G03640.1"; gene_id "AT1G03640" 
                    gene_to_tair.add(gene)
                    gene_attr = gene_arr[8].split("; ")[0].replace('transcript_id ', '')
                    gene_attr = gene_attr.replace('\"', '')
                    gene_id = gene_attr.split(".")[0] # AT号 ref的和query的可能不对应，以query的为准
                    # gene_arr[8] = f"gene_id \"{gene_id}\"" # GTF format
                    gene_arr[8] = f"ID={gene};" # GFF format
                else:
                    # transcript_id "MSTRG.34790.1"; gene_id "MSTRG.34790"
                    gene_to_assem.add(gene)
                    gene_attr = gene_arr[8].split("; ")[1].replace('gene_id ', '')
                    gene_id = gene_attr.replace('\"', '')
                    gene_arr[8] = f"ID={gene_id};"
                gene_arr[2] = 'gene'
                gene_arr[3] = str(assembly_gene[gene][0])
                gene_arr[4] = str(assembly_gene[gene][1])
                del assembly_gene[gene] # only print one
                out.write("\t".join(gene_arr)+'\n')
            else:
                pass
            # mRNA info 
            gene_mRNA2.add(gene)
            # arr[2] = assembly_feature[ts][1] # transcript feature from tair
            # 转录本注释属性获取，refer中存在的注释直接用，不存在的子集赋值
            # arr[2] = assembly_feature[ts][1] if assembly_feature[ts][1] != "-" else 'transcript'
            arr[2] = get_transcript_anno(ts, assembly_feature, ts_feature)
            ref_gene_id, ref_id, class_code, qry_gene_id = tsid_transform[ts]
            mRNA_geneid = ".".join(ts.split('.')[:-1]) # 该基因id的数目不等于装出来的(MSTRG计数)数目，
            gene_mRNA.add(gene)
            arr[8] = f'ID={ts};Parent={gene};'
            out.write("\t".join(arr)+'\n')

            # exon info
            if assembly_exon.get(ts):
                for i, exon in enumerate(assembly_exon[ts], start=1):
                    if strand == "+":
                        arr[8] = f'ID={ts}:exon:{i};Parent={ts};'
                    else:
                        exon_num = len(assembly_exon[ts])
                        arr[8] = f'ID={ts}:exon:{exon_num - i + 1};Parent={ts};'
                    exon[-1] = arr[8]
                    out.write("\t".join(exon)+'\n')

            # CDS info 组装出来以AT开始的转录本，直接继承原先的CDS信息，但是要注意反向的两种class code x s不继承
            # 该情况下直接给出exon信息即可，不需要给CDS信息
            if refer_cds.get(ts):
                # from tair10
                ref_strand = refer_cds[ts][0][6] # 任选一个CDS的方向
                if strand != ref_strand:
                    continue
                if ts == 'AT5G01020.1':
                    print('AT5G01020.1 transcoder', trans_decoder_dict[gene][ts]['CDS'])
                    print('AT5G01020.1 refer', refer_cds[ts])
                # Araport中存在CDS则直接予赋CDS的注释信息
                # if ts not in cds_final_set:
                #     delete_protein.add(ts)
                #     continue
                class_code = assembly_feature[ts][2]
                if class_code in ['s', 'x']:
                    # 反向的不给CDS,UTR3/5的注释，直接跳过 组装出来的AT开头的没有s x,所以该if不会执行
                    continue
                # for i,cds in enumerate(refer_cds[ts], start=1):
                for i,cds in enumerate(sorted(refer_cds[ts], key=lambda c: int(c[3])), start=1):
                    # if to_ath_geneid.get(gene):# error
                    if strand == "+":
                        arr[8] = f'ID={ts}:CDS:{i};Parent={ts};' # GFF
                    else:
                        cds_num = len(refer_cds[ts])
                        arr[8] = f'ID={ts}:CDS:{cds_num - i + 1};Parent={ts};' # GFF
                    cds[-1] = arr[8]
                    out.write("\t".join(cds)+'\n')
                # utr5 utr3
                utr5 = add_five_prime_utr(assembly_exon[ts], refer_cds[ts],strand)
                for i, u in enumerate(utr5, start=1):
                    arr[3] = str(u[0])
                    arr[4] = str(u[1])
                    arr[2] = 'five_prime_UTR'
                    arr[8] = f'ID={ts}:five_prime_UTR:{i};Parent={ts};'
                    out.write("\t".join(arr)+'\n')
                utr3 = add_three_prime_utr(assembly_exon[ts], refer_cds[ts],strand)
                for j, u in enumerate(utr3, start=1):
                    arr[3] = str(u[0])
                    arr[4] = str(u[1])
                    arr[2] = 'three_prime_UTR'
                    arr[8] = f'ID={ts}:three_prime_UTR:{j};Parent={ts};'
                    out.write("\t".join(arr)+'\n')
            else:
                # from transcoder new isoform
                # 转录本以MSTRG开头的
                # 如果不在最终的预测list中直接跳过，不予赋CDS的注释信息
                # 如果transcoder预测的CDS的方向和基因方向相反，则不要
                if ts not in cds_final_set:
                    delete_protein.add(ts)
                    continue
                class_code = assembly_feature[ts][2]
                #if class_code in ['s', 'x']:
                #    # 反向的不给CDS,UTR3/5的注释，直接跳过 组装出来的AT开头的没有s x,所以该if不会执行
                #    # novel 的需要给其加上自己注释的CDS
                #    continue
                if trans_decoder_dict.get(gene):
                    if gene == 'MSTRG.4':
                        print('MSTRG.4---', trans_decoder_dict[gene][ts])
                    if trans_decoder_dict[gene][ts]:
                        if ts == 'AT5G01020.1':
                            print('AT5G01020.1', trans_decoder_dict[gene][ts]['CDS'])
                        # CDS
                        # for i,cds in enumerate(trans_decoder_dict[gene][ts]['CDS'],start=1):
                        for i,cds in enumerate(sorted(trans_decoder_dict[gene][ts]['CDS'], key=lambda c: int(c[3])), start=1):
                            if strand != cds[6]:
                                break 
                            cds[1] = 'StringTie'
                            #cds[8] = re.sub('.p\d', '', cds[8])
                            #cds[8] = re.sub('cds.', '', cds[8])
                            if strand == "+":
                                cds[8] = f'ID={ts}:CDS:{i};Parent={ts};'
                            else:
                                cds_num = len(trans_decoder_dict[gene][ts]['CDS'])
                                cds[8] = f'ID={ts}:CDS:{cds_num - i + 1};Parent={ts};'
                            cds_line = "\t".join(cds)
                            out.write(cds_line+'\n')
                        # five_prime_UTR
                        if len(trans_decoder_dict[gene][ts]["five_prime_UTR"]) != 0:
                            for i, utr5 in enumerate(trans_decoder_dict[gene][ts]["five_prime_UTR"], start=1):
                                if strand != utr5[6]:
                                    break
                                utr5[1] = 'StringTie'
                                #utr5[8] = re.sub('.p\d.utr5p\d', '', utr5[8])
                                #utr5[8] = re.sub('.p\d', '', utr5[8]) 
                                utr5[8] = f'ID={ts}:five_prime_UTR:{i};Parent={ts};'
                                utr5_line = "\t".join(utr5)
                                out.write(utr5_line+'\n')
            
                        # three_prime_UTR
                        if len(trans_decoder_dict[gene][ts]["three_prime_UTR"]) != 0:
                            for j, utr3 in enumerate(trans_decoder_dict[gene][ts]["three_prime_UTR"], start=1):
                                if strand != utr3[6]:
                                    break
                                utr3[1] = 'StringTie'
                                #utr3[8] = re.sub('.p\d.utr3p\d', '', utr3[8])
                                #utr3[8] = re.sub('.p\d', '', utr3[8])
                                utr3[8] = f'ID={ts}:three_prime_UTR:{j};Parent={ts};'
                                utr3_line = "\t".join(utr3)
                                out.write(utr3_line+'\n')

print('Protein Number=', line_count)
print('Pass Count=', pass_count)
print('gene_to_ref=', len(gene_to_ref))
print('gene_to_tair=', len(gene_to_tair))
print('gene_to_assem=', len(gene_to_assem))
print('gene_mRNA=', len(gene_mRNA))
print('gene_mRNA2=', len(gene_mRNA2))
print('delete_protein=', len(delete_protein))

# check gene id
# re format gene region
# because MSTRG.x will cover AT1G01020, AT1G01030
# this will cause ath_inherit.gff gene region eeeor
# longest region of multiple transcripts for gene region 
import numpy as np 
gene_ids = dict()
gene_region = dict()
gene_exist = dict()
with open('ath_inherit.gff', 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        arr = line.split('\t')
        if arr[2] in ['CDS', 'exon', 'five_prime_UTR', 'three_prime_UTR', 'gene']:
            continue
        if arr[2] == 'gene':
            gene_id = arr[8].split(';')[0].replace("ID=","")
            if not gene_exist.get(gene_id):
                gene_exist[gene_id] = 1
        # ID=AT1G01010.1;Parent=AT1G01010;
        ts = arr[8].split(";")[0].replace("ID=", '')
        start, end = int(arr[3]), int(arr[4])
        gene = arr[8].split(";")[1].replace("Parent=", '')
        if gene_ids.get(gene):
            gene_ids[gene].append([start, end])
        else:
            gene_ids[gene] = [[start, end]]
    for gene in gene_ids.keys():
        if len(gene_ids[gene]) == 1:
            gene_region[gene] = gene_ids[gene][0]
        else:
            npa = np.array(gene_ids[gene])
            gene_region[gene] = [npa.min(), npa.max()]

with open('ath_inherit.gff', 'r') as f, open('ath_inherit_correct.gff', 'w') as out:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        arr = line.split('\t')
        if arr[2] in ['CDS', 'exon', 'five_prime_UTR', 'three_prime_UTR', 'gene']:
            if arr[2] == 'gene':
                continue
            out.write(line+'\n')
        else:
            gene = arr[8].split(";")[1].replace("Parent=", '')
            if gene_exist.get(gene):
                pass
            else:
                arr[2] = 'gene'
                arr[8] = f'ID={gene};'
                arr[3] = str(gene_region[gene][0])
                arr[4] = str(gene_region[gene][1])
                gene_line = '\t'.join(arr)
                out.write(gene_line+'\n')
                gene_exist[gene] = 1
            out.write(line+'\n')



    

        



print(len(assembly_feature))

        

