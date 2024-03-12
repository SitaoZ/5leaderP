#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: CAGE_step1_ctss_call.py
date: 2021/10/10 上午10:03
author: Sitao Zhu
mail: zhusitao1990@163.com
'''


import os
import sys
import argparse
from multiprocessing import Pool

def write_shell(commands:list,outdir:str):
    '''
    write shell to local file
    :param commads: commands exec
    :param outdir: outdir for command to write
    :return: None
    '''
    if isinstance(commands, str):
        commands = [commands]

    with open(os.path.join(outdir,'work.sh'),'a+') as f:
        for c in commands:
            f.write(c+'\n')


def run_command(commands, run_bool=False):
    '''
    Run commands
    :param commands:
    :return:
    '''
    if isinstance(commands, str):
        commands = [commands]
    if run_bool == True:
        for command in commands:
            os.system(command)



def fastqc(fastq_files: list, outdir: str, run=False):
    '''
    fastqc the raw reads
    :param fastq_files: fastq file list
    :param outdir: result dir
    :return:None
    '''
    qc_dir = os.path.join(outdir, "01.fastqc")
    if not os.path.exists(qc_dir):
        os.makedirs(qc_dir)
    fastq_abs_path = [f'{outdir}/{fastq_files[i]}' for i in range(len(fastq_files))]
    fastq_args = ' '.join(fastq_abs_path)
    command = f'fastqc -t 8 -o {qc_dir} {fastq_args} '
    # write shell
    write_shell(command, qc_dir)
    run_command(command, run_bool=run)


def trim(fastq_files: list, outdir: str, adapters:str, pair=False, run=False):
    '''
    TruSeq RNA Sample Prep Kits v2 adapter
    :param fastq_files: fastq raw files
    :param outdir: result dir
    :return: trimed fastq basename, not the absolute path
    '''
    trim_dir = os.path.join(outdir, "02.trim")
    if not os.path.exists(trim_dir):
        os.makedirs(trim_dir)
    outfiles = [i.replace('.fastq.gz', '') for i in fastq_files]

    if pair == False:
        single_adapter = adapter_parse(pair, adapters)

        commands = [f'cutadapt -j 24 -m 20 -q 20' \
                f' --max-n 0.2 -e 0.08 -Z' \
                f' --trim-n -a {single_adapter}' \
                f' -o {trim_dir}/{outfiles[i]}_trimed.fq.gz' \
                f' {outdir}/{fastq_files[i]}' for i in range(len(fastq_files))]
    else:
        forward_adapter, reverse_adapter = adapter_parse(pair, adapters)
        commands = [f'cutadapt -j 24 -m 20 -q 20' \
                    f' --max-n 0.2 -e 0.08 -Z' \
                    f' --trim-n -a {forward_adapter}' \
                    f' -A {reverse_adapter}' \
                    f' -o {trim_dir}/{outfiles[i]}_trimed.fq.gz' \
                    f' -p {trim_dir}/{outfiles[i+1]}_trimed.fq.gz' \
                    f' {outdir}/{fastq_files[i]}' \
                    f' {outdir}/{fastq_files[i+1]}' for i in range(len(fastq_files)//2)]
    write_shell(commands, trim_dir)
    run_command(commands, run_bool=run)

    return [f'{outfiles[i]}_trimed.fq.gz' for i in range(len(fastq_files))]



def rm_rRNA(fq_files: list, outdir: str, pair=False, run=False):
    '''
    remove rRNA through sortmerna
    :param fq_files: trimmed fastq files
    :param outdir: result dir
    :return:removed the rRNA fastq file
    '''
    db1 = '/home/zhusitao/software/sortmerna/data/rRNA_databases/silva-euk-18s-id95.fasta'
    db2 = '/home/zhusitao/software/sortmerna/data/rRNA_databases/silva-euk-28s-id98.fasta'
    db3 = '/home/zhusitao/software/sortmerna/data/rRNA_databases/rfam-5.8s-database-id98.fasta'
    db4 = '/home/zhusitao/software/sortmerna/data/rRNA_databases/rfam-5s-database-id98.fasta'
    trim_dir = os.path.join(outdir, "02.trim")
    rm_dir = os.path.join(outdir, "03.remove_rRNA")
    if not os.path.exists(rm_dir):
        os.makedirs(rm_dir)
    outfiles = [i.replace('_trimed.fq.gz', '') for i in fq_files]
    sampleid = [i.split('_')[0] for i in outfiles]

    if pair == False:
        # single end read
        commands = [f'sortmerna --threads 24 --workdir {rm_dir}' \
              f' -ref {db1} -ref {db2} -ref {db3} -ref {db4}' \
              f' --reads {trim_dir}/{fq_files[i]}' \
              f' --sam --num_alignments 1 -fastx' \
              f' --aligned {rm_dir}/{outfiles[i]}_rRNA' \
              f' --other {rm_dir}/{outfiles[i]}_non_rRNA -v' for i in range(len(outfiles))]


        rm_command = f'rm -rf {rm_dir}/idx  {rm_dir}/kvdb {rm_dir}/readb'
        commands.insert(1,rm_command)
        commands.insert(3,rm_command)

    else:
        # pair end read
        commands = [f'sortmerna --threads 24 --workdir {rm_dir}' \
                    f' -ref {db1} -ref {db2} -ref {db3} -ref {db4}' \
                    f' --reads {trim_dir}/{fq_files[i]}' \
                    f' --reads {trim_dir}/{fq_files[i+1]}' \
                    f' --paired_out True --out2 True' \
                    f' --sam --num_alignments 1 -fastx' \
                    f' --aligned {rm_dir}/{sampleid[i]}_rRNA' \
                    f' --other {rm_dir}/{sampleid[i]}_non_rRNA -v' for i in range(len(sampleid)//2)]
        rm_command = f'rm -rf {rm_dir}/idx  {rm_dir}/kvdb {rm_dir}/readb'
        commands.insert(1, rm_command)
    # write shell
    write_shell(commands, rm_dir)
    # exec
    run_command(commands, run_bool=run)
    # return result
    if pair == False:
        return [f'{outfiles[i]}_non_rRNA.fq.gz' for i in range(len(fq_files))]
    else:
        return [f'{sampleid[0]}_non_rRNA_fwd.fq.gz', f'{sampleid[0]}_non_rRNA_rev.fq.gz']


def fastqc2(fastq_files: list, outdir: str, run=False):
    '''
    fastqc after trimmed
    :param fastq_files: trimmed fastq file
    :param outdir: output dir
    :return: None
    '''
    qc_dir = os.path.join(outdir, "04.fastqc")
    if not os.path.exists(qc_dir):
        os.makedirs(qc_dir)
    fastq_abs_path = [f'{outdir}/03.remove_rRNA/{fastq_files[i]}' for i in range(len(fastq_files))]
    fastq_args = ' '.join(fastq_abs_path)
    command = f'fastqc -t 8 -o {qc_dir} {fastq_args} '
    write_shell(command, qc_dir)
    run_command(command, run_bool=run)


# aligner alternative
def hisat2(fastq_files:list, hisat_index:str, outdir:str, pair=False, run=False):
    '''
    genome mapping
    :param fastq_files: fastq file
    :param hisat_index: hisat2 index prefix
    :param outdir: result dir
    :param pair: pair end or single end
    :param run: run mode
    :return: bam file
    '''
    hisat_dir = os.path.join(outdir, "05.hisat2")
    if not os.path.exists(hisat_dir):
        os.makedirs(hisat_dir)

    if pair == False:
        # single end reads
        sampleid = [i.replace('_non_rRNA.fq.gz', '') for i in fastq_files]
        aligner_commands = [f'hisat2 -x {hisat_index}' \
              f' -p 16 --phred33 --sensitive' \
              f' -U {outdir}/03.remove_rRNA/{fastq_files[i]}' \
              f' 2>{hisat_dir}/{sampleid[i]}.Map2GenomeStat.xls |' \
              f' samtools view -b -S -o {hisat_dir}/{sampleid[i]}.bam' for i in range(len(fastq_files))]
        sort_command = [f'samtools sort -@ 8 -o {hisat_dir}/{sampleid[i]}.sorted.bam {hisat_dir}/{sampleid[i]}.bam' for
                        i in range(len(fastq_files))]

    else:
        # pair end reads
        sampleid = [i.split('_')[0] for i in fastq_files]
        aligner_commands = [f'hisat2 -x {hisat_index}' \
              f' -p 16 --phred33 --sensitive' \
              f' -1 {outdir}/03.remove_rRNA/{fastq_files[i]}' \
              f' -2 {outdir}/03.remove_rRNA/{fastq_files[i+1]}' \
              f' 2>{hisat_dir}/{sampleid[i]}.Map2GenomeStat.xls |' \
              f' samtools view -b -S -o {hisat_dir}/{sampleid[i]}.bam' for i in range(len(fastq_files)//2)]
        sort_command = [f'samtools sort -@ 8 -o {hisat_dir}/{sampleid[i]}.sorted.bam {hisat_dir}/{sampleid[i]}.bam' for i in range(len(fastq_files)//2)]

    joint_command = aligner_commands + sort_command
    # write
    write_shell(joint_command, hisat_dir)
    # exec
    run_command(joint_command, run_bool=run)

    if pair:
        return [f'{sampleid[i]}.sorted.bam' for i in range(len(fastq_files)//2)]
    else:
        return [f'{sampleid[i]}.sorted.bam' for i in range(len(fastq_files))]

def ctss_call(bam:str,outdir:str,mqc=20,run=False):
    '''
    cage tss calling
    :param bam: input bam
    :param mqc: mapping quality cutoff
    :param outdir: output dir
    :return:
    '''
    ctss_dir = os.path.join(outdir, "06.ctss_call")
    if not os.path.exists(ctss_dir):
        os.makedirs(ctss_dir)
    bam_id = bam.replace('.bam','')
    bam_abs = os.path.join(outdir, '05.hisat2',bam_id)
    basename = os.path.basename(bam_id)

    out_prefix = os.path.join(ctss_dir,basename)

    command = f'/home/zhusitao/software/cageseq-1.0.2/bin/make_ctss.sh -q {mqc} -i {bam_abs} -n {out_prefix}'
    # write
    write_shell(command, ctss_dir)
    # exec
    run_command(command, run_bool=run)


def boolean_string(s):
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

def adapter_parse(pair_mode,adapters):
    '''
    parse adapters
    :param pair_mode: bool
    :param adapters:
    :return:adapter
    '''
    if pair_mode:
        forward_adapter, reverse_adapter = adapters.split(',')
        return forward_adapter,reverse_adapter
    else:
        single_adapter = adapters
        return single_adapter

def parameters_parse():
    parser = argparse.ArgumentParser(description='CAGE peak calling main program')

    parser.add_argument('--index', '-i', type=str,
                        help='genome hisat index ')
    parser.add_argument('--output', '-o', type=str,
                        help='result output dir')
    parser.add_argument('--sample', '-s', type=str,
                        help='sample list, separate by comma')
    parser.add_argument('--adapter', '-a', type=str,
                        help='adapter for platform,if paired, separate by comma')
    parser.add_argument('--run_mode', '-r', default=False, type=boolean_string,
                        help='switch run mode')
    parser.add_argument('--pair_mode', '-p', default=False, type=boolean_string,
                        help='library pair or single')
    return parser.parse_args()



def main():
    # parameter parse
    args = parameters_parse()
    print(args)
    outdir = args.output
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not outdir:
        sys.exit('Outdir was  not specified')
    hisat_index = args.index
    if not hisat_index:
        sys.exit('Hisat2 index was not specified')
    files = args.sample.split(',')
    if not files:
        sys.exit('Fastq files were not specified')

    adapters = args.adapter
    if not adapters:
        sys.exit('Adapters were not specified')
    pair_mode = args.pair_mode

    run_mode = args.run_mode
    print('run_mode',run_mode)
    # files = ['SRR12011294_1.fastq.gz','SRR12011294_2.fastq.gz']
    # run mode
    # run_mode = False
    # step1 qc
    fastqc(files, outdir, run=run_mode)
    # step2 cutadapt
    trim_files = trim(files, outdir, adapters, pair=pair_mode, run=run_mode)
    # remove rRNA
    rm_files = rm_rRNA(trim_files, outdir, pair=pair_mode, run=run_mode)
    # step4 qc
    fastqc2(rm_files, outdir, run=run_mode)
    # step5 mapping
    bam_files = hisat2(rm_files, hisat_index ,outdir, pair=pair_mode, run=run_mode)
    # step6 ctss calling
    ctss_call(bam_files[0],outdir,run=run_mode)




if __name__ == '__main__':
    main()