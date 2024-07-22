# ITS2 Human trichuriasis post-processing
R-code to analyze ITS2 data from nanopore amplicon data

**If you use this, please cite:**

Citation to add

Thanks! :)

**Installation**

Install the following packages in R-studio:

**dada2 ; ShortRead; Biostrings**

Biostrings link: https://bioconductor.org/packages/release/bioc/html/Biostrings.html

ShortRead link: https://www.bioconductor.org/packages/release/bioc/html/ShortRead.html

dada2 link: https://benjjneb.github.io/dada2/dada-installation.html

**Usage**

This script uses the output from the pre-processing pipeline available at:

```bash
https://github.com/STPHxBioinformatics/ITS2_Trichuriasis_post_processing.git
```

The filename structure for the nanopore read files is as follows:

Target_nativebarcode_PCRbarcode_basecalling_sample (e.g. ITS2_01_bar_D_singlex_spl_P0311.fastq)
