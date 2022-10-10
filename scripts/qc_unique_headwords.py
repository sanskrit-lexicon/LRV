# -*- coding: utf-8 -*-
"""Find headwords which are absent in sanhw1, if any.

Usage - python3 qc_unique_headwords.py
"""
import codecs
import re
from indic_transliteration import sanscript

def read_sanhw1():
	result = set()
	with codecs.open('../../../cologne/hwnorm1/sanhw1/sanhw1.txt', 'r', 'utf-8') as fin:
		for lin in fin:
			hw = lin.split(':')[0]
			result.add(hw)
	return result

def varga_panchama(word):
	word = re.sub('M([kKgGN])', 'N\g<1>', word)
	word = re.sub('M([cCjJY])', 'Y\g<1>', word)
	word = re.sub('M([wWqQR])', 'R\g<1>', word)
	word = re.sub('M([tTdDn])', 'n\g<1>', word)
	word = re.sub('M([pPbBm])', 'm\g<1>', word)
	return word


def remove_bracket(word):
	word = re.sub('\(.*?\)', '', word)
	return word

if __name__ == "__main__":
	sanhw1_set = read_sanhw1()
	ok_counter = 0
	panchama_counter = 0
	bracket_counter = 0
	bad_counter = 0
	fout = codecs.open('../logs/issue11/unique_headwords.txt', 'w', 'utf-8')
	with codecs.open('../interim/lrv_4.txt', 'r', 'utf-8') as fin:
		for lin in fin:
			if lin.startswith('<L>'):
				m = re.search('<pc>(.*?)<k1>(.*?)<k2>', lin)
				pc = m.group(1)
				k1 = m.group(2)
				pan = varga_panchama(k1)
				brac = remove_bracket(pan)
				if k1 in sanhw1_set:
					ok_counter += 1
				elif pan in sanhw1_set:
					panchama_counter += 1
				elif brac in sanhw1_set:
					bracket_counter += 1
				else:
					bad_counter += 1
					#print(bad_counter, k1)
					k1_deva = sanscript.transliterate(k1, 'slp1', 'devanagari')
					fout.write(k1_deva + '\t' + pc + '\n')

	print('Direct Match:\t' + str(ok_counter))
	print('Varga Panchama Match:\t' + str(panchama_counter))
	print('Bracket Removal Match:\t' + str(bracket_counter))
	print('No Match:\t' + str(bad_counter))
	fout.close()

	

