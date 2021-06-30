# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28, 2020 by Patrick Finneran (Menten AI)

Modified on Mon Apr 05, 2021 by Danny Woldring (MSU)
"""

'''
This script is part of the workflow necessary for determining the appropriate 
positioning of gaps, insertions, and deletions following IQ-Tree analysis for 
ancestral proteins (ASR).

1. Use standard amino acid sequence alignment to run IQ-Tree.
    iqtree -s MUSCLE_CDHit_BlastP_file.fasta -bb 1000 -alrt 1000 -asr
2. Convert amino acid sequence alignment into binary sequence alignment using this script.
   Note that you must change the 'fasta_fname' variable at bottom of script to match the 
   name of the file you wish to convert to binary.
3. Rerun IQ-Tree analysis using the phylogenetic tree calculated in step (1) and the 
   the following command:
    iqtree.exe -s KinDom_binary.fasta -te KinDom.tree -blfix -asr -m GTR2+FO -redo\
   where -te indivcates a fixed tree and KinDom.tree is the tree from step (1). GTR2+RO is 
   the preferred evolutionary model to use for recreating the ancestral sequences in this step.
4. Compare *.state file output to identify where gaps should exist.

'''

def fasta2dict(fasta,d={},not_allow_PDB=False,min_len=0,not_allow_X=True):
    ### Reads in fasta file
    ### Renames certain sequences based on forbidden characters in IQ Tree as needed
    with open(fasta) as infile:
        lines = infile.readlines()

    seq = ''
    key = None
    for line in lines:
        if line[0] == '>':
            if seq != '':
                if not_allow_X and 'X' in seq:
                    pass
                elif not_allow_PDB:
                    if key.split(' ')[0][4] == '_' and len(key.split(' ')[0]) == 6:
                        pass
                    else:
                        if len(seq.replace('-','')) >= min_len:
                            d[key] = seq
                else:
                    if len(seq.replace('-','')) >= min_len:
                        d[key] = seq
            key = line[1:].rstrip()
            seq = ''
        else:
            seq = seq + line.rstrip()
    if seq != '':
        if not_allow_X and 'X' in seq:
            pass
        elif not_allow_PDB:
            if key.split(' ')[0][4] == '_' and len(key.split(' ')[0]) == 6:
                pass
            else:
                if len(seq.replace('-','')) >= min_len:
                    d[key] = seq
        else:
            if len(seq.replace('-','')) >= min_len:
                d[key] = seq
    return d

def dict_2_fasta(fasta_d,fname):
    ### Saves dictionary to fasta. Where the dictionary key is the protein name
    ### and the value is the sequence
    with open(fname,'w') as out_fasta:
        for key in fasta_d.keys():
            out_fasta.write('>{}\n{}\n'.format(key,fasta_d[key]))
            


fasta_fname = 'KinDom.fasta'
fasta = fasta2dict(fasta_fname)

bin_fasta = {key:''.join(['0' if aa =='-' else '1' for aa in fasta[key]]) for key in fasta.keys()}
bin_fname = 'KinDom_binary.fasta'
dict_2_fasta(bin_fasta,bin_fname)

