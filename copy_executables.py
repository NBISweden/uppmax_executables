#!/usr/bin/env python
import os
import shutil
import argparse
import magic
import pdb

EXCLUDED_EXTENSIONS = {'.sh', '.pl', '.py', '.r', '.lua', '.c', '.h', '.o', '.tcl', '.sam', '.bam', '.gz', '.tar', '.java', '.a', 'fa', 'fasta', '.zip', '.bed', '.vcf', '.pdf', '.tsv', '.sample', '.txt', '.fai', '.hmm', '.info', }

def is_executable_binary(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK) and not os.path.islink(file_path) and 'executable' in magic.from_file(file_path, mime=True)

def copy_executables(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):

        print(f"Checking {root}")

        # skip git dirs
        if root.endswith('.git') or root.endswith('src'):
            continue


        for file in files:

            # not needed after the executable check above?
            _, ext = os.path.splitext(file)
            if ext.lower() in EXCLUDED_EXTENSIONS:
                continue

            # skip non executable
            if not is_executable_binary(os.path.join(root, file)):
                continue


            src_file_path = os.path.join(root, file)
            if os.access(src_file_path, os.X_OK):  # Check if the file is executable
                file_name = src_file_path.replace(os.sep, ".")
                if file_name.startswith("."):
                    file_name = file_name[1:]
                dest_file_path = os.path.join(dest_dir, file_name)
                shutil.copy(src_file_path, dest_file_path)
                print(f"Copied {src_file_path} to {dest_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Recursive copying of executable files to a specified directory.')
    parser.add_argument('-s', '--source', dest='source_directory', required=True, help='Path to the source directory')
    parser.add_argument('-d', '--destination', dest='destination_directory', required=True, help='Path to the destination directory')
    args = parser.parse_args()

    source_directory = os.path.abspath(args.source_directory)
    destination_directory = os.path.abspath(args.destination_directory)
    copy_executables(source_directory, destination_directory)
