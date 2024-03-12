# RCAE验证20个基因

library(ggplot2)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/RACE_verify/')

# TBF1
df <- read.csv('TBF1.csv')
df$Ratio <- df$depth/max(df$depth)
head(df)
ID <- head(df$ts,1)
ID <- gsub('-cdna', '', ID)
ID
ggplot(data = df, aes(x = posi, y = Ratio, color = Source)) + 
  geom_line() + theme_classic() + ylab('Ratio of depth') + 
  xlab("Transcript coordinates") + ggtitle(ID) + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave('TBF1.pdf', width = 8, height = 6,units = 'in',dpi=300)

# ath
Ats <- c(1,2,3,4,5,6,7,9,10)
for (i in Ats){
  path <- sprintf("At%d.csv", i)
  out_name <- gsub('.csv', '.pdf' ,path)
  df <- read.csv(path)
  df$Ratio <- df$depth/max(df$depth)
  head(df)
  ID <- head(df$ts,1)
  ID <- gsub('-cdna', '', ID)
  ID
  ggplot(data = df, aes(x = posi, y = Ratio, color = Source)) + 
    geom_line() + theme_classic() + ylab('Ratio of depth') + 
    xlab("Transcript coordinates") + ggtitle(ID) + 
    theme(plot.title = element_text(hjust = 0.5))
  ggsave(out_name, width = 8, height = 6,units = 'in',dpi=300)
}

# rice 
Oss <- c(1,2,4,5,8,10)
for (i in Oss){
  path <- sprintf("Os%d.csv", i)
  out_name <- gsub('.csv', '.pdf' ,path)
  df <- read.csv(path)
  df$Ratio <- df$depth/max(df$depth)
  head(df)
  ID <- head(df$ts,1)
  ID <- gsub('-cdna', '', ID)
  ID
  ggplot(data = df, aes(x = posi, y = Ratio, color = Source)) + 
    geom_line() + theme_classic() + ylab('Ratio of depth') + 
    xlab("Transcript coordinates") + ggtitle(ID) + 
    theme(plot.title = element_text(hjust = 0.5))
  ggsave(out_name, width = 8, height = 6,units = 'in',dpi=300)
}


# End Count read的5' 端比对的情况

# TBF1
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/RACE_verify/')
df <- read.csv('TBF1_read.csv')
head(df)
df$Ratio <- df$ReadCount/max(df$ReadCount)
df$New_Position <- df$Position - df$leader5
head(df)
ID <- head(df$ts,1)
ID <- gsub('-cdna', '', ID)
ID
ggplot(data = df, aes(x = New_Position, y = Ratio, color = Source)) + 
  geom_linerange(aes(x = New_Position, ymax = Ratio, ymin=0)) +
  theme_classic() + ylab('Ratio of ReadCount') + 
  xlab("Transcript coordinates") + ggtitle(ID) + 
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_manual(values = c('5leaderP'='#385488', '5RACE'='#ED766D')) 
ggsave('tag/TBF1_read.pdf', width = 8, height = 6,units = 'in',dpi=300)

# ath
Ats <- c(1,2,3,4,5,6,7,9,10)
for (i in Ats){
  path <- sprintf("At%d_read.csv", i)
  out_name <- gsub('.csv', '.pdf' ,path)
  df <- read.csv(path)
  head(df)
  df$Ratio <- df$ReadCount/max(df$ReadCount)
  df$New_Position <- df$Position - df$leader5
  head(df)
  ID <- head(df$ts,1)
  ID <- gsub('-cdna', '', ID)
  ID
  ggplot(data = df, aes(x = New_Position, y = Ratio, color = Source)) + 
    geom_linerange(aes(x = New_Position, ymax = Ratio, ymin=0)) +
    theme_classic() + ylab('Ratio of ReadCount') + 
    xlab("Transcript coordinates") + ggtitle(ID) + 
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_color_manual(values = c('5leaderP'='#385488', '5RACE'='#ED766D'))
  ggsave(file.path('tag', out_name), width = 8, height = 6,units = 'in',dpi=300)
}


Oss <- c(1,2,4,5,8,10)
for (i in c(14)){
  path <- sprintf("Os%d_read.csv", i)
  out_name <- gsub('.csv', '.pdf' ,path)
  df <- read.csv(path)
  df$Ratio <- df$ReadCount/max(df$ReadCount)
  df$New_Position <- df$Position - df$leader5
  head(df)
  ID <- head(df$ts,1)
  ID <- gsub('-cdna', '', ID)
  ID
  ggplot(data = df, aes(x = New_Position, y = Ratio, color = Source)) + 
    geom_linerange(aes(x = New_Position, ymax = Ratio, ymin=0)) +
    theme_classic() + ylab('Ratio of depth') + 
    xlab("Transcript coordinates") + ggtitle(ID) + 
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_color_manual(values = c('5leaderP'='#385488', '5RACE'='#ED766D'))
  #ggsave(file.path('tag', out_name), width = 8, height = 6,units = 'in',dpi=300)
}


# 画成一张图 facet
total <- read.csv('One_map.csv')
head(total)
total$New_Position <- total$Position - total$leader5 -1

library(dplyr)

vline_data <- total %>%
  group_by(ts) %>%
  summarise(z = -mean(leader5))
vline_data

head(total)
ggplot(data = total, aes(x = New_Position, y = Ratio, color = Source)) + 
  geom_linerange(aes(x = New_Position, ymax = Ratio, ymin=0)) +
  theme_classic() + ylab('Ratio of tag count') + 
  xlab("Transcript coordinates") + 
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_manual(values = c('5leaderP'='#385488', '5RACE'='#ED766D')) +
  facet_wrap(~ts) + 
  geom_vline(aes(xintercept=z), vline_data, linetype='dashed')
ggsave('tag/One_map.pdf', width = 8, height = 6,units = 'in',dpi=300)
