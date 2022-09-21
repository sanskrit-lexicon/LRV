# -*- coding: utf-8 -*-
"""Convert SLP1 to Devanagari.
	Convert grammar details from {%...%} markup.
	
	Ultimately ../interim/reversion/lrv_3.txt should match with ../interim/lrv_3.txt

Usage - python3 revert_4to3.py ../interim/lrv_4.txt ../interim/reversion/lrv_3.txt
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
		if lin.startswith('<L>'):
			# <L>00005<pc>001-02<k1>afRin<k2>afRin
			# is to be converted to
			# <L>00005<pc>001-02<k1>अऋणिन्<k2>अऋणिन्
			p = re.search('<k1>(.*)<k2>(.*)', lin)
			k1 = p.group(1)
			k2 = p.group(2)
			k1_dev = sanscript.transliterate(k1, 'slp1', 'devanagari')
			k2_dev = sanscript.transliterate(k2, 'slp1', 'devanagari')
			# Hack till this issue gets resolved
			# https://github.com/indic-transliteration/indic_transliteration_py/issues/75
			k1_dev = k1_dev.replace('रृ', 'र्ऋ')
			k2_dev = k2_dev.replace('रृ', 'र्ऋ')
			lin = lin.replace('<k1>'+k1+'<k2>'+k2, '<k1>'+k1_dev+'<k2>'+k2_dev)
			fout.write(lin)
		elif  lin.startswith('<LEND>') or lin == '\n':
			fout.write(lin)
		else:
			# afRin¦ {%a. (f. {#nI#})%} Free from debt.
			# is to be converted to
			# अऋणिन्	a. (f. नी)	Free from debt.
			(k2, gram_ent) = lin.split('¦ {%')
			(gram, ent) = gram_ent.split('%} ')
			
			# Prepare key2
			k2_dev = sanscript.transliterate(k2, 'slp1', 'devanagari')
			# Prepare grammar
			gram_dev = ''
			m = re.split('{#(.*?)#}', gram)
			for i in range(len(m)):
				if i % 2 == 0:
					gram_dev += m[i]
				else:
					gram_dev += sanscript.transliterate(m[i], 'slp1', 'devanagari')
			# Prepare entry
			ent_dev = ''
			n = re.split('{#(.*?)#}', ent)
			for j in range(len(n)):
				if j % 2 == 0:
					ent_dev += n[j]
				else:
					ent_dev += sanscript.transliterate(n[j], 'slp1', 'devanagari')
			# Hack till this issue gets resolved
			# https://github.com/indic-transliteration/indic_transliteration_py/issues/75
			k2_dev = k2_dev.replace('रृ', 'र्ऋ')
			gram_dev = gram_dev.replace('रृ', 'र्ऋ')
			ent_dev = ent_dev.replace('रृ', 'र्ऋ')


			# Write to file
			fout.write(k2_dev + '\t' + gram_dev + '\t' + ent_dev)


