## Analysis Scripts in 5leaderP

### Short-read assembly 

The assembly pipelines have been deployed in `Assembly_pipeline` directory. Those pipelines include short-read and long-read assembly.

The python `RNA_assemble_ath.py` is used for transcriptom assembly in next-generation sequencing reads.
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

A work_tair.sh in Arabidopsis
```bash
python RNA_assemble_ath.py --gtf /home/zhusitao/database/plant/ath/tair10/araport11.gff \
                           --genome /home/zhusitao/database/plant/ath/tair10/hisat2_index/TAIR10.fa \
                           --index /home/zhusitao/database/plant/ath/tair10/hisat2_index/TAIR10 \
                           --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA \
                           --run_mode True \
                           --pair_mode True \
                           --sample DRR146853_1.fastq.gz,DRR146853_2.fastq.gz \
                           --output /home/zhusitao/database/plant/ath/RNA/Dzjx/pysradb_downloads_leaves/DRP004486/DRX137645/assemble  
```

### Long-read assembly

The `SMRT_ONT_assembly.sh` is a command pipeline for SMRT and ONT reads assembly. The pipeline adopted `Minimap2` and `TALON` for long-read assembly.



### CAGE-Seq pipeline

The `CAGE_step1_ctss_call.py` and  `CAGE_step2_peak_call.sh` are used for CAGE-Seq analysis.

- CTSS calling 
```bash
$ python CAGE_step1_ctss_call.py -h 
usage: CAGE_step1_ctss_call.py [-h] [--index INDEX] [--output OUTPUT] [--sample SAMPLE] [--adapter ADAPTER] [--run_mode RUN_MODE]
                               [--pair_mode PAIR_MODE]

CAGE peak calling main program

optional arguments:
  -h, --help            show this help message and exit
  --index INDEX, -i INDEX
                        genome hisat index
  --output OUTPUT, -o OUTPUT
                        result output dir
  --sample SAMPLE, -s SAMPLE
                        sample list, separate by comma
  --adapter ADAPTER, -a ADAPTER
                        adapter for platform,if paired, separate by comma
  --run_mode RUN_MODE, -r RUN_MODE
                        switch run mode
  --pair_mode PAIR_MODE, -p PAIR_MODE
                        library pair or single
```

- aTSS peak identification
```bash
/home/zhusitao/project/DPI/dpi1-master/identify_tss_peaks.sh -g /home/zhusitao/project/DPI/01.ath/CTSS_for_DPI/chrom.sizes \
                                                             -i 'CTSS_for_DPI/*.ctss.gz' -d N -o CTSS_22samples_v2
```
### Ranking-algorithm 
The `isoform_ranking_algorithm_for_representative.py` is used for representative isoform identification.
The scirpts need the expression files from `RSEM`. 

```bash
$ python isoform_ranking_algorithm_for_representative.py -h 
usage: isoform_ranking_algorithm_for_representative.py [-h] [--gff GFF]
                                                       [--exp_dir EXP_DIR]
                                                       [--output OUTPUT]

Ranking-algorithm implementation

optional arguments:
  -h, --help            show this help message and exit
  --gff GFF, -f GFF     General Feature Format(GFF)
  --exp_dir EXP_DIR, -i EXP_DIR
                        A dir contains expression file (ends with
                        isoforms.results) from RSEM
  --output OUTPUT, -o OUTPUT
                        representative isoform filename
```

### Model performance comparison

The `Model_performance` dir contains the comparison scripts for evaluating the performance of various tools.
We selected `TransPrise`, `TSSFinder` and `TSSPlant` compared with the 5leaderP tool in classification and regression.
each `work.sh` describe the comparison in detail.

### Figure scripts

The `Fig.1-5` dirs contain the analysis scripts for results visualization.

### Supplementary figures scripts

The `FigS.1-8` dirs include the analysis scripts for supplementary results visualization.

### Other scripts

The `inherit_feature_from_genome.py` script is used for known genes and transcripts feature annotation.
The `recorrect_gff.py` script is utilized to rectify overlapping issues in GFF files.
