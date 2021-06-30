# Written by Ashley Maloney and Zirui Wang 2021
# Make Data Frame with input excel data and the specific code (make a "-" if there's a 0)

import pandas as pd 
import numpy as np

df = pd.DataFrame(pd.read_excel('AA_Binary_Merge.xlsx ')) 
df ['State']= np.where(df['p_l']< 0.5, '-',df.State)
df.to_excel("AA_Binary_Merge_Gapped.xlsx" )

# Make general --> nodes number
node = 145

# Excel file: "AA_Binary_Merge"

text_file •open("Seqs_Gapped.fasta", "w")

for each_node in list(range(l,node+l)):
    state = df.loc(df ['Node'] == f"Node{each_node}"]["State"]
    text_file.write(">" + f"Node{each_node}\n") 
    text_file = open('Seqs_Gapped.fasta', 'a+')
    for each_state in state: 
        text_file.write(each_state)
text_file .write("\n") text_file.close()
