from __future__ import print_function
from __future__ import division

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, gzip
from itertools import islice

os.chdir(r'/media/wilson/b776f228-366c-4e52-acd6-65df5b458e8c/Project_G/db.STRING/filter.Find.Sym.In.ProtAlias')
Genes = r'Mus_Gene.txt'
ProteinAlias = r'../2.Association.Data/10090.protein.aliases.v10.txt.gz'

with open(Genes, 'rb') as f:
	allGenes = [item.strip() for item in f]
	
Gene_in_ProteinAlias = []
Out = open(r'-'.join(['Gene_in', Genes]), 'wb')
with gzip.open(ProteinAlias, 'rb') as f:
	for line in islice(f, 1, None):
		line = line.strip().split('\t')
		#line[2] = line[2].split(' ')
		if line[1] in allGenes:
			Out.writelines('\t'.join(line) )
			Out.write('\n')
			
			Gene_in_ProteinAlias.append(line[1] )
	
Out.close()
	
Gene_in_ProteinAlias = set(Gene_in_ProteinAlias)
Gene_notIn_ProteinAlias = set(allGenes) ^ Gene_in_ProteinAlias
with open(r'-'.join(['Gene_notIn', Genes]), 'wb') as f:
	f.write('\n'.join(Gene_notIn_ProteinAlias))



