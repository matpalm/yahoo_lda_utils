library(NCStats)
# see http://www.rforge.net/NCStats/files/

setwd("/home/mat/dev/yahoo_lda_utils/bin")
df = read.delim('foo.tsv', h=F, col.names=c('id','A','B','C','D','E'))

for(i in 1:nrow(df)) {
  row = df[i,]
  item_id = row$id
  topics = row[2:5]
  chi.sq = chisq.test(topics)
  fit = gofCI(chi.sq, conf.level=0.99)
  ci_lower = fit[,2]
  print(item_id)
  print(topics)
  print(ci_lower)
  residual = 1 - sum(ci_lower)
  print(residual)
}

df[1,]