# -*- coding: utf-8 -*-
"""Find out alternate headwords from grammatical information.

Usage - python3 issue20.py ../interim/lrv_5.txt ../logs/issue20/neuter_alt_words.txt
"""
import sys
import re
import codecs
import json
import parseheadline

if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	problematic_entries = []
	for lin in fin:
		lin = lin.rstrip('\n')
		if lin.startswith('<L>'):
			meta = parseheadline.parseheadline(lin)
			k1 = meta['k1']
			lnum = meta['L']
			pc = meta['pc']
		elif '{%' in lin:
			# Neuter endings
			m = re.search('{%.*n[.][ ]*{#(.*?)#}.*%}', lin)
			if m:
				fem_end = m.group(1)
				new_k1 = k1[:-len(fem_end)] + fem_end
				result = '<L>' + lnum + '.1<pc>' + pc + '<k1>' + new_k1 + '<k2>' + k1 + '(' + fem_end + ')' +  '<type>neu<LP>' + lnum + '<k1P>' + k1
				fout.write(result + '\n')
	

