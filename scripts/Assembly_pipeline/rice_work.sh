# NovSeq 6000
# AGATGTGTATAAGAGACAG
# AGATGTGTATAAGAGACAG
python RNA_assemble_rice.py --gtf /home/zhusitao/database/plant/rice/MSU7/msu7.gtf \
                           --genome /home/zhusitao/database/plant/rice/MSU7/msu7.fa \
                           --index /home/zhusitao/database/plant/rice/MSU7/hisat2_index/msu7 \
                           --adapter AGATGTGTATAAGAGACAG,AGATGTGTATAAGAGACAG \
                           --run_mode True \
                           --pair_mode True \
                           --sample SRR12011292_1.fastq.gz,SRR12011292_2.fastq.gz \
                           --output /home/zhusitao/database/plant/rice/RNA/leaf/pysradb_downloads/SRP267262/SRX8543996/assemble
