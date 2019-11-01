'''
pcc - Pearson
scc - Spearman
gcc - Gini

use - python3 coef.py syn_tsv tissue_tsv out_file

'''

import pandas as pd
import numpy as np
from sys import argv
from scipy.stats import pearsonr  # pcc
from scipy.stats import spearmanr # scc

##########
## VARS ##
##########

syn_tsv = argv[1]
tissue_tsv = argv[2]
out_file_name = argv[3]
out_file = open(out_file_name, "w")
tissue_data = pd.read_csv(tissue_tsv, sep='\t')
syn_data = pd.read_csv(syn_tsv, sep='\t')


###########
## FUNCS ##
###########

## Takes two gene names and returns correlation coefficients for them
def get_correlations(gene1, gene2):
    global out_file
    global tissue_data
    row1 = None
    row2 = None
    pcc = None
    pcc_pval = None
    
    # find row1
    for i in range(len(tissue_data.index)):
        gene = tissue_data.iloc[i, 0]
        if gene == gene1:
            row1 = tissue_data.iloc[i].drop(tissue_data.columns.values[0]).astype(float)
            break
    
    # find row2
    for i in range(len(tissue_data.index)):
        gene = tissue_data.iloc[i, 0]
        if gene == gene2:
            row2 = tissue_data.iloc[i].drop(tissue_data.columns.values[0]).astype(float)
            break
            
        
    # check if rows were found
    if row1 is None or row2 is None:
        return '', '', '', '', ''

    # get pcc (function is from scipy.stats)
    pcc, pcc_pval = pearsonr(row1, row2)

    # get Spearman (function is from scipy.stats)
    scc, scc_pval = spearmanr(row1, row2)

    # get Gini
    gcc = gini(row1, row2)

    print(str(pcc) + '\t' + str(gcc) + '\t' + str(scc))
    return pcc, pcc_pval, scc, scc_pval, gcc


# calculate gcc
def gini(x, w=None):
    # The rest of the code requires numpy arrays.
    x = np.asarray(x)
    w = np.asarray(w)
    sorted_indices = np.argsort(x)
    sorted_x = x[sorted_indices]
    sorted_w = w[sorted_indices]
    # Force float dtype to avoid overflows
    cumw = np.cumsum(sorted_w, dtype=float)
    cumxw = np.cumsum(sorted_x * sorted_w, dtype=float)
    return (np.sum(cumxw[1:] * cumw[:-1] - cumxw[:-1] * cumw[1:]) / 
            (cumxw[-1] * cumw[-1]))
    

############
### MAIN ###
############


## write out header
###################

# write already existing headers
for header in syn_data.columns.values:
    # write header values
    if header != syn_data.columns.values[0]:  # if not first header
        out_file.write(header)
    out_file.write('\t')
# write new correlation headers
out_file.write('pcc\tpcc_pval\tscc\tscc_pval\tgcc\n')


## get coefficients and write out
#################################
for i in range(len(syn_data.index)):
    gene1 = syn_data.iloc[i, 11]
    gene2 = syn_data.iloc[i, 12]
    pcc, pcc_pval, scc, scc_pval, gcc = get_correlations(gene1, gene2)
    out_file.write(syn_data.iloc[[i]].to_csv(sep='\t', index=False, header=False).rstrip() + 
                   '\t' + str(pcc) + '\t' + str(pcc_pval) + '\t' + str(scc) + '\t' + 
                   str(scc_pval) + '\t' + str(gcc) + '\n')

out_file.close()
