# -*- coding: utf-8 -*-
"""Prepare baseline data for lrv_hwextra.txt (from metalines having alternate headwords)

Usage - python3 lrv_prep_althw.py ../interim/change_metalines.json ../interim/lrv_hwextra.txt
"""
import codecs
import sys
import json
import re
import parseheadline

if __name__ == "__main__":
	filein = sys.argv[1]
	fileout = sys.argv[2]
	fin = codecs.open(filein, 'r', 'utf-8')
	fout = codecs.open(fileout, 'w', 'utf-8')
	changed_metalines = json.load(fin)
	# <L>00085<pc>002-32<k1>akUpAra<k2>akUpA(vA)ra
	# to
	# <L>00085.1<pc>002-32<k1>akUpA(vA)ra<k2>akUpA(vA)ra<type>alt<LP>00085<k1P>akUpAra
	# Keeping k1 and k2 as k2 of parent. They will be manually modified later.
	for key, value in changed_metalines.items():
		meta = parseheadline.parseheadline(value)
		# print(meta)
		lnum_parent = meta['L']
		pc_parent = meta['pc']
		k1_parent = meta['k1']
		k1_parent = re.sub('\(.*?\)', '', k1_parent)
		k2_parent = meta['k2']
		k1_alt = k2_parent
		k2_alt = k2_parent
		lnum_alt = lnum_parent + '.1'
		result = '<L>' + lnum_alt + '<pc>' + pc_parent + '<k1>' + k1_alt + '<k2>' + k2_alt + '<type>alt<LP>' + lnum_parent + '<k1P>' + k1_parent
		# print(result)
		fout.write(result + '\n')
	
		
		
		
		
		