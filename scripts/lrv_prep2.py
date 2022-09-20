# -*- coding: utf-8 -*-
"""Extract L-id, page-column, key1, key2

	e.g. <L>00017<pc>001-09<k1>अंशु<k2>अंशु

Usage - python3 lrv_prep2.py ../interim/lrv_1.txt ../interim/lrv_2.txt
"""
import sys
import csv
import re
import codecs


if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	reader = csv.reader(fin, delimiter='\t')
	h1 = ''
	for row in reader:
		lnum = row[0]
		pc = row[1]
		k2 = row[2]
		if k2.startswith('<p>'):
			clean_k2 = re.sub('<p>[ ]*', '', k2)
			h1 = clean_k2
		elif k2.startswith('<b>'):
			clean_k2 = h1 + re.sub('<b>[ ]*', '', k2)
		elif k2 == '':
			clean_k2 = clean_k2
		else:
			print(k2)
		prevhw = k2
		grammar = row[3]
		entry = row[4].rstrip()
		fout.write('<L>' + lnum + '<pc>' + pc + '<k1>' + clean_k2 + '<k2>' + clean_k2 + '\n')
		fout.write(lnum + '\t' + pc + '\t' + k2 + '\t' + grammar + '\t' + entry + '\n')
	fin.close()
	fout.close()
