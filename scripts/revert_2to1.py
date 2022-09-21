# -*- coding: utf-8 -*-
"""Extract L-id, page-column, key1, key2 and put in metaline
	Extract key2, lexinfo and entry and put in the next line
	
	e.g. 
	<L>00017<pc>001-09<k1>अंशु<k2>अंशु
	अंशु	m.	1. A ray of light, सूर्योंशुभिर्मित्रमिवारविन्दम् /K.S./i.32; 2. light, refulgence, अंगुष्ठनखांशुभिन्नया /Sis./i.9; 3. dress; 4. a minute particle, an atom.
	<LEND>

	Also separate out the entries with multiple headword information in them.
	e.g. aMSa-hara, aMSa-hArin

Usage - python3 revert_2to1.py ../interim/reversion/lrv_2.txt ../interim/reversion/lrv_1.txt
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
	counter = 0
	for lin in fin:
		if counter == 500:
			exit(0)
		if lin.startswith('<L>'):
			# <L>00017<pc>001-09<k1>अंशु<k2>अंशु
			m = re.search('<L>([^<]*)<pc>([^<]*)<k1>([^<]*)<k2>([^<]*)\n', lin)
			lnum = m.group(1)
			pc = m.group(2)
			k1 = m.group(3)
			k2 = m.group(4)
			if '-' in k2:
				# अंश-अंशि -> -अंशि
				k2secondpart = k2.replace(k1 + '-', '-')
				tabclass = ('<b> ', '<b> ', '<+> ')
			else:
				k2secondpart = k2
				tabclass = ('<p> ', '<p> ', '<p> ')
		elif lin == '\n':
			pass
		elif lin.startswith('<LEND>'):
			# 00005	001-02	<p> अऋणिन्	<p> अऋणिन्	<p> अऋणिन्	#-a. (f. नी)	$--Free from debt.	18
			# lnum	pc	k2secondpart	k2	k1	gram	entry	enlen
			fout.write(lnum + '\t' + pc + '\t' + tabclass[0] + k2secondpart + '\t' + tabclass[1] + k2 + '\t' + tabclass[2] + k1 + '\t#-' + gram + '\t$--' + entry + '\t' + enlen + '\n')             
		else:
			(k2, gram, entry) = lin.split('\t')
			entry = entry.rstrip()
			enlen = str(len(entry) + 3)
		counter += 1
