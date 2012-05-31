#!/usr/bin/python

import os,sys,math
from basictype import *
from graphops import *
from flowmetric_naive import *

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
	pids={}
	uids={}
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
		mtv=calcmetric(it)
		if(len(mtv)==0):
			print "\nCannot determine the MTV of code: %s."%it.rid
		else:
			mtd[it.rid]=mtv
			if(it.pid not in pids):
				pids[it.pid]=[]
			pids[it.pid].append(it.rid)
			uids[it.rid]=it.uid



	print "\nMatching."
	#stat total work load
	cnt=0.0
	cntn=0.0
	for it in pids.itervalues():
		n=float(len(it))
		cnt+=n*(n-1.0)/2.0
	#iter problems
	for pid,kys in pids.iteritems():
		print("Working on problem %d."%pid)
		serf={}
		allmtvs=[]
		print "\tCalc self similarity."
		for ki in kys:
			serf[ki]=calcmatch(mtd[ki],mtd[ki])
		print "\tCalc mutual similarity."
		ress=[[9.9 for x in xrange(len(kys))] for y in xrange(len(kys))]

		#calc similarity matrix
		for i in xrange(len(kys)):
			cntn+=1
			print "%.1lf%%"%(100.0*cntn/cnt),
			sys.stdout.flush()
			for j in xrange(i):
				cntn+=1.0
				ki,kj=(kys[i],kys[j])
				if(uids[ki]==uids[kj]):
					continue
				ress[i][j]=ress[j][i]=calcmatch(mtd[ki],mtd[kj])

		#display results
		for i in xrange(len(kys)):
			mtvs=[]
			for j in xrange(len(kys)):
				ki,kj=(kys[i],kys[j])
				if(uids[ki]==uids[kj]):
					continue
				res=ress[i][j]
				mtvs.append((kj,res,math.fabs(res/serf[ki]-1.0)))
				if(i<j):allmtvs.append((ki,kj,math.fabs(res/serf[ki]-1.0)))
			mtvs.sort(key=lambda x:math.fabs(x[1]-serf[ki]))
			print("\tTop 10 similar with Code %s (MTV:%.4lf)"%(ki,serf[ki]))
			for j in xrange(0,min(10,len(mtvs))):
				print "\t\t%s: %.4lf(%.5lf)"%(mtvs[j][0],mtvs[j][1],mtvs[j][2])
		allmtvs.sort(key=lambda x:x[2])
		print "\n\tIn all code,Top 100 similar pairs are:"
		for i in xrange(0,min(100,len(allmtvs))):
			print "\t\t%s with %s, diff:%.5lf"%(allmtvs[i][0],allmtvs[i][1],allmtvs[i][2])


if __name__=='__main__':
	if(len(sys.argv)==2):
		main(sys.argv[1])
	else:
		print("Usage: %s <rr set>\n"%sys.argv[0])

