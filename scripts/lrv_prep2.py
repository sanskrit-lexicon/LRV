# -*- coding: utf-8 -*-
"""Extract L-id, page-column, key1, key2

	e.g. <L>00017<pc>001-09<k1>अंशु<k2>अंशु

Usage - python3 lrv_prep2.py ../interim/lrv_1.txt ../interim/lrv_2.txt
"""
import sys
import csv
import re
import codecs


def remove_markup(hw):
	hw = re.sub('<p>[ ]*', '', hw)
	hw = re.sub('<b>[ ]*', '', hw)
	hw = re.sub('<\+>[ ]*', '', hw)
	return hw


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
		h1 = row[2]
		k2 = row[3]
		k1 = row[4]
		grammar = row[5]
		entry = row[6]
		charcount = row[7].rstrip()
		if h1.startswith('<p>'):
			clean_h1 = remove_markup(h1)
			clean_k2 = remove_markup(k2)
			clean_k1 = remove_markup(k1)
			clean_pc = pc
		elif h1.startswith('<b>'):
			clean_h1 = remove_markup(k1)
			clean_k2 = remove_markup(k2)
			clean_k1 = remove_markup(k1)
		fout.write('<L>' + lnum + '<pc>' + clean_pc + '<k1>' + clean_k1 + '<k2>' + clean_k2 + '\n')
		fout.write(lnum + '\t' + clean_pc + '\t' + clean_h1 + '\t' + clean_k2 + '\t' + clean_k1 + '\t' + grammar + '\t' + entry  + '\t' + charcount + '\n')
	fin.close()
	fout.close()
