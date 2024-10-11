#-*- coding:utf-8 -*-
"""make_lrv_1.py
"""
import sys,re,codecs
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print("%s lines read from %s" % (len(lines),filein))
 return lines

def adjust(lines):
 # remove blank lines in body
 newlines = []  # returned
 metaline = None
 iline_meta = None
 nchg = 0
 nx = 0
 nbody = 0
 xlines = []
 nmeta = 0 
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   iline_meta = iline
   nmeta = nmeta + 1
   newlines.append(line)
   line1 = lines[iline+1]
   if (not '¦' in line1) and (not '{{Lbody' in line1):
    print('Error at',metaline)
    exit(1)
   line2 = lines[iline+2]
   assert line2 == '<LEND>'
   continue
  if line.startswith('<LEND>'):
   metaline = None
   iline_meta = None
   newlines.append('<LEND>')
   continue
  if metaline == None:
   newlines.append(line)
   continue
  if iline != (iline_meta + 1):
   newlines.append(line)
   continue
  # change line after metaline
  newline = re.sub(r'^(.*?)¦',  r'{#\1#}¦', line)
  newlines.append(newline)
  if newline == line:
   if line.startswith('{{Lbody'):
    nbody = nbody + 1
   else:
    nx = nx + 1
    xlines.append((iline,line))
  else:
   nchg = nchg + 1
  continue
 print('adjust: %s lines changed' % nchg)
 print('nbody = %s' % nbody)
 print('nmeta = %s' % nmeta)
 print('nx = %s' % nx)
 write_x('temp_nx.txt',xlines)
 return newlines

def write_x(fileout,xlines):
 outarr = []
 for (iline,line) in xlines:
  out = '%s %s' %(iline,line)
  outarr.append(out)
 write(fileout,outarr)
 
def write(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line + '\n')
 print(len(lines),"written to",fileout)
 
if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # revised xxx.txt
 lines = read_lines(filein)
 newlines = adjust(lines)
 write(fileout,newlines)

 
