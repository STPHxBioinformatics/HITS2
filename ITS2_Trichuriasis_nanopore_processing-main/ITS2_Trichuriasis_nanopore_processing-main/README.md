# Human trichuriasis nanopore sequencing (ITS1/ITS2) - processing
Amplicon processing pipeline for ITS1/2 sequencing of human trichuriasis

**If you use this, please cite:**

Citation to add

Thanks! :)


**Installation**

Download the repository using the following command:

```bash
git clone https://github.com/STPHxBioinformatics/ITS2_Trichuriasis_nanopore_processing.git
```

```bash
cd Human_trichuriasis_nanopore_processing/
```

Use the provided configuration file ("ITS_processing_config_file.yml") to create a conda environment named ITS_processing with the required packages using the following command:

```bash
conda create --name ITS_processing --file ITS_processing_config_file.yml
```

Activate the environment using the command:

```bash
conda activate ITS_processing
```

Or use the provided *.sh file ("ITS_processing_slurm.sh") if you want to run the pipeline on a cluster using the SLURM scheduler

**Usage**
```python
ITS_processing.py [-h] -m MAIN_FOLDER -i INPUT_FOLDER [-t THREADS]
                         -step {0,1,2,3,4,5,6,7,8} [{0,1,2,3,4,5,6,7,8} ...]
                         [-v] [-vf]

optional arguments:
  -h, --help            show this help message and exit
  -m MAIN_FOLDER, --main_folder MAIN_FOLDER
                        Path to the main folder where the script will be
                        executed
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        Path to the input folder
  -t THREADS, --threads THREADS
                        Number of threads to use (default: 4)
  -step {0,1,2,3,4,5,6,7,8} [{0,1,2,3,4,5,6,7,8} ...]
                        Specify the step(s) to execute (1-8; 8 runs the
                        complete pipeline)
  -v, --verbose         Enable verbose output for detailed logging
  -vf, --verbose_full   Enable all verbose output for detailed logging
```

**Formatting of sequence and configuration files**

*A) The structure of the input fastq files contains the following information:*

- Target (ITS1 or ITS2)
- Basecalling type (duplex or singlex)
- The column the pool corresponds to, e.g. col 01-12 on the 96-well plate

As an example: ITS1_duplex_02.fastq

*B) The file containing the primer pairs ("primers.tab") is a tab-separated file and can be modified*

Here is the list of primer pairs used in the paper:
| |                                |                     |
|-|--------------------------------|---------------------|
|A|GAGCCCGTTCCGACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|B|TGGCACCGATTAACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|C|GACATACAATGAACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|D|ATGGTCTACTACACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|E|CCACTTGGATAGACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|F|CGATTATGGCACACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|G|CTTACGAGGCATACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|H|GTCCACCCTGGGACTGGCCGAACCAAGCCATC|TCTACGAGCCAAGTGATCCAC|
|A|GAGCCCGTTCCGTAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|B|TGGCACCGATTATAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|C|GACATACAATGATAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|D|ATGGTCTACTACTAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|E|CCACTTGGATAGTAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|F|CGATTATGGCACTAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|G|CTTACGAGGCATTAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|
|H|GTCCACCCTGGGTAGCCTCGTCTGATCTGAGG|ATGTCGACGCTACGCCTGTC|

*C) The sample layout file ("Sample_layout.txt") is also a tab-separated table which has the following structure*

|Column|Row|Sample|
|------|---|------|
|01|A|Sample001|

The column number corresponds to the sample column on the 96-well plate (01-12)
The row character corresponds to the sample row on the 96-well plate (A-H)
The sample column contains the sample information (sequencing ID or patient ID..)
