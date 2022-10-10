# -*- coding: utf-8 -*-
"""Find duplicate page-sequence numbers, if any.

Usage - python3 qc_duplicate_pc.py
"""

import codecs
import csv

if __name__ == "__main__":
	fin = codecs.open('../interim/lrv_0.txt', 'r', 'utf-8')
	reader = csv.reader(fin, delimiter='\t')
	result = set()
	for row in reader:
		pc = row[1]
		if pc != '':
			if pc in result:
				print(pc)
				print('\t'.join(row))
			result.add(pc)
		