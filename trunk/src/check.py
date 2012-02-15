#!/usr/bin/python

import os,sys
from basictype import *
from graphops import *
from flowmetric import *

def print_rr(it):
	print(it,)
	for itf in it.funcs.itervalues():
		print "\t"+str(itf),
		for itb in itf.blocks.itervalues():
			print "\t\t"+str(itb),
			if('probs' in itb.__dict__):print "\t\t"+str(itb.probs)
			for ita in itb.arcs:
				print "\t\t\t"+str(ita),

def main(fname):
	rd=rrreader(fname)
	print "Reading running records",
	mtd={}
	for it in rd:
		print ".",
		for itf in it.funcs.itervalues():
			update_entry(itf)
			erase_ntv(itf)
			calc_in_out(itf)
			combine_1in1out_block(itf)
			calc_branch_p(itf)
			check_DAG(itf)
		mtd[it.rid]=calcmetric(it)
	print "\nMatching."
	for ka,va in mtd.iteritems():
		print "RR %s: "%ka,
		for kb,vb in mtd.iteritems():
			print "%s=%.4f "%(kb,calcmatch(va,vb)),
		print ""

if __name__=='__main__':
	if(len(sys.argv)==2):
		main(sys.argv[1])
	else:
		print("Usage: %s <rr set>\n"%sys.argv[0])

