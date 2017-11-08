"""
@author Jacob Reeves
@author jake.reeves2013@gmail.com

REQUIRES PYTHON 3

**IMPORTANT NOTE WHEN RUNNING ON SAPELO:
    After importing python/3.4.3, you need to run it as python3...

This script extracts APPROXIMATELY a defined integer percent of
reads from either single-end or paired-end reads from one or two
fastq or fq files depending on whether single or paired. The input
files(s) can be gzipped or not. They will be written out to the
specified directory with the prefix xpercent_filename where x is
the percent specified and filename is the input file.

SINGLE END ARGS
argv[1] integer percent of reads to be extracted
argv[2] input file
argv[3] out directory

PAIRED END ARGS
argv[1] integer percent of reads to be extracted
argv[2] first paired file
argv[3] second paired file
argv[4] out directory
"""

from sys import argv
from sys import exit
import random
import os
import gzip
from subprocess import check_call
import time

############
### VARS ###
############

# check for proper arg length
if len(argv) == 4 or len(argv) == 5:
    pass
else:
    print("The arguments passed in must be of the form\n<percent>\t" +
          "<input file>\t<optional paired input file>\t<out directory>")
    exit(0)

percent = 0
try:
    percent = int(argv[1])
except ValueError:
    print(argv[1] + " is not an integer.")
    exit(0)
file = ""  # will be used if single end
files = []  # will be used if paired end
out_dir = ""
paired = False
if len(argv) == 5:  # if paired end
    paired = True
    files.append(argv[2])
    files.append(argv[3])
    out_dir = argv[4]
else:  # if single end
    file = argv[2]
    out_dir = argv[3]


#################
### FUNCTIONS ###
#################


# Decides whether or not to include this piece of data based on pseudo-randomness
# and the percent given by user.
def include_data():
    global percent
    y_or_n = False
    if random.random() < (int(percent) / 100.0):
        y_or_n = True
    return y_or_n


# Checks if a file exists
def check_file_exists(thefile):
    if os.path.isfile(thefile):
        return
    else:
        print("The file " + thefile + " does not exist.")
        exit(0)


def check_dir_exists(thedir):
    if os.path.isdir(thedir):
        return
    else:
        print("The directory " + thedir + " does not exist.")
        exit(0)


def gzip_file(afile):
    check_call(['gzip', afile])


# main extraction function for paired-end reads
def analyze_paired():
    global files
    global percent
    sample1 = files[0].split("/")
    sample1 = sample1[len(sample1) - 1]
    sample2 = files[1].split("/")
    sample2 = sample2[len(sample2) - 1]
    out_file1name = ""
    out_file2name = ""
    # if files are a valid fq or fastq file gzipped or not
    if ((files[0].endswith(".fq") or files[0].endswith(".fq.gz") or files[0].endswith(".fastq") or
        files[0].endswith(".fastq.gz")) and (files[1].endswith(".fq") or files[1].endswith(".fq.gz") or
        files[1].endswith(".fastq") or files[1].endswith(".fastq.gz"))):
        out_file1name = (files[0])[:(-1 * (len(sample1)))] + str(percent) + 'percent_' + sample1
        out_file2name = (files[1])[:(-1 * (len(sample2)))] + str(percent) + 'percent_' + sample2
    else:
        print("The files " + files[0] + " and " + files[1] + " are not valid fq or fastq files.")
        exit(0)
    out_file1 = open(out_file1name, 'w')
    out_file2 = open(out_file2name, 'w')

    insert_line = False
    lines = 0
    reads_out = set()  # sets make the recall MUCH faster
    # get line count
    if files[0].endswith(".gz"):  # is gzipped
        with gzip.open(files[0], 'r') as infile:
            for aline in infile:
                lines += 1
    else:  # is not gzipped
        with open(files[0], 'rb') as infile:
            for aline in infile:
                lines += 1
    # determine pseudo-randomly based on percent which reads get included
    for aread in range(0, lines, 4):
        if include_data():
            reads_out.add(aread)
    # write out from files[0] based on reads_out
    if files[0].endswith(".gz"):  # is gzipped
        with gzip.open(files[0], 'r') as infile1:
            line_number = 0
            for aline in infile1:
                aline = str(aline)
                if line_number % 4 == 0:
                    if line_number in reads_out:
                        insert_line = True
                    else:
                        insert_line = False
                if insert_line:
                    if aline.endswith("\\n\'"):
                        out_file1.write(aline[2:-3] + '\n')
                    else:
                        out_file1.write(aline[2:] + '\n')
                line_number += 1
        out_file1.close()
        gzip_file(out_file1name)
        # write out from files[1] based on reads_out
        with gzip.open(files[1], 'r') as infile2:
            line_number = 0
            for aline in infile2:
                aline = str(aline)
                if line_number % 4 == 0:
                    if line_number in reads_out:
                        insert_line = True
                    else:
                        insert_line = False
                if insert_line:
                    if aline.endswith("\\n\'"):
                        out_file2.write(aline[2:-3] + '\n')
                    else:
                        out_file2.write(aline[2:] + '\n')
                line_number += 1
        out_file2.close()
        gzip_file(out_file2name)
    else:  # not gzipped
        with open(files[0], 'rb') as infile1:
            line_number = 0
            for aline in infile1:
                aline = str(aline)
                if line_number % 4 == 0:
                    if line_number in reads_out:
                        insert_line = True
                    else:
                        insert_line = False
                if insert_line:
                    if aline.endswith("\\n\'"):
                        out_file1.write(aline[2:-3] + '\n')
                    else:
                        out_file1.write(aline[2:] + '\n')
                line_number += 1
        out_file1.close()
        gzip_file(out_file1name)
        # write out from files[1] based on reads_out
        with open(files[1], 'rb') as infile2:
            line_number = 0
            for aline in infile2:
                aline = str(aline)
                if line_number % 4 == 0:
                    if line_number in reads_out:
                        insert_line = True
                    else:
                        insert_line = False
                if insert_line:
                    if aline.endswith("\\n\'"):
                        out_file2.write(aline[2:-3] + '\n')
                    else:
                        out_file2.write(aline[2:] + '\n')
                line_number += 1
        out_file2.close()
        gzip_file(out_file2name)


# main extraction function for single-end reads
def analyze_single():
    global file
    global percent
    out_filename = ""
    sample = file.split("/")
    sample = sample[len(sample) - 1]
    # if file is a valid fastq file gzipped or not
    if file.endswith(".fq") or file.endswith(".fq.gz") or file.endswith(".fastq") or file.endswith(".fastq.gz"):
        out_filename = file[:(-1 * (len(sample)))] + str(percent) + 'percent_' + sample
    else:
        print("The file " + file + " is not a valid fq or fastq file.")
        exit(0)
    out_file = open(out_filename, 'w')

    insert_line = False
    lines = 0
    reads_out = set()  # sets make the recall MUCH faster
    # get line count
    if file.endswith(".gz"):  # is gzipped
        with gzip.open(file, 'r') as infile:
            for aline in infile:
                lines += 1
    else:  # is not gzipped
        with open(file, 'rb') as infile:
            for aline in infile:
                lines += 1
    # determine pseudo-randomly based on percent which reads get included
    for aread in range(0, lines, 4):
        if include_data():
            reads_out.add(aread)
    # write out from files[0] based on reads_out
    if file.endswith(".gz"):  # is gzipped
        with gzip.open(file, 'r') as infile:
            line_number = 0
            for aline in infile:
                aline = str(aline)
                if line_number % 4 == 0:
                    if line_number in reads_out:
                        insert_line = True
                    else:
                        insert_line = False
                if insert_line:
                    if aline.endswith("\\n\'"):
                        out_file.write(aline[2:-3] + '\n')
                    else:
                        out_file.write(aline[2:] + '\n')
                line_number += 1
        out_file.close()
        gzip_file(out_filename)
    else:  # not gzipped
        with open(file, 'rb') as infile:
            line_number = 0
            for aline in infile:
                aline = str(aline)
                if line_number % 4 == 0:
                    if line_number in reads_out:
                        insert_line = True
                    else:
                        insert_line = False
                if insert_line:
                    if aline.endswith("\\n\'"):
                        out_file.write(aline[2:-3] + '\n')
                    else:
                        out_file.write(aline[2:] + '\n')
                line_number += 1
        out_file.close()
        gzip_file(out_filename)


############
### MAIN ###
############

if paired:
    check_file_exists(files[0])
    check_file_exists(files[1])
    check_dir_exists(out_dir)
    analyze_paired()
else:
    check_file_exists(file)
    check_dir_exists(out_dir)
    analyze_single()
