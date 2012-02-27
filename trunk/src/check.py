#!/usr/bin/python

import os,sys,math
from basictype import *
from graphops import *
from flowmetric_advanced import *

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
	cnt=0
	for it in rd:
		print "%d"%cnt,
		cnt+=1
		for itf in it.funcs.itervalues():
			update_entry(itf)
			erase_ntv(itf)
			calc_in_out(itf)
			combine_1in1out_block(itf)
			calc_branch_p(itf)
			check_DAG(itf)
		if (it.rid in mtd):
			raise Exception("Two code share one CID: %s."%it.rid)
		mtd[it.rid]=calcmetric(it)
	print "\nMatching."
	kys=mtd.keys()
	serf={}
	allmtvs=[]
	print "Calc self similarity."
	for ki in kys:
		serf[ki]=calcmatch(mtd[ki],mtd[ki])
	print "Calc mutual similarity."
	cntn=0.0
	for ki in kys:
		cntn+=1.0
		mtvs=[]
		for kj in kys:
			if(ki==kj):
				continue
			res=calcmatch(mtd[ki],mtd[kj])
			mtvs.append((kj,res,))
			allmtvs.append((ki,kj,math.fabs(res/serf[ki]-1.0)))
		mtvs.sort(key=lambda x:math.fabs(x[1]-serf[ki]))
		print("[%.1f%%] Top 10 similar with Code %s (MTV:%.4lf)"%(cntn*100.0/float(cnt),ki,serf[ki]))
		for j in xrange(0,min(10,len(mtvs))):
			print "\t%s: %.4lf"%(mtvs[j][0],mtvs[j][1])
	allmtvs.sort(key=lambda x:x[2])
	print "\nIn all code,Top 100 similar pairs are:"
	for i in xrange(0,min(100,len(allmtvs))):
		print "%s with %s, diff:%.5lf"%(allmtvs[i][0],allmtvs[i][1],allmtvs[i][2])


if __name__=='__main__':
	if(len(sys.argv)==2):
		main(sys.argv[1])
	else:
		print("Usage: %s <rr set>\n"%sys.argv[0])

