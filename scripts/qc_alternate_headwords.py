# -*- coding: utf-8 -*-
"""Find missing compounds. 

See https://github.com/sanskrit-lexicon/LRV/issues/12

Usage - python3 qc_alternate_headwords.py
"""
import codecs
import csv

if __name__ == "__main__":
	fout = codecs.open('../logs/issue12/brackets.txt', 'w', 'utf-8')
	with codecs.open('../interim/lrv_0.txt', 'r', 'utf-8') as fin:
		reader = csv.reader(fin, delimiter='\t')
		start = False
		for row in reader:
			lnum = row[0]
			pc = row[1]
			k1 = row[2]
			if '(' in k1:
				print('\t'.join(row))
				fout.write('\t'.join(row) + '\n')
	