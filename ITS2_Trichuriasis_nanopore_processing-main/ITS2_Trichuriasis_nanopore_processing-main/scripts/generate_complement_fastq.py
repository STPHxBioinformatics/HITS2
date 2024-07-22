import argparse
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os

def convert_to_complementary(sequence):
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
    complementary_sequence = ''.join([complement_dict[base] for base in sequence])
    return complementary_sequence

def reverse_and_complement(sequence, quality_scores):
    # Reverse the sequence and then apply the complement
    reversed_sequence = sequence[::-1]
    complemented_sequence = convert_to_complementary(reversed_sequence)

    # Reverse the quality scores as well
    reversed_quality_scores = quality_scores[::-1]

    return complemented_sequence, reversed_quality_scores

def get_target_sequence(filename):
    if "ITS1" in filename:
        return "CTAGAG"  # Replace with the ITS1 target sequence
    elif "ITS2" in filename:
        return "TAGCCT"  # Replace with the new ITS2 target sequence
    else:
        return None

def process_fastq(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".fastq"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace(".fastq", "_compl.fastq"))

            target_sequence = get_target_sequence(filename)

            if target_sequence:
                with open(output_file_path, 'w') as output_handle:
                    for record in SeqIO.parse(input_file_path, 'fastq'):
                        if str(record.seq).startswith(target_sequence):
                            reversed_complemented_sequence, reversed_quality_scores = reverse_and_complement(
                                str(record.seq), record.letter_annotations.get('phred_quality', [])
                            )
                            new_record = SeqRecord(Seq(reversed_complemented_sequence),
                                                  id=record.id, description=record.description)

                            # Preserve reversed quality scores
                            if reversed_quality_scores:
                                new_record.letter_annotations['phred_quality'] = reversed_quality_scores

                            SeqIO.write(new_record, output_handle, 'fastq')
                        else:
                            SeqIO.write(record, output_handle, 'fastq')

def main():
    parser = argparse.ArgumentParser(description='Convert sequences to complementary strand in FASTQ files.')
    parser.add_argument('input_folder', help='Path to the input folder containing FASTQ files')
    parser.add_argument('output_folder', help='Path to the output folder for modified FASTQ files')

    args = parser.parse_args()

    process_fastq(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
