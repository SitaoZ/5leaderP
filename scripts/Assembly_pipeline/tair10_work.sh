#mkdir XJTU
#mv 05.hisat2/ 06.stringTie/ 07.trinity/ 08.blat/ 09.gmap/ 10.stringTieMerge/ 11.trans_decoder/ XJTU/
# AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
# AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA
python RNA_assemble_ath.py --gtf /home/zhusitao/database/plant/ath/tair10/araport11.gff \
                           --genome /home/zhusitao/database/plant/ath/tair10/hisat2_index/TAIR10.fa \
                           --index /home/zhusitao/database/plant/ath/tair10/hisat2_index/TAIR10 \
                           --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA \
                           --run_mode True \
                           --pair_mode True \
                           --sample DRR146853_1.fastq.gz,DRR146853_2.fastq.gz \
                           --output /home/zhusitao/database/plant/ath/RNA/Dzjx/pysradb_downloads_leaves/DRP004486/DRX137645/assemble  
