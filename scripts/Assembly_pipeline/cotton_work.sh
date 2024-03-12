# AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
# AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA
python RNA_assemble_cotton.py --gtf /home/zhusitao/database/plant/cotton/genome/A2_HAU/Garboreum_gene.gtf \
                           --genome /home/zhusitao/database/plant/cotton/genome/A2_HAU/gab.fa \
                           --index /home/zhusitao/database/plant/cotton/genome/A2_HAU/hisat2_index/gab \
                           --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA \
                           --run_mode True \
                           --pair_mode True \
                           --sample SRR8268758_1.fastq.gz,SRR8268758_2.fastq.gz \
                           --output /home/zhusitao/database/plant/cotton/RNA/leaf/pysradb_downloads/SRP171691/SRX5085610/assemble
