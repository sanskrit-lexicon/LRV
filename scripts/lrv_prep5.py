# -*- coding: utf-8 -*-
"""Convert key1 with brackets to without brackets.

Usage - python3 lrv_prep5.py ../interim/lrv_4.txt ../interim/lrv_5.txt
"""
import sys
import re
import codecs
import json
import parseheadline

def prepare_metaline(meta):
	result = ''
	for key, value in meta.items():
		result += '<' + key + '>' + value
	return result

if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	changefile = '../interim/change_metalines.json'
	cfout = codecs.open(changefile, 'w', 'utf-8')
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	changed_entries = {}
	for lin in fin:
		lin = lin.rstrip('\n')
		if lin.startswith('<L>'):
			meta = parseheadline.parseheadline(lin)
			if '(' in meta['k1']:
				lnum = meta['L']
				meta['k1'] = re.sub('\(.*?\)', '', meta['k1'])
				metaline = prepare_metaline(meta)
				fout.write(metaline + '\n')
				changed_entries[lnum] = lin
			else:
				fout.write(lin + '\n')
		else:
			fout.write(lin + '\n')
	json.dump(changed_entries, cfout, indent='\t')
	