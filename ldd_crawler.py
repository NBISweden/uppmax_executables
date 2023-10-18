#!/usr/bin/env python
import os
import shutil
import argparse
import magic
import pdb
import lddwrap
import pathlib
import pickle

EXCLUDED_EXTENSIONS = {'.sh', '.pl', '.py', '.r', '.lua', '.c', '.h', '.o', '.tcl', '.sam', '.bam', '.gz', '.tar', '.java', '.a', 'fa', 'fasta', '.zip', '.bed', '.vcf', '.pdf', '.tsv', '.sample', '.txt', '.fai', '.hmm', '.info', }

def is_executable_binary(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK) and not os.path.islink(file_path) and 'executable' in magic.from_file(file_path, mime=True)

def ldd_checker(src_dir, output_file):

    # test output file before starting to crawl
    with open(output_file, 'w') as output_file_handle:
        pass

    # init
    missing_libs = set()
    lib_paths    = {}
    software2lib = {}
    lib2software = {}

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

            path = pathlib.Path(os.path.join(root, file))
            try:
                deps = lddwrap.list_dependencies(path=path)
            except:
                pass
            for dep in deps:

                # save missing deps
                if not dep.found:
                    missing_libs.add(dep.soname)

                # save lib and software info
                lib_paths[dep.soname] = str(dep.path)

                try:
                    software2lib[os.path.join(root, file)].add(dep.soname)
                except:
                    software2lib[os.path.join(root, file)] = [dep.soname]

                try:
                    lib2software[dep.soname].add(os.path.join(root, file))
                except:
                    lib2software[dep.soname] = [os.path.join(root, file)]
    # save lists
    pickle.dump( {'lib_paths':lib_paths, 'missing_libs':missing_libs, 'software2lib':software2lib , 'lib2software':lib2software}, open( output_file, "wb" ) )





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Recursive checking of executable files to see which libraries they use (ldd)')
    parser.add_argument('-i', '--inputdir', dest='input_directory', required=True, help='Path to the input directory')
    parser.add_argument('-o', '--outputfile', dest='output_file', required=True, help='Path to the output file')
    args = parser.parse_args()

    input_directory = os.path.abspath(args.input_directory)
    output_file = os.path.abspath(args.output_file)
    ldd_checker(input_directory, output_file)
