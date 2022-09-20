# -*- coding: utf-8 -*-
"""Extract literary sources and mark with <ls></ls> markup

Usage - python3 lrv_prep3.py ../interim/lrv_2.txt ../interim/lrv_3.txt
"""
import sys
import re
import codecs
from collections import Counter

if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	ls_list = []
	for lin in fin:
		if lin.startswith('<L>') or lin.startswith('<LEND>'):
			fout.write(lin)
		else:
			m = re.search('\/([^/ ]+)\/', lin)
			if m:
				print(m.group(1))
				ls_list.append(m.group(1))
				#lin = re.sub('\/([^/ ]+)\/', '<ls>\g<1></ls>', lin)
			fout.write(lin)
	cnt = Counter(ls_list)
	print(cnt.most_common())
				
