# bioinformatics
Posting of code I write to solve little binf problems here and there

### OmicCircos_Variants.R
#### Go to my repository VCF-OmicCircos-Mapping for a full working version including example data
* Creates an OmicCircos plot mapping vcf and gff data

### cat_coverage.py
#### merges .coverage files together
* Example: from one file, position 15 on Chr01 has been read 2 times says one file and another says position 15 on Chr01 has been read 6 times. The output will be that this has been read 8 times.
* This code also gets rid of positions that have been read 0 times, but that would be easy to change.

### vcf2OmicCircos.py
#### another one you should look at in my VCF-OmicCircos-Mapping repository
* converts a vcf file to OmicCircos usable data
