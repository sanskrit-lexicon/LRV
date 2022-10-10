# -*- coding: utf-8 -*-
"""Club the key1 of alternate headwords back together.
	
	Ultimately ../interim/reversion/lrv_4.txt should match with ../interim/lrv_4.txt

Usage - python3 revert_5to4.py ../interim/lrv_5.txt ../interim/reversion/lrv_4.txt
"""
import sys
import codecs
import json
import parseheadline


if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	jsonfile = 	'../interim/change_metalines.json'
	jsonfin = codecs.open(jsonfile, 'r', 'utf-8')
	changed_lines = json.load(jsonfin)
	for lin in fin:
		lin = lin.rstrip('\n')
		if lin.startswith('<L>'):
			meta = parseheadline.parseheadline(lin)
			metaline = lin
			lnum = meta['L']
			if lnum in changed_lines:
				metaline = changed_lines[lnum]
			fout.write(metaline + '\n')
		else:
			fout.write(lin + '\n')
	
			
			
			
			
			
	