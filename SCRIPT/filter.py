from __future__ import print_function

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# ----- Build 12/26/2016 -----
# Before you running this script, you must run filter.awk first.
# After that, you would get 3 files, which is nessesary for this script. These files are:
# 'Ensemble.ENSP2ENSG.tsv': the crosslink between ENSP and ENSG, which was extraced from file '9606.protein.aliases.v10.txt.gz'
# 'link.higher9.ENSP.tsv': the high level links, note that the nodes are ENSP, , which was extraced from file '9606.protein.links.v10.txt.gz'
# [!Skip]'gencode.v22.annotation.tsv': the annotations of all ensemble gene id, which was extraced from file 'gencode.v22.annotation.used4FPKM.csv'
# ----- Updata 12/27/2016 -----
# Skip building the 'linkedDict' steps.
# change the ENSP to ENSG in file 'link.higher9.ENSP.tsv', and save the results to file 'link.higher9.ENSG.tsv', 
# The links in this file will be used to background networks for constructing the single-sample networks

import os, pickle
import pandas as pd
from pandas import DataFrame

os.chdir(r'E:/Project_G/db.STRING')

# construct the dictionary of all links		
with open(r'Ensemble.ENSP2ENSG.tsv', 'rb') as handle:
	mapping = {}
	for line in handle:
		line = line.strip().split('\t')
		mapping[line[0] ] = line[1]

with open(r'link.higher9.ENSP.tsv', 'rb') as handle:
	count = 0
	links = []
	for line in handle:
		line = line.strip().split('\t')
		if mapping.has_key(line[0]) and mapping.has_key(line[1]):
			line[0] = mapping[line[0] ]
			line[1] = mapping[line[1] ]
			links.append([line[0], line[1] ] )
		else:
			count += 1

linksDF = DataFrame(links)
linksDF.to_csv(r'link.higher9.ENSG.tsv', sep='\t', header=False, index=False)
					
# Skip the following steps
linkedDict = {}
for item in links:
	if linkedDict.has_key(item[0] ):
		linkedDict[item[0] ].append(item[1] )
	else:
		linkedDict[item[0] ] = [item[1] ]

# Find the overlap between gencode id and all node in the links
with open(r'gencode.v22.annotation.tsv', 'rb') as handle:
	gencode = [line.strip().split('\t')[0] for line in handle]

gencode = set(gencode)
node = set(linkedDict.keys() )
selectedNode = gencode & node
excludedNode = node - selectedNode
for item in excludedNode:
	linkedDict.pop(item)
	
for key in selectedNode:
	for item in linkedDict[key]:
		if item not in selectedNode:
			linkedDict[key].remove(item)
		
	if len(linkedDict[key] ) == 0:
		linkedDict.pop(key)

# Finally, the linkedDict contains all possible nodes and its corresponding links that 
# can be used to construct the single-sample networks
# Result: node, 11005; links: 427791
# Save linkedDict to a pickle object
with open(r'linkedDict.pickle', 'wb') as handle:
	pickle.dump(linkedDict, handle)

