library(rGREAT)
library(dplyr)

bed <- read.table("/mnt/work1/users/hoffmangroup/zhiyuanl/BEHST/data/vista_LIMB_sorted_EDITED_FOR_GREAT.bed", sep="\t", header=FALSE)

names(bed)[1] <- "chr"
names(bed)[2] <- "start"
names(bed)[3] <- "end"

job = submitGreatJob(bed)

tb2 = getEnrichmentTables(job, download_by = "tsv")
nrow(tb2[["GO Molecular Function"]])

head(tb2[["GO Molecular Function"]])

mf <- tb2[["GO Molecular Function"]]
bp <- tb2[["GO Biological Process"]]
cc <- tb2[["GO Cellular Component"]]

# select useful columns
mf_res <- mf %>% select(Ontology, ID, Desc, BinomP, BinomBonfP, BinomFdrQ, HyperP, HyperBonfP, HyperFdrQ, Genes)
bp_res <- bp %>% select(Ontology, ID, Desc, BinomP, BinomBonfP, BinomFdrQ, HyperP, HyperBonfP, HyperFdrQ, Genes)
cc_res <- cc %>% select(Ontology, ID, Desc, BinomP, BinomBonfP, BinomFdrQ, HyperP, HyperBonfP, HyperFdrQ, Genes)

# concatenate dataframes
total <- rbind(mf_res, bp_res,cc_res) 

# write final output dataframe to file
write.table(total, "C:/Users/annie/data/limb_GREAT_res_all", sep="\t", quote=FALSE, row.names=FALSE)
