# -*- coding: utf-8 -*-
"""Find duplicate lnums, if any.

Usage - python3 duplicate_lnum.py
"""
import codecs
import re


if __name__ == "__main__":
	fin = codecs.open('../interim/lrv_4.txt', 'r', 'utf-8')
	result = set()
	for lin in fin:
		if lin.startswith('<L>'):
			m = re.search('<L>(.*?)<pc>', lin)
			lnum = m.group(1)
			if lnum in result:
				print(lnum)
			result.add(lnum)
		