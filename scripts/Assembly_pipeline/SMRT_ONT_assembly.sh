## step1
## iteration samples
# minimap2 mapping and sort 
mkdir 01.minimap2
cd 01.minimap2
minimap2 -ax splice -t 20 -uf --MD --secondary=no -C5 /home/zhusitao/database/plant/ath/tair10/TAIR10.fa ../SRX1583871.fastq.gz > SRX1583871.sam
samtools sort -@ 10 -o SRX1583871.sorted.sam SRX1583871.sam
cd ..

mkdir 02.talon 
cd 02.talon 
# label sam
talon_label_reads --f ../01.minimap2/SRX1583871.sorted.sam \
                  --g /home/zhusitao/database/plant/ath/tair10/TAIR10.fa \
                  --t 10 \
                  --ar 20 \
                  --tmpDir=tmp_label_reads \
                  --deleteTmp \
                  --o SRX1583871

## step2
## assembly 
plat="Sequel"
touch config.csv
for file in `ls sam/*_labeled.sam`;
do
    base=`basename $file`
    sample="${base::${#base}-12}"
    sample="${base}"
    printf "${base},${sample},${plat},${file}\n" >> config.csv
done

talon_initialize_database --f refer/ath_talon_reformatted.gtf \
                          --a Col0 \
                          --g thale_cress \
                          --l 50 \
                          --5p 500 \
                          --3p 300 \
                          --o COL0


# run talon for many samples had finished  
talon --f config.csv \
      --db COL0.db \
      --build thale_cress \
      --threads 4 \
      --o ath

talon_summarize --db COL0.db --v --o talon_summmary

# abundance
talon_abundance \
       --db COL0.db \
       -a Col0 \
       --build thale_cress \
       --o example
# filter isoform-level analysis
talon_filter_transcripts \
       --db COL0.db \
       -a Col0 \
       --maxFracA 0.5 \
       --minCount 5 \
       --minDatasets 2 \
       --o filtered_transcripts.csv
# filter abundance
talon_abundance \
       --db COL0.db \
       -a Col0 \
       --build thale_cress \
       --whitelist filtered_transcripts.csv \
       --o example

# generate gtf 
talon_create_GTF --db COL0.db \
                 -a Col0 \
                 --build thale_cress \
                 --whitelist filtered_transcripts.csv \
                 --o new
