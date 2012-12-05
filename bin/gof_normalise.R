library(NCStats)
# see http://www.rforge.net/NCStats/files/

setwd("/home/mat/dev/yahoo_lda_utils/bin")
df = read.delim('foo.tsv', h=F, col.names=c('id','A','B','C','D','E'))

calc_ci_lower = function(topics) {
  chi.sq = chisq.test(topics)
  fit = gofCI(chi.sq, conf.level=0.99)
  fit[,2]
}

t(apply(df[,2:6], 1, calc_ci_lower))
