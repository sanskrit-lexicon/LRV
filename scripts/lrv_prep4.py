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
		if lin.startswith('<L>') or lin.startswith('<LEND>') or lin == '\n':
			lin = sanscript.transliterate(lin, 'devanagari', 'slp1')
			fout.write(lin)
		else:
			(key2, grammar, entry) = lin.split('\t')
			# Prepare key2
			key2 = sanscript.transliterate(key2, 'devanagari', 'slp1')
			# Prepare grammar
			# https://stackoverflow.com/questions/41356013/how-to-detect-if-a-string-contains-hindi-devnagri-in-it-with-character-and-wor
			# [\u0900-\u097F]+ matches Devanagari text
			n = re.split('([\u0900-\u097F]+)', grammar)
			gram = ''
			for j in range(len(n)):
				if j % 2 == 0:
					gram += n[j]
				else:
					gram += '<s>' + sanscript.transliterate(n[j], 'devanagari', 'slp1') + '</s>'
			gram = re.sub('</s>([ ]+)<s>', '\g<1>', gram)
			# Prepare entry
			m = re.split('([\u0900-\u097F]+)', entry)
			ent = ''
			for i in range(len(m)):
				if i % 2 == 0:
					ent += m[i]
				else:
					ent += '<s>' + sanscript.transliterate(m[i], 'devanagari', 'slp1') + '</s>'
			ent = re.sub('</s>([ ]+)<s>', '\g<1>', ent)
			# Write to file
			fout.write(key2 + '\t' + gram + '\t' + ent)


