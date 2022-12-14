# -*- coding: utf-8 -*-
"""Find out alternate headwords from grammatical information.

Usage - python3 issue19.py ../interim/lrv_5.txt ../logs/issue19/grammatical_althw.txt
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
			# Feminine endings
			m = re.search('{%.*f[.][ ]*{#(.*?)#}.*%}', lin)
			if m:
				fem_end = m.group(1)
				if k1.endswith('a'):
					new_k1 = k1[:-len(fem_end)] + fem_end
					# <L>00005.1<pc>001-02<k1>afRinI<k2>afRin(nI)<type>fem<LP>00005<k1P>afRin
					result = '<L>' + lnum + '.1<pc>' + pc + '<k1>' + new_k1 + '<k2>' + k1 + '(' + fem_end + ')' +  '<type>fem<LP>' + lnum + '<k1P>' + k1
					fout.write(result + '\n')
				elif k1.endswith('in'):
					new_k1 = k1[:-1] + fem_end
					result = '<L>' + lnum + '.1<pc>' + pc + '<k1>' + new_k1 + '<k2>' + k1 + '(' + fem_end + ')' +  '<type>fem<LP>' + lnum + '<k1P>' + k1
					fout.write(result + '\n')
				elif fem_end.endswith('I') and len(fem_end) < 4:
					new_k1 = k1[:-len(fem_end)+1] + fem_end
					result = '<L>' + lnum + '.1<pc>' + pc + '<k1>' + new_k1 + '<k2>' + k1 + '(' + fem_end + ')' +  '<type>fem<LP>' + lnum + '<k1P>' + k1
					fout.write(result + '\n')
				else:
					# Store to append at the last, to allow easy analysis
					result = '<L>' + lnum + '.1<pc>' + pc + '<k1>' + k1 + '(' + fem_end + ')' + '<k2>' + k1 + '(' + fem_end + ')' +  '<type>fem<LP>' + lnum + '<k1P>' + k1
					problematic_entries.append(result)
	# Write problematic entries at the end
	for entry in problematic_entries:
		fout.write(entry + '\n')
	
