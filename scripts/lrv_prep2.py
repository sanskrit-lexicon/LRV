# -*- coding: utf-8 -*-
"""Extract L-id, page-column, key1, key2 and put in metaline
	Extract key2, lexinfo and entry and put in the next line
	
	e.g. 
	<L>00017<pc>001-09<k1>अंशु<k2>अंशु
	अंशु	m.	1. A ray of light, सूर्योंशुभिर्मित्रमिवारविन्दम् /K.S./i.32; 2. light, refulgence, अंगुष्ठनखांशुभिन्नया /Sis./i.9; 3. dress; 4. a minute particle, an atom.
	<LEND>

	Also separate out the entries with multiple headword information in them.
	e.g. aMSa-hara, aMSa-hArin

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
	hw = re.sub('^\#\-[ ]*', '', hw)
	hw = re.sub('^\$[\-]*', '', hw)
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
		clean_grammar = remove_markup(grammar)
		clean_entry = remove_markup(entry)
		if ',' in clean_k2:
			cnt = 0
			split2 = clean_k2.split(', ')
			split1 = clean_k1.split(', ')
			for i in range(len(split2)):
				if ' ' in split2[i]:
					mp = re.search('^([^ ]*?)[ ]+(.*)$', split2[i])
					clean_k2 = mp.group(1)
					clean_grammar = mp.group(2)

					# print(mp.groups())
					np = re.search('^(.*?)[ ]+([^ ]*)$', split1[i])
					# print(np.groups())
					clean_k1 = np.group(1)
				else:
					clean_k2 = split2[i]
					clean_k1 = split1[i]
				if cnt > 0:
					clean_lnum = lnum + '.' + str(cnt)
				else:
					clean_lnum = lnum
				fout.write('<L>' + clean_lnum + '<pc>' + clean_pc + '<k1>' + clean_k1 + '<k2>' + clean_k2 + '\n')
				fout.write(clean_k2 + '\t' + clean_grammar + '\t' + clean_entry  + '\n')
				fout.write('<LEND>\n\n')
				cnt += 1
		else:
			fout.write('<L>' + lnum + '<pc>' + clean_pc + '<k1>' + clean_k1 + '<k2>' + clean_k2 + '\n')
			fout.write(clean_k2 + '\t' + clean_grammar + '\t' + clean_entry  + '\n')
			fout.write('<LEND>\n\n')
	fin.close()
	fout.close()
