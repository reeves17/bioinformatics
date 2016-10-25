#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
import os
import re

working_dir = argv[1]
data_dir = argv[2]
output_file = argv[3]
input_files = []
for i in range(4, len(argv)):
    input_files.append(argv[i])

#################
### FUNCTIONS ###
#################


# changes name of output_file if it already exists
def is_output_file_there(ofile):
    if os.path.isfile(working_dir + '/' + ofile):
        # change the value of ofile so previous runs will not be overwritten
        for incr in range(1, 1000):
            if os.path.isfile(working_dir + '/' + str(int) + '_' + ofile):
                pass
            else:
                ofile = str(int) + '_' + ofile
                break
    return ofile


def process_data(ifiles):
    temp_library = {}
    temp_library2 = {}
    for ifile in ifiles:
        with open(data_dir + '/' + ifile, 'rb') as infile:
            for line in infile:
                line = line.split('\t')
                # this re search and if statement only allows Chromosomes to be added to the output_file
                chr_search = re.search('^Chr', line[0])
                if chr_search is not None:
                    try:
                        try:
                            (temp_library[line[0]])[line[1]] += 1
                        except KeyError:
                            (temp_library[line[0]])[line[1]] = 1
                    # if line[0] is not in the dictionary, adds it
                    except KeyError:
                        temp_library[line[0]] = {}
                        try:
                            (temp_library[line[0]])[line[1]] += 1
                        except KeyError:
                            (temp_library[line[0]])[line[1]] = 1
    for a in temp_library:
        for b in temp_library[a]:
            # splits up by increments of 100k
            # int((temp_library[a])[b])
            var_range = b
            if len(var_range) > 5:
                var_range = var_range[:-5] + '00001'
            else:
                var_range = '1'
            # like asking if a is already in the dictionary, but takes less time
            try:
                try:
                    (temp_library2[a])[var_range] += 1
                except KeyError:
                    (temp_library2[a])[var_range] = 1
            # if a is not in the dictionary, adds it
            except KeyError:
                temp_library2[a] = {}
                try:
                    (temp_library2[a])[var_range] += 1
                except KeyError:
                    (temp_library2[a])[var_range] = 1
    return temp_library2


def export_library(thelibrary):
    outfile = open(working_dir + '/' + output_file, 'w')
    for a in thelibrary:
        for b in thelibrary[a]:
            outfile.write(a + '\t' + str(b) + '\t' + str((thelibrary[a])[b]) + '\n')
    outfile.close()


############
### MAIN ###
############

output_file = is_output_file_there(output_file)
data_library = process_data(input_files)
export_library(data_library)
