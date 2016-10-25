#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
concatenates all coverage files to see how many times each area has been covered by all reads
'''

from sys import argv
import os
import random

script_name, working_dir, data_dir = argv

#################
### FUNCTIONS ###
#################

def getFilesThatEndWith(endOfFileName):
    allfiles = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    correctFiles = []
    for afile in allfiles:
        if afile.endswith(endOfFileName) and afile != output_file:
            correctFiles.append(afile)
    print 'step1'
    return correctFiles


def isOutputFileThere(ofile):
    if os.path.isfile(ofile):
        ofile = random.choice('abcdefghijk') + random.choice('abcdefghijk') + random.choice('abcdefghijk') + '_' + ofile
    return ofile


def processData(files):
    temp_library = {}
    for afile in files:
        with open(data_dir + '/' + afile, 'rb') as infile:
            for line in infile:
                line = line.split('\t')
                line[2] = int(line[2])
                try:
                    if line[2] != 0:
                        try:
                            (temp_library[line[0]])[str(line[1])] += line[2]
                        except KeyError:
                            (temp_library[line[0]])[str(line[1])] = line[2]
                except KeyError:
                    temp_library[line[0]] = {}
                    if line[2] != 0:
                        try:
                            (temp_library[line[0]])[str(line[1])] += line[2]
                        except KeyError:
                            (temp_library[line[0]])[str(line[1])] = line[2]
    return temp_library


def exportLibrary(thelibrary):
    outfile = open(working_dir + '/' + output_file, 'w')
    for a in thelibrary:
        for b in thelibrary[a]:
            outfile.write(a + '\t' + str(b) + '\t' + str((thelibrary[a])[b]) + '\n')
    outfile.close()


#################
### VARIABLES ###
#################

output_file = 'cat_coverage.coverage'

############
### MAIN ###
############

list_coverage = getFilesThatEndWith('.coverage')
output_file = isOutputFileThere(output_file)
data_library = processData(list_coverage)
exportLibrary(data_library)
