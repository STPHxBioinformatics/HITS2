library(dada2)
packageVersion("dada2")
library(ShortRead)
packageVersion("ShortRead")
library(Biostrings)
packageVersion("Biostrings")

path <- "Fastq_files/"
filt <- "filtered/"

list.files(path)

#List all files
Read_files <- sort(list.files(path, pattern = ".fastq", full.names = TRUE))

#Plot quality profiles
#plotQualityProfile(Read_files[1])

# Forward and reverse fastq filenames have the format:
filt_files <- sort(list.files(path, pattern = ".fastq", full.names = TRUE))

# Extract sample names, assuming filenames have format:
get.sample.name <- function(fname) strsplit(basename(fname), ".fastq")[[1]][1]
sample.names <- unname(sapply(filt_files, get.sample.name))
head(sample.names)

# Sequence filter -  change minLen to your actual amplicon length; maxEE = 15 (15/500 = < 3% error rate)
out <- filterAndTrim(filt_files, filt, minLen=425, maxLen=700, maxN=0, rm.phix=FALSE, maxEE=c(15), compress=FALSE)

#List all files
filtered_files <- sort(list.files(filt, pattern = ".fastq", full.names = TRUE))
head(out)

#Learn the error rates
errF <- learnErrors(filtered_files, multithread = TRUE)

#Plot errors
plotErrors(errF, nominalQ = TRUE)

#Dereplicate
derepFs <- derepFastq(filtered_files, verbose=TRUE)

#Sample inference
dadaFs <- dada(derepFs, err = errF, multithread = TRUE, pool=FALSE)
dadaFs[[1]]

#Construct sequence table
seqtab <- makeSequenceTable(dadaFs)

dim(seqtab)

# Inspect distribution of sequence lengths
table(nchar(getSequences(seqtab)))

#remove chimers
seqtab.nochim <- removeBimeraDenovo(seqtab, method="consensus", multithread=TRUE, verbose=TRUE)

# Create a data frame from the vector (as write.table expects a data frame)
data_frame <- data.frame(IntegerValue = seqtab)

# Calculate row sums
row_sums <- rowSums(data_frame)

# Replace values less than 0.1% of row sum with 0
threshold <- 0.01 * row_sums  # 0.1% threshold
data_frame[data_frame < threshold] <- 0

# Absolute reads threshold
abs_threshold <- 5  # 5 reads absolute threshold
data_frame <- data_frame[row_sums >= abs_threshold, ]

# Remove columns with a sum of 0
data_frame <- data_frame[, colSums(data_frame) != 0]

# Choose a file path and name for the output file
output_file <- "seqtab_table_ITS2_V4.txt"

# Use write.table to write the data frame to a tab-delimited text file
write.table(data_frame, file = output_file, sep = "\t", row.names = TRUE)


