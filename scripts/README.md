## Analysis Scripts in 5leaderP

### Short-read assembly 
The assembly pipelines have been deployed in Assembly_pipeline directory. Those pipelines includes short-read and long-read.

The python RNA_assemble_ath.py is used for transcriptom assembly in next-generation sequencing reads.
You can get help by `python RNA_assemble_ath.py -h` in command line.
```bash
$ python RNA_assemble_ath.py -h 
usage: RNA_assemble_ath.py [-h] [--gtf GTF] [--genome GENOME] [--index INDEX] [--output OUTPUT] [--adapter ADAPTER] [--sample SAMPLE]
                           [--pair_mode PAIR_MODE] [--run_mode RUN_MODE]

RNA assemble main program

optional arguments:
  -h, --help            show this help message and exit
  --gtf GTF, -f GTF     General Feature Format(GTF) of genome
  --genome GENOME, -g GENOME
                        Genome fasta
  --index INDEX, -i INDEX
                        genome hisat index
  --output OUTPUT, -o OUTPUT
                        result output dir
  --adapter ADAPTER, -a ADAPTER
                        adapter for platform,if paired, separate by comma
  --sample SAMPLE, -s SAMPLE
                        sample list, separate by comma
  --pair_mode PAIR_MODE, -p PAIR_MODE
                        library pair or single
  --run_mode RUN_MODE, -r RUN_MODE
                        switch run mode
```
- Example

A work.sh in Arabidopsis
```bash
python RNA_assemble_ath.py --gtf /home/zhusitao/database/plant/ath/tair10/araport11.gff \
                           --genome /home/zhusitao/database/plant/ath/tair10/hisat2_index/TAIR10.fa \
                           --index /home/zhusitao/database/plant/ath/tair10/hisat2_index/TAIR10 \
                           --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA \
                           --run_mode True \
                           --pair_mode True \
                           --sample SRR545214_1.fastq.gz,SRR545214_2.fastq.gz \
                           --output /home/zhusitao/database/plant/ath/RNA/Dzjx/pysradb_downloads_leaves/SRP014919/SRX179402/assemble
```
