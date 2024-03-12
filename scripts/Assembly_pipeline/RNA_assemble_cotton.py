#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: RNA_assemble_cotton.py
date: 2021/9/22 上午8:39
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
        # pair end reads
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
              f' --sam --num_alignments 1 --fastx' \
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
                    f' --paired_out --out2 ' \
                    f' --sam --num_alignments 1 --fastx' \
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
              f' samtools view -b -q 20 -S -o {hisat_dir}/{sampleid[i]}.bam' for i in range(len(fastq_files))]
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
              f' samtools view -b -q 20 -S -o {hisat_dir}/{sampleid[i]}.bam' for i in range(len(fastq_files)//2)]
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


def star(fastq_files: list, refer_gtf:str, outdir: str, run=False):
    '''
    STAR aligner
    :param fastq_files: clean fastq files
    :param outdir: output dir
    :return: bam file
    '''
    star_dir = os.path.join(outdir, "05.star")
    if not os.path.exists(star_dir):
        os.makedirs(star_dir)
    sampleid = [i.replace('_non_rRNA.fq.gz', '') for i in fastq_files]
    commands = [f'STAR --runThreadN 24 --sjdbOverhang 50 ' \
              f'--genomeDir /home/zhusitao/database/plant/rice/MSU7/star_index' \
              f' --sjdbGTFfile {refer_gtf}' \
              f' --readFilesIn {outdir}/03.remove_rRNA/{fastq_files[i]}' \
              f' --outFileNamePrefix {star_dir}/{sampleid[i]}' \
              f' --readFilesCommand zcat' \
              f' --outFilterMismatchNmax 2' \
              f' --outSAMtype BAM SortedByCoordinate' \
              f' --outSAMstrandField intronMotif' for i in range(len(fastq_files))]
    write_shell(commands, star_dir)
    run_command(commands, run_bool=run)

    return [f'{sampleid[i]}Aligned.sortedByCoord.out.bam' for i in range(len(fastq_files))]



# assembler alternative
def cufflinks(bamfiles: list, refer_gtf:str, outdir: str, run=False):
    '''
    reference guide assembly
    :param bamfiles: bam file for assemble
    :param outdir: output dir
    :return: None
    '''
    cuff_ditr = os.path.join(outdir, "06.cufflinks")
    if not os.path.exists(cuff_ditr):
        os.makedirs(cuff_ditr)
    commands = [f'cufflinks -g {refer_gtf}' \
              f' --library-type fr-unstranded -p 16' \
              f' -o {cuff_ditr}' \
              f' {outdir}/05.star/{bamfiles[i]}' for i in range(len(bamfiles))]
    write_shell(commands, cuff_ditr)
    run_command(commands, run_bool=run)



def stringTie(bamfiles: list, refer_gtf:str, outdir: str, run=False):
    '''
    reference guide assembly as a successor to Cufflinks
    :param bamfiles:
    :param outdir:
    :return:
    '''
    stie_dir = os.path.join(outdir, "06.stringTie")
    if not os.path.exists(stie_dir):
        os.makedirs(stie_dir)
    # for star
    # out_gtf = [i.replace('Aligned.sortedByCoord.out.bam', '.gtf') for i in bam_files]
    # alternative hisat2
    out_gtf = [i.replace('.sorted.bam', '.gtf') for i in bamfiles]
    commands = [f'stringtie {outdir}/05.hisat2/{bamfiles[i]}' \
               f' -G {refer_gtf}' \
               f' -p 16' \
               f' -o {stie_dir}/{out_gtf[i]}' for i in range(len(bamfiles))]
    write_shell(commands, stie_dir)
    run_command(commands, run_bool=run)

    return [os.path.join(stie_dir, gtf) for gtf in out_gtf]

def trinity_guide(bamfiles: list, outdir: str, run=False):
    '''
    Genome-guided Trinity different from cufflink genome-guided model
    :param bamfiles: bam for trinity
    :param outdir: result dir
    :return: Trinity-GG.fasta
    '''
    bams_dir = os.path.join(outdir, "05.hisat2")
    trinity_dir =  os.path.join(outdir,"07.trinity/genome_guide_trinity")
    if not os.path.exists(trinity_dir):
        os.makedirs(trinity_dir)
    # merge bams
    bams_abs = [os.path.join(bams_dir,i) for i in bamfiles]
    bams_args = ' '.join(bams_abs)
    command1 = f'samtools merge -@ 10 {trinity_dir}/trinity.bam {bams_args}'
    # Genome-guided Trinity
    command2 = f'Trinity --genome_guided_bam {trinity_dir}/trinity.bam' \
               f' --genome_guided_max_intron 10000' \
               f' --max_memory 30G --CPU 20' \
               f' --output {trinity_dir}'

    write_shell(command1, trinity_dir)
    write_shell(command2, trinity_dir)
    run_command(command1, run_bool=run)
    run_command(command2, run_bool=run)

    return os.path.join(trinity_dir,'Trinity-GG.fasta')


def trinity_denovo(fastq_files: list, outdir: str, run=False):
    '''
    De novo assemble
    :param fastq_files: file list
    :param outdir: result dir
    :return: Trinity.fasta
    '''
    fq_dir = os.path.join(outdir, "03.remove_rRNA")
    trinity_dir =  os.path.join(outdir,"07.trinity/denovo_trinity")
    if not os.path.exists(trinity_dir):
        os.makedirs(trinity_dir)
    # De novo Trinity
    command = f'Trinity --seqType fq' \
               f' --left {fq_dir}/{fastq_files[0]}' \
               f' --right {fq_dir}/{fastq_files[1]}' \
               f' --max_memory 30G --CPU 20' \
               f' --output {trinity_dir}'


    write_shell(command, trinity_dir)
    run_command(command, run_bool=run)

    return trinity_dir+'.Trinity.fasta'

def trinit_cat(fasta_GG:str,fasta_denovo:str,outdir: str, run=False):
    '''
    cat two fasta file
    :param fasta_GG:
    :param fasta:
    :param outdir:
    :return:one fasta
    '''
    trinity_dir = os.path.join(outdir, "07.trinity")
    if not os.path.exists(trinity_dir):
        os.makedirs(trinity_dir)
    result = os.path.join(trinity_dir,'transcripts.fasta')
    command = f'cat {fasta_GG} {fasta_denovo} > {result}'
    write_shell(command, trinity_dir)
    run_command(command, run_bool=run)

    return result


def blat(fasta:str, genome_fasta:str, outdir:str, run=False):
    '''
    filter the trinity denovo fasta
    :param fasta: trinity genome guided assemble (Trinity-GG.fasta)
    :param outdir: result dir
    :return: None
    '''
    blat_dir = os.path.join(outdir,'08.blat')
    if not os.path.exists(blat_dir):
        os.makedirs(blat_dir)

    # blat
    command_blat = f'blat -minIdentity=95' \
                   f' -minScore=30 ' \
                   f' {genome_fasta} ' \
                   f' {fasta}' \
                   f' {blat_dir}/output.psl'
    # remove not passed threshold
    command_filter = f'cat {blat_dir}/output.psl | cut -f 10 | grep TRINITY > {blat_dir}/passed_id.txt \n' \
              f' seqkit grep --id-regexp "^(\\S+)\\s+" -f {blat_dir}/passed_id.txt {fasta} > {blat_dir}/trinity.blat.fasta'
    # write
    write_shell(command_blat, blat_dir)
    write_shell(command_filter, blat_dir)
    # exec
    run_command(command_blat, run_bool=run)
    run_command(command_filter, run_bool=run)

    return os.path.join(blat_dir, 'trinity.blat.fasta')

def gmap(fasta: str, outdir:str, run=False):
    '''
    Gmap transform trinity fasta to gff
    :param fasta: fasta from trinity assemble,and filter by blat
    :param outdir: result dir
    :return: trinity gff
    '''
    gmap_dir = os.path.join(outdir,'09.gmap')
    if not os.path.exists(gmap_dir):
        os.makedirs(gmap_dir)
    # Firstly, gmap should be build index for genome
    # index was saved in '/home/zhusitao/software/RNA_assemble/gmap-2021-08-25/share'
    # exec in share dir ,only one
    # build_command = 'gmap_build -d msu7 ' \
    #                 ' -c msu7_tr ' \
    #                 ' -T /home/zhusitao/database/plant/rice/MSU7/refMrna/refMrna.fa ' \
    #                 ' /home/zhusitao/database/plant/rice/MSU7/msu7.fa'
    # Gmap
    command = f'gmap -t 8 ' \
              f' -f 2 ' \
              f' -D /home/zhusitao/software/RNA_assemble/gmap-2021-08-25/share ' \
              f' -d msu7 ' \
              f' {fasta}' \
              f' 1> {gmap_dir}/trinity.gff3 ' \
              f' 2> {gmap_dir}/log'
    write_shell(command, gmap_dir)
    run_command(command, run_bool=run)

    return os.path.join(gmap_dir, 'trinity.gff3')


def stringTieMerge(gtf_files: list, refer_gtf:str, outdir: str,run=False):
    '''
    Merge GTF
    :param gtf_files: input files for merge
    :return: None
    '''
    merge_dir = os.path.join(outdir, "10.stringTieMerge")
    if not os.path.exists(merge_dir):
        os.makedirs(merge_dir)

    gtf_abs_path = ' '.join(gtf_files)
    command = f'stringtie --merge ' \
               f' -G {refer_gtf}' \
               f' -o {merge_dir}/merge.gtf' \
               f' {gtf_abs_path}'
    write_shell(command, merge_dir)
    run_command(command, run_bool=run)

    return f'{merge_dir}/merge.gtf'



def gffcompare(merge_gtf:str, refer_gtf:str, outdir:str, run=False):
    '''
    compare merge.gtf to reference gtf
    :param merge_gtf:
    :param outdir:
    :return: new gtf
    '''
    merge_dir = os.path.join(outdir, "10.stringTieMerge")
    if not os.path.exists(merge_dir):
        os.makedirs(merge_dir)
    command1 = f'gffcompare -R -r {refer_gtf} {merge_gtf} -o {merge_dir}/total'
    command2 = f'trmap {refer_gtf} {merge_gtf} -o {merge_dir}/trmap.out'
    write_shell(command1, merge_dir)
    run_command(command1, run_bool=run)
    write_shell(command2, merge_dir)
    run_command(command2, run_bool=run)

    return os.path.join(merge_dir,'total.annotated.gtf')

def trans_decoder(final_gtf:str, genome_fasta:str,outdir:str, run=False):
    '''
    transfromer stringtie gtf to nomal gene structure (gene,mRNA,CDS 3'utr, 5'utr)
    :param final_gtf: stringtie gtf
    :param outdir: result dir
    :return:
    '''
    decode_dir = os.path.join(outdir, "11.trans_decoder")
    if not os.path.exists(decode_dir):
        os.makedirs(decode_dir)
    os.chdir(f'{decode_dir}')
    command = f'/home/zhusitao/software/TransDecoder-TransDecoder-v5.5.0/sample_data/stringtie_example/bin/runMe.sh {final_gtf} {genome_fasta} {decode_dir}'
    write_shell(command, decode_dir)
    run_command(command, run_bool=run)


def liftoff():
    pass

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
    parser = argparse.ArgumentParser(description='RNA assemble main program')

    parser.add_argument('--gtf', '-f', type=str,
                        help='General Feature Format(GTF) of genome')
    parser.add_argument('--genome', '-g', type=str,
                        help='Genome fasta')
    parser.add_argument('--index', '-i', type=str,
                        help='genome hisat index ')
    parser.add_argument('--output', '-o', type=str,
                        help='result output dir')
    parser.add_argument('--adapter', '-a', type=str,
                        help='adapter for platform,if paired, separate by comma')
    parser.add_argument('--sample', '-s', type=str,
                        help='sample list, separate by comma')
    parser.add_argument('--pair_mode', '-p', default=False, type=boolean_string,
                        help='library pair or single')
    parser.add_argument('--run_mode', '-r', default=False, type=boolean_string,
                        help='switch run mode')
    return parser.parse_args()



def main():
    # parameter parse
    args = parameters_parse()
    print(args)
    outdir = args.output
    if not outdir:
        sys.exit('Outdir was  not specified')
    genome_fasta = args.genome
    if not genome_fasta:
        sys.exit('Genome fasta was not specified')
    refer_gtf = args.gtf
    if not refer_gtf:
        sys.exit('Reference gtf was not specified')
    hisat_index = args.index
    if not hisat_index:
        sys.exit('Hisat2 index was not specified')
    files = args.sample.split(',')
    if not files:
        sys.exit('Fastq files were not specified')
    run_mode = args.run_mode
    adapters = args.adapter
    if not adapters:
        sys.exit('Adapters were not specified')
    pair_mode = args.pair_mode

    print('run_mode', run_mode)
    # files = ['SRR12011294_1.fastq.gz','SRR12011294_2.fastq.gz']
    # run mode
    # run_mode = False
    # step1 qc
    fastqc(files, outdir, run=False)
    # step2 cutadapt
    trim_files = trim(files, outdir, adapters, pair=pair_mode, run=False)
    # remove rRNA
    rm_files = rm_rRNA(trim_files, outdir, pair=pair_mode, run=False)
    # step4 qc
    fastqc2(rm_files, outdir, run=False)
    # step5 mapping
    bam_files = hisat2(rm_files, hisat_index, outdir, pair=pair_mode, run=run_mode)
    '''
    # step6 genome guide assemble
    gtf_files = stringTie(bam_files, refer_gtf, outdir, run=run_mode)
    # step7.1 genome guide denovo assemble
    trinity_GG_fasta = trinity_guide(bam_files, outdir, run=run_mode)
    # step7.2 denovo assemble
    trinity_denovo_fasta = trinity_denovo(rm_files, outdir, run=run_mode)
    # step7.3 cat
    transcripts_fasta = trinit_cat(trinity_GG_fasta, trinity_denovo_fasta, outdir, run=run_mode)
    # step8 denovo filter
    trinity_blat_fasta = blat(transcripts_fasta, genome_fasta, outdir, run=run_mode)
    # step9 denovo fasta to gff
    trinity_gff = gmap(trinity_blat_fasta, outdir, run=run_mode)
    # step10.1 merge
    gtf_files.append(trinity_gff)
    merge_gtf = stringTieMerge(gtf_files, refer_gtf, outdir, run=run_mode)
    # step10.2 gffcompare
    final_gtf = gffcompare(merge_gtf, refer_gtf, outdir, run=run_mode)
    # step 11 trans_decoder
    trans_decoder(final_gtf, genome_fasta, outdir, run=run_mode)
    '''

if __name__ == '__main__':
    main()
