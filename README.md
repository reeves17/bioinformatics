# Bioinformatics
Posting of code I write to solve little bioinformatics-related problems here and there




## OmicCircos_Variants.R
### Go to my repository VCF-OmicCircos-Mapping for a full working version including example data
* Creates an OmicCircos plot mapping vcf and gff data

## cat_coverage.py
### merges .coverage files together
* Example: from one file, position 15 on Chr01 has been read 2 times says one file and another says position 15 on Chr01 has been read 6 times. The output will be that this has been read 8 times.
* This code also gets rid of positions that have been read 0 times, but that would be easy to change.

## vcf2OmicCircos.py
### another one you should look at in my VCF-OmicCircos-Mapping repository
* converts a vcf file to OmicCircos usable data

## fastq_percent_extraction_paired.py
### extracts a specified percentage of reads from paired-end fastq files
* Takes in arguments <data directory> <out directory> <percent>
* Note that this does not extract an exact percent of reads. Instead, it assigns each read a perecnt chance of being added to the output file. The if statement looks like:
 ''' if random.random() < (int(percent)/100.0): '''
