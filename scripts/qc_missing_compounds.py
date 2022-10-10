# -*- coding: utf-8 -*-
"""Find missing compounds. 

See https://github.com/sanskrit-lexicon/LRV/issues/14

Usage - python3 qc_missing_compounds.py
"""
import codecs
import re
import csv

if __name__ == "__main__":
	with codecs.open('../interim/lrv_0.txt', 'r', 'utf-8') as fin:
		reader = csv.reader(fin, delimiter='\t')
		start = False
		for row in reader:
			lnum = row[0]
			pc = row[1]
			k1 = row[2]
			# These two lnums have been manually corrected.
			# See https://github.com/sanskrit-lexicon/LRV/commit/347a08c8715ff6ebaffaec963d1ae4fcc7d73644
			# Therefore, these two lnums are not required to be shown.
			if lnum in ['16604', '43273']:
				continue
			# If there are more than one compounds and more than one sub-compounds
			if start:
				if ', ˚' in k1:
					print('\t'.join(row))
					print()
				else:
					start = False
			# If there are more than one compounds
			if ', -' in k1:
				start = True
