# -*- coding: utf-8 -*-
"""Revert literary sources from '<ls></ls>' markup to '/...../' markup.
	Revert paragraph markup from <P> to '//' markup.

	Usage - python3 revert_3to2.py ../interim/reversion/lrv_3.txt ../interim/reversion/lrv_2.txt
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
	for lin in fin:
		lin = lin.replace('<P>', '//')
		if lin.startswith('<L>') or lin.startswith('<LEND>'):
			fout.write(lin)
		else:
			lin = lin.replace('<ls>', '/')
			lin = lin.replace('</ls>', '/')
			fout.write(lin)
	fin.close()
	fout.close()

