#!/usr/bin/env python


import os
import argparse
import pickle
import pdb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find the diffs between 2 ldd_crawler output files.')
    parser.add_argument('-d', dest='dardelo_file', required=True, help='Path to the dardelo file')
    parser.add_argument('-u', dest='uppmax_file', required=True, help='Path to the uppmax file')
    args = parser.parse_args()

    dardelo_filename = os.path.abspath(args.dardelo_file)
    uppmax_filename = os.path.abspath(args.uppmax_file)
    #output_file = os.path.abspath(args.output_file)



    # unpickle the files
    with open(dardelo_filename, 'rb') as file:
        # Load the pickled object
        dardelo = pickle.load(file)

    # unpickle the files
    with open(uppmax_filename, 'rb') as file:
        # Load the pickled object
        uppmax = pickle.load(file)


    # for each lib that is missing on dar-delo, find the path where it is on uppmax and print it
    for missing_lib in dardelo['missing_libs']:

        # skip empty ones
        if uppmax['lib_paths'][missing_lib] != 'None':

            # print the path to the missing libs
            print(uppmax['lib_paths'][missing_lib])







