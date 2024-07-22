# ITS_processing.py
# Cleans up and extract amplicons generated using the ITS1 or ITS2 primers described in
# add citation
# 

import argparse
import os
import subprocess
import shutil

def create_main_folder(main_folder, verbose=False):
    os.makedirs(main_folder, exist_ok=True)

def run_command_its1_its2(input_folder, verbose=False):
    os.chdir(input_folder)
    qual_length_filter_folder = os.path.join(main_folder, "01_qual_length_filter")
    os.makedirs(qual_length_filter_folder, exist_ok=True)

    command_its1 = "ls ITS1*.fastq | awk -F '.fastq' '{print $1}' | sort | uniq > ID_ITS1"
    subprocess.run(command_its1, shell=True)
    if verbose_full:
        print(f"Executed: {command_its1}")

    command_its2 = "ls ITS2*.fastq | awk -F '.fastq' '{print $1}' | sort | uniq > ID_ITS2"
    subprocess.run(command_its2, shell=True)
    if verbose_full:
        print(f"Executed: {command_its2}")

    shutil.move("ID_ITS1", os.path.join(main_folder, "ID_ITS1"))
    shutil.move("ID_ITS2", os.path.join(main_folder, "ID_ITS2"))

    os.chdir(main_folder)

    command_seqkit_its1 = (
        "for i in $(cat ./ID_ITS1); "
        f"do seqkit seq -j {threads} -Q 9 --min-len 800 --max-len 900 ./{input_folder}/$i\.fastq > "
        f"./01_qual_length_filter/$i\_qual_leng_filt.fastq; done"
    )
    subprocess.run(command_seqkit_its1, shell=True)
    if verbose_full:
        print(f"Executed: {command_seqkit_its1}")

    command_seqkit_its2 = (
        "for i in $(cat ./ID_ITS2); "
        f"do seqkit seq -j {threads} -Q 9 --min-len 450 --max-len 750 ./{input_folder}/$i\.fastq > "
        f"./01_qual_length_filter/$i\_qual_leng_filt.fastq; done"
    )
    subprocess.run(command_seqkit_its2, shell=True)
    if verbose_full:
        print(f"Executed: {command_seqkit_its2}")

    if verbose:
        print("Step 1: Quality and length filter done\n")

def create_pool_demul_folder(main_folder, verbose=False):
    pool_demul_folder = os.path.join(main_folder, "02_pool_demul")
    os.makedirs(pool_demul_folder, exist_ok=True)

    command_seqkit_amplicon_its1 = (
        "for i in $(cat ./ID_ITS1); "
        f"do seqkit -j {threads} amplicon -m 0 -p primers.tab -r 12:-21 "
        f"./01_qual_length_filter/$i\_qual_leng_filt.fastq --bed > "
        f"./02_pool_demul/$i\_bed.txt; done"
    )
    subprocess.run(command_seqkit_amplicon_its1, shell=True)
    if verbose_full:
        print(f"Executed: {command_seqkit_amplicon_its1}")

    command_seqkit_amplicon_its2 = (
        "for i in $(cat ./ID_ITS2); "
        f"do seqkit -j {threads} amplicon -m 0 -p primers.tab -r 13:-1 "
        f"./01_qual_length_filter/$i\_qual_leng_filt.fastq --bed > "
        f"./02_pool_demul/$i\_bed.txt; done"
    )
    subprocess.run(command_seqkit_amplicon_its2, shell=True)
    if verbose_full:
        print(f"Executed: {command_seqkit_amplicon_its2}")

    os.chdir(main_folder)

    if verbose:
        print("Step 2: Generating BED files completed\n")

def call_python_script(main_folder, pool_demul_folder, verbose=False):
    os.chdir(main_folder)

    split_bed_files_folder = os.path.join(main_folder, "03_split_bed_files")
    os.makedirs(split_bed_files_folder, exist_ok=True)

    for i in ["ID_ITS1", "ID_ITS2"]:
        for file in os.listdir(pool_demul_folder):
            if file.endswith("_bed.txt") and os.path.isfile(os.path.join(pool_demul_folder, file)):
                input_bed_file = os.path.join(pool_demul_folder, file)
                output_prefix = os.path.join(main_folder, "03_split_bed_files", os.path.splitext(file)[0] + "_bar")
                command_split_bed = f"python3 scripts/split_bed_files.py {input_bed_file} {output_prefix}"
                subprocess.run(command_split_bed, shell=True)
                if verbose_full:
                    print(f"Executed: {command_split_bed}")

    os.chdir(main_folder)
    if verbose:
        print("Step 3: Splitting BED files completed\n")

def rename_sample_files(main_folder, verbose=False):
    
    os.chdir(main_folder)

    command_retrieve_info = (
        f"python3 scripts/rename_samples.py "
        f"{os.path.join(main_folder, '03_split_bed_files')} "
        f"{'Sample_layout.txt'}"
    )
    subprocess.run(command_retrieve_info, shell=True)
    if verbose:
        print("Step 4: The sample name was added to the corresponding sample bed file\n")
            
def create_sample_fastq_folder(main_folder, verbose=False):
    sample_fastq_files_folder = os.path.join(main_folder, "04_sample_fastq_files")
    os.makedirs(sample_fastq_files_folder, exist_ok=True)

#    shutil.move(os.path.join(main_folder, "ID_ITS1"), os.path.join(main_folder, "ID_ITS1"))
#    shutil.move(os.path.join(main_folder, "ID_ITS2"), os.path.join(main_folder, "ID_ITS2"))

    os.chdir(main_folder)
     
    command_retrieve_info = (
        f"python3 scripts/retrieve_quality_information_for_fastq_files.py "
        f"{os.path.join(main_folder, '01_qual_length_filter')} "
        f'"{os.path.join(main_folder, "03_split_bed_files", "*_bar_*.bed")}" '
        f"-o {sample_fastq_files_folder}"
    )
    subprocess.run(command_retrieve_info, shell=True)
    if verbose_full:
        print(f"Executed: {command_retrieve_info}")
    if verbose:
        print("Step 5: Retrieving quality information from original fastq done\n")
        
def final_length_filter(main_folder, verbose=False):
#    print("Step 6: Creating 06_final_length_filter directory.")
    final_length_filter_folder = os.path.join(main_folder, "05_final_length_filter")
    os.makedirs(final_length_filter_folder, exist_ok=True)
#    print(f"Step 6: Changing directory to {os.path.join(main_folder, '04_sample_fastq_files')}.")
    os.chdir(os.path.join(main_folder, "04_sample_fastq_files"))

    command_extract_info = (
        "ls *.fastq | awk -F '_extracted.fastq' '{print $1}' | sort | uniq > ID_FILT"
    )
    subprocess.run(command_extract_info, shell=True)
    if verbose_full:
        print(f"Executed: {command_extract_info}")

    shutil.move("ID_FILT", os.path.join(main_folder, "ID_FILT"))

    os.chdir(main_folder)

    command_final_length_filter = (
        "for i in $(cat ./ID_FILT); "
        f"do seqkit seq -j {threads} --min-len 425  04_sample_fastq_files/$i\_extracted.fastq > "
        f"05_final_length_filter/$i\_2nd_len_filter.fastq; done"
    )
    subprocess.run(command_final_length_filter, shell=True)
    if verbose_full:
        print(f"Executed: {command_final_length_filter}")
    if verbose:
        print("Step 6: Length filtering completed\n")

def complement_fastq(main_folder, verbose=False):
#    print("Step 7: Creating 06_curated_fastq.")
    curated_fastq_folder = os.path.join(main_folder, "06_curated_fastq")
    os.makedirs(curated_fastq_folder, exist_ok=True)

    command_generate_complement = (
        f"python3 scripts/generate_complement_fastq.py "
        f"{os.path.join(main_folder, '05_final_length_filter')} "
        f"{os.path.join(main_folder, '06_curated_fastq')}"
    )
    subprocess.run(command_generate_complement, shell=True)
    
    if verbose_full:
        print(f"Executed: {command_generate_complement}")
    if verbose:
        print("Step 7: Complement files generated")
        
    if verbose:
        print("All steps completed.")

def run_all_steps(main_folder, input_folder, verbose=False):
    create_main_folder(main_folder, verbose)
    run_command_its1_its2(input_folder, verbose)
    create_pool_demul_folder(main_folder, verbose)
    call_python_script(main_folder, os.path.join(main_folder, "02_pool_demul"), verbose)
    rename_sample_files(main_folder, verbose)
    create_sample_fastq_folder(main_folder, verbose)
    final_length_filter(main_folder, verbose)
    complement_fastq(main_folder, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input folder.")
    parser.add_argument("-m", "--main_folder", required=True, help="Path to the main folder where the script will be executed")
    parser.add_argument("-i", "--input_folder", required=True, help="Path to the input folder")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads to use (default: 4)")
    parser.add_argument("-step", type=int, nargs='+', required=True, choices=range(0, 9),
                        help="Specify the step(s) to execute (1-8; 8 runs the complete pipeline)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for detailed logging")
    parser.add_argument("-vf", "--verbose_full", action="store_true", help="Enable all verbose output for detailed logging")
    
    args = parser.parse_args()
    main_folder = args.main_folder
    input_folder = args.input_folder
    threads = args.threads
    verbose = args.verbose
    verbose_full = args.verbose_full

    if 1 in args.step:
        create_main_folder(main_folder, verbose)
        run_command_its1_its2(input_folder, verbose)
    if 2 in args.step:
        create_pool_demul_folder(main_folder, verbose)
    if 3 in args.step:
        call_python_script(main_folder, os.path.join(main_folder, "02_pool_demul"), verbose)
    if 4 in args.step:
        rename_sample_files(main_folder, verbose)
    if 5 in args.step:
        create_sample_fastq_folder(main_folder, verbose)
    if 6 in args.step:
        final_length_filter(main_folder, verbose)
    if 7 in args.step:
        complement_fastq(main_folder, verbose)
    if 8 in args.step:
        create_main_folder(main_folder, verbose)
        run_command_its1_its2(input_folder, verbose)
        create_pool_demul_folder(main_folder, verbose)
        call_python_script(main_folder, os.path.join(main_folder, "02_pool_demul"), verbose)
        rename_sample_files(main_folder, verbose)
        create_sample_fastq_folder(main_folder, verbose)
        final_length_filter(main_folder, verbose)
        complement_fastq(main_folder, verbose)
