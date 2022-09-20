# -*- coding: utf-8 -*-
"""Extract L-id, page-column, key1, key2

	e.g. <L>00017<pc>001-09<k1>अंशु<k2>अंशु

Usage - python3 lrv_prep1.py ../interim/lrv_0.txt ../interim/lrv_1.txt
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
	for lin in fin:
		fout.write(lin)
	fin.close()
	fout.close()
