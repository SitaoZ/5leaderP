# AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
# AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA
python RNA_assemble_maize.py --gtf /home/zhusitao/database/plant/maize/genome/zma.gtf \
                           --genome /home/zhusitao/database/plant/maize/genome/zma.fa \
                           --index /home/zhusitao/database/plant/maize/genome/hisat2_index/zma \
                           --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA \
                           --run_mode True \
                           --pair_mode True \
                           --sample SRR1757990_1.fastq.gz,SRR1757990_2.fastq.gz \
                           --output /home/zhusitao/database/plant/maize/RNA/pysradb_downloads_leaf/SRP052226/SRX842297/assemble
