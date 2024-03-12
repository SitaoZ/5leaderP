# AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
# AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA
python RNA_assemble_soybean.py --gtf /home/zhusitao/database/plant/soybean/genome/gmx.gtf \
                           --genome /home/zhusitao/database/plant/soybean/genome/gmx.fa \
                           --index /home/zhusitao/database/plant/soybean/genome/hisat2_index/gmx \
                           --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC \
                           --run_mode True \
                           --pair_mode False \
                           --sample SRR11741800_1.fastq.gz \
                           --output /home/zhusitao/database/plant/soybean/RNA/pysradb_downloads_leaf/SRP260832/SRX8295294/assemble
