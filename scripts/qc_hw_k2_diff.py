# -*- coding: utf-8 -*-
"""Find headword and k2 differences.

Usage - python3 qc_hw_k2_diff.py
"""
import codecs
import re
from indic_transliteration import sanscript

if __name__ == "__main__":
	with codecs.open('../interim/lrv_0.txt', 'r', 'utf-8') as fin:
		counter = 1
		for lin in fin:
			lin = lin.rstrip()
			splt = lin.split('\t')
			lnum = splt[0]
			pc = splt[1]
			hw = splt[2]
			k1 = splt[3]
			k2 = splt[4]
			if hw.startswith('<p>'):
				if hw != k1 or hw != k2 or k1 != k2:
					print(counter, lnum, pc, hw, k1, k2)
					counter += 1
			
	
