# -*- coding: utf-8 -*-
"""Convert Devanagari to SLP1 with <s></s> markup

Usage - python3 lrv_prep4.py ../interim/lrv_3.txt ../interim/lrv_4.txt
"""
import sys
import re
import codecs
from indic_transliteration import sanscript


if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	ls_list = []
	for lin in fin:
		# https://stackoverflow.com/questions/41356013/how-to-detect-if-a-string-contains-hindi-devnagri-in-it-with-character-and-wor
		# [\u0900-\u097F]+ matches Devanagari text
		if lin.startswith('<L>') or lin.startswith('<LEND>') or lin == '\n':
			lin = sanscript.transliterate(lin, 'devanagari', 'slp1')
			fout.write(lin)
		else:
			(key2, grammar, entry) = lin.split('\t')
			key2 = sanscript.transliterate(key2, 'devanagari', 'slp1')
			m = re.split('([\u0900-\u097F]+)', entry)
			ent = ''
			for i in range(len(m)):
				if i % 2 == 0:
					ent += m[i]
				else:
					ent += '<s>' + sanscript.transliterate(m[i], 'devanagari', 'slp1') + '</s>'
			fout.write(key2 + '\t' + grammar + '\t' + ent)


