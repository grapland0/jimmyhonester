#!/usr/bin/python

import os,sys
from basictype import *

def main(fname):
	rd=rrreader(fname)
	for it in rd:
		print(it,)
		for itf in it.funcs.itervalues():
			print "\t"+str(itf),
			for itb in itf.blocks.itervalues():
				print "\t\t"+str(itb),
				for ita in itb.arcs:
					print "\t\t\t"+str(ita),

if __name__=='__main__':
	if(len(sys.argv)==2):
		main(sys.argv[1])
	else:
		print("Usage: %s <rr set>\n"%sys.argv[0])

