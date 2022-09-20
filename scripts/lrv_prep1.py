# -*- coding: utf-8 -*-
"""Change line ending to \n instead of \r\n

Usage - python3 lrv_prep1.py ../interim/lrv_0.txt ../interim/lrv_1.txt
"""
import sys
import re
import codecs


if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	for lin in fin:
		lin = lin.rstrip()
		fout.write(lin + '\n')
	fin.close()
	fout.close()
