import os
import sys
import re

def rename_files(directory, text_file, verbose=False):
    # Read the text file with pool, barcode, and sample information
    with open(text_file, 'r') as f:
        mapping_data = [line.strip().split() for line in f]

    # Define a regular expression pattern to extract information from filenames
    filename_pattern = re.compile(r'^(.*)ex_(.*)_bed_bar_(.*)\.bed$')

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.bed'):
            # Try to match the filename pattern
            match = filename_pattern.match(filename)
            
            if match:
                ex = match.group(2)
                bar = match.group(3)

                # Find the corresponding entry in the mapping data
                for entry in mapping_data:
                    if entry[0] == ex and entry[1] == bar:
                        # Build the new filename
                        new_filename = f'{match.group(1)}ex_{ex}_bar_{entry[1]}_spl_{entry[2]}.bed'

                        # Rename the file
                        old_path = os.path.join(directory, filename)
                        new_path = os.path.join(directory, new_filename)
                        os.rename(old_path, new_path)

                        if verbose:
                            print(f'Renaming: {filename} --> {new_filename}')

                        break
                else:
                    if verbose:
                        print(f'No mapping found for file: {filename}')
            else:
                if verbose:
                    print(f'Filename does not match pattern: {filename}')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <directory_path> <text_file_path> [--verbose]")
        sys.exit(1)

    directory_path = sys.argv[1]
    text_file_path = sys.argv[2]
    verbose = "--verbose" in sys.argv

    rename_files(directory_path, text_file_path, verbose)
