# TSS enrichment
library(ggplot2)
library(reshape2)
library(dplyr)


setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/enrichment_analysis/')
# /home/zhusitao/database/plant/ath/representative_gene_model/GO
# /home/zhusitao/database/plant/ath/representative_gene_model/Araport11_cdna_20220914_representative_gene_model
# df <- read.csv('Shadow_GO_Biological_Process.csv') # 全部代表性转录本,后面只使用蛋白编码的
df <- read.csv('GO_Biological_Process_shadow_left_protein_coding_20230518.csv')
head(df)
df_filter <- filter(df, df$Enrichment.FDR < 0.05)
df_filter <- filter(df, df$Fold.Enrichment > 1.3)
dim(df_filter)
tmp <- head(arrange(df_filter, Fold.Enrichment), 35) # 升序排列; 降序排列为 desc(Enrichment.FDR)
tmp <- tail(tmp, 15) # 升序排列
dim(tmp)
# 根据其中一列的数值大小排序，指定X/Y轴排序，这里是更近有Fold.Enrichment的大小指定Y轴的顺序
tmp %>% 
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") +
  xlim(0,4) + theme_bw()
ggsave('left_represent_principal_protein_coding.pdf',width = 8, height = 6,units = 'in',dpi=300)

# right 
df <- read.csv('GO_Biological_Process_shadow_right_protein_coding_20230518.csv')
head(df)
dim(df)
# choose RNA
#df_filter <- filter(df, Fold.Enrichment >=1 & Enrichment.FDR < 0.05) # 根据p值和富集因子过滤
#df_filter <- filter(df_filter, grepl('RNA', Pathway)) #只显示RNA代谢相关的，
#tmp <- head(arrange(df_filter, Enrichment.FDR), 10) # 选取top10画图
#
df_filter <- filter(df, df$Enrichment.FDR < 0.05)
df_filter <- filter(df, df$Fold.Enrichment > 1.3)
dim(df_filter)
tmp <- head(arrange(df_filter, Enrichment.FDR), 35) # 升序排列; 降序排列为 desc(Enrichment.FDR)
tmp <- head(tmp, 20) # 升序排列

# 根据其中一列的数值大小排序，指定X/Y轴排序，这里是更近有Fold.Enrichment的大小指定Y轴的顺序
tmp %>% 
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
  ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") +
  xlim(0,3) + theme_bw()
ggsave('right_represent_principal_protein_coding.pdf',width = 8, height = 6,units = 'in',dpi=300)


# Fig2f
# 换分母(分母为检测到该基因的样本，分子为检测到的样本中该转录本是principal-isoform的样本数)
# 小于50% samples detected principal isoforms, 
lt05 <- read.csv('rank_lt09_gene_GO_Biological_Process.csv')
# lt05 <- read.csv('/Users/zhusitao/Downloads/enrichment_all (2).csv')
head(lt05)
dim(lt05)
lt05_filter <- filter(lt05, lt05$Enrichment.FDR < 0.05) # 首先根据p值过滤
head(lt05_filter)
dim(lt05_filter)
# 根据显著性排名前18位的
# tmp <- head(arrange(lt05_filter, Enrichment.FDR), 20)
# tmp <- tail(arrange(lt05_filter, Fold.Enrichment), 20) 
tmp <- filter(lt05_filter, Fold.Enrichment >=1 & Enrichment.FDR < 0.05) # 根据p值和富集因子过滤
#tmp <- filter(tmp, grepl('RNA', Pathway)) #只显示RNA代谢相关的，
tmp <- head(arrange(tmp, Enrichment.FDR), 15) # 选取top10画图
tmp$Enrichment.FDR
#tmp %>% filter(grepl('RNA', Pathway)) %>%
tmp %>%
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
  ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") + theme_bw() #+ 
  #scale_x_continuous(breaks = c(1.3,1.5,1.7,2), limits = c(1.3,2)) 
ggsave('lt09_GO.pdf',width = 10, height = 10,units = 'in',dpi=300)

### triple GO ####################################################
df <- read.csv('GO_triple.csv')
head(df)
colnames(df)
ggplot(data = df, aes(x = Source, y=Pathway)) + 
  geom_point(aes(size=Fold.Enrichment, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") + theme_classic()
ggsave('GO_triple.pdf',width = 10, height = 6,units = 'in',dpi=300)
### triple GO ######################################################

# greater than 50% samples detected principal isoforms
# gt05 <- read.csv('gt05_GO_Biological_Process_Transfer_ID.csv')
gt05 <- read.csv('gt05_GO_Biological_Process.csv')
gt05_filter <- filter(gt05, gt05$Enrichment.FDR < 0.001)
dim(gt05_filter)
tmp08 <- head(arrange(gt05_filter, Enrichment.FDR), 10)
# tmp08 <- tail(arrange(gt05_filter, Fold.Enrichment), 10)
tmp08 %>% 
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
  ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") + theme_bw() + xlim(0, 1.5)
ggsave('gt08_GO.pdf',width = 8, height = 6,units = 'in',dpi=300)


# utr5和CDS 共剪切的的基因的富集分析
co_as <- read.csv('co_utr5_cds_GO_Biological_Process.csv')
co_as_filter <- filter(co_as, co_as$Enrichment.FDR < 0.05)
tmp_co_as <- head(arrange(co_as_filter, Enrichment.FDR), 10)
tmp_co_as %>% 
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
  ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") + theme_bw() 
ggsave('co_utr5_CDS_GO.pdf',width = 8, height = 6,units = 'in',dpi=300)


# 评率最高的转录本，他们的基因对应的转录本有大于1，这些基因的占比
# 拟南芥中 isoform freq == 1的转录本有 7780，其中只有一个转录本的基因为5371，还有2409个有两个以上转录本
# /home/zhusitao/project/DPI/01.ath/All_isoforms_peak_process/12.transcript_per_gene
more_than_one <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/enrichment_analysis/enrichment_all (1).csv')
more_than_one_filter <- filter(more_than_one, more_than_one$Enrichment.FDR < 0.05)
tmp_more_than_one <- tail(arrange(more_than_one_filter, Enrichment.FDR), 15)
tmp_more_than_one %>% 
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
  ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") + theme_bw() 
ggsave('all_exist_principal_with_more_than_one.pdf',width = 8, height = 6,units = 'in',dpi=300)



# sankey 
# UTR sankey figure 反应流的信息
library(ggsankey)
library(dplyr)
library(ggplot2)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/enrichment_analysis/sankey')

df <- read.csv('go_sankey_RNA.csv')
df[,c("transcript_id")] <- list(NULL)
head(df)
df <- df %>% make_long(gene, Source, Pathway)
head(df)
ggplot(df, aes(x = x, 
               next_x = next_x, 
               node = node, 
               next_node = next_node,
               fill = factor(node))) +
  geom_sankey() + theme_classic()
ggsave('total_go_sankey.pdf',width = 8, height = 6,units = 'in',dpi=300)
