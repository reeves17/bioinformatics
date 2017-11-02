from sys import argv
import random
import os
import re

###########
### VAR ###
###########

script, data_dir, out_dir, percent = argv
files = []

#################
### FUNCTIONS ###
#################


# Decides whether or not to include this piece of data based on randomness and
# percent given by user.
def include_data():
    global percent

    y_or_n = False
    if random.random() < (int(percent)/100.0):
        y_or_n = True
    return y_or_n


# Get list of fastq files
def get_fastq_files():
    global data_dir
    global files

    all_files = os.listdir(data_dir)
    for afile in all_files:
        if afile.endswith(".fastq") or afile.endswith(".fq"):
            files.append(afile)
    files.sort()


# Pull proper percent of reads from each file in files
def analyze_file_pair(file1, file2):
    global data_dir
    global out_dir
    file1_arr = re.split("\d_CA_R", file1)
    file2_arr = re.split("\d_CA_R", file2)
    out_file1 = open(out_dir + '/' + file1_arr[0] + out_dir[-2:] + 'percent' + '_' + file1_arr[1], 'w')
    out_file2 = open(out_dir + '/' + file2_arr[0] + out_dir[-2:] + 'percent' + '_' + file2_arr[1], 'w')
    insert_line = False
    lines = 0
    reads_out = set()
    # get how many lines in file
    with open(data_dir + '/' + file1, 'rb') as infile:
        for aline in infile:
            lines += 1
            if lines % 100000 == 0:
                print(lines)
    infile.close()
    print("got " + str(lines) +  " lines")
    # determine randomly based on percent which reads get included
    for aread in range(0, lines, 4):
        if include_data():
            reads_out.add(aread)
    
    print("made list")
    # write out from file1 based on reads_out
    with open(data_dir + '/' + file1, 'rb') as infile1:
        line_number = 0
        for aline in infile1:
            aline = str(aline)
            if line_number % 4 == 0:
                if line_number in reads_out:
                    insert_line = True
                else:
                    insert_line = False
            if insert_line:
                out_file1.write(aline)
            line_number += 1
    infile1.close()
    out_file1.close()
    # write out from file2 based on reads_out
    with open(data_dir + '/' + file2, 'rb') as infile2: 
        line_number = 0 
        for aline in infile2: 
            aline = str(aline) 
            if line_number % 4 == 0: 
                if line_number in reads_out: 
                    insert_line = True 
                else: 
                    insert_line = False 
            if insert_line: 
                out_file2.write(aline) 
            line_number += 1
    infile2.close()
    out_file2.close()


############
### MAIN ###
############

get_fastq_files()
for pair in range(0, len(files), 2):
    analyze_file_pair(files[pair], files[pair + 1])
