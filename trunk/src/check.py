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
	kys=mtd.keys()
	serf={}
	for ki in kys:
		serf[ki]=calcmatch(mtd[ki],mtd[ki])
	for ki in kys:
		for kj in kys:
			if(ki==kj):
				continue
			res=calcmatch(mtd[ki],mtd[kj])
			if(res>0.97*serf[ki] and res<1.03*serf[ki]):
				print("%s copies %s,matval: %.4lf[%s self] %.4lf[%s with %s]."%(ki,kj,serf[ki],ki,res,ki,kj))

if __name__=='__main__':
	if(len(sys.argv)==2):
		main(sys.argv[1])
	else:
		print("Usage: %s <rr set>\n"%sys.argv[0])

