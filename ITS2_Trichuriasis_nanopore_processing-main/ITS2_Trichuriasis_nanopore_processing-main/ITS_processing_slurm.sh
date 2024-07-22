#!/bin/bash

#SBATCH --job-name=ITS_processing                   #This is the name of your job
#SBATCH --cpus-per-task=10                  #This is the number of cores reserved
#SBATCH --mem-per-cpu=5G              #This is the memory reserved per core.
#Total memory reserved: 50GB

#SBATCH --time=00:30:00        #This is the time that your task will run
#SBATCH --qos=30min           #You will run in this queue

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output=/path/to/stdout/ITS_processing_stdout.txt    #These are the STDOUT and STDERR files
#SBATCH --error=/path/to/stderr/ITS_processing_stderr.txt

#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=your@email.com        #You will be notified via email when your task ends or fails

#This job runs from the current working directory


#Remember:
#The variable $TMPDIR points to the local hard disks in the computing nodes.
#The variable $HOME points to your home directory.
#The variable $SLURM_JOBID stores the ID number of your job.


#load your required modules below
conda activate ITS_processing


#export your required environment variables below
#################################################


#add your command lines below
#Set variables
python3 ITS_processing.py -t 5 -v -step 8 -m /your/main/folder/ -i ./folder_with_input_fastq/
