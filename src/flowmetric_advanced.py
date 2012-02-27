#!/usr/bin/python

import os,sys,math
from basictype import *

class vinf_t:
	def __init__(self,bid,metval,bidfw):
		self.bid=bid
		self.metval=metval
		self.bidfw=bidfw	#a set, within forward vertexs.
	def __repr__(self):
		return "BID: %s, MTV: %.4f, FW:%s"%(self.bid,self.metval,str(self.bidfw))

#TO MANY ASS FUCKING in this code, so if you find some formulas hard to understand, ignore them for the time being, then lookup my paper for details.
mseg=(0.1,0.3,0.7,0.9)
def calcmtv(pbs):
	return reduce(lambda x,y:x+min(map(lambda x:math.fabs(y-x),mseg)),filter(lambda x:x>0.05 and x<0.95,map(lambda x:x[1],pbs)),0.0)

#toposort the DAG.
def toposort(entry_bid,blks):
	outs=[]
	hits={entry_bid:(0,[])}
	for it in blks.itervalues():
		for ia in it.arcs:
			if(ia.dest not in hits):
				hits[ia.dest]=[1,[it.bid]]
			else:
			 	hits[ia.dest][0]+=1
			 	hits[ia.dest][1].append(it.bid)
	for bid,hit in hits.iteritems():
		if(hit[0]==0 and bid!=entry_bid):
			raise Exception("DAG has multiple entries.")
	zs=[entry_bid]
	while len(zs)!=0:
		cur=zs.pop()
		outs.append((cur,hits[cur][1]))
		for it in blks[cur].arcs:
			hits[it.dest][0]-=1
			if(hits[it.dest][0]==0):
				zs.append(it.dest)
	return outs

#This routine returns a 2-D arraylist include MTV and meanful forward blocks' MTV of every branched block.
def calcmetric(rr):
	dd={}
	for itf in rr.funcs.itervalues():
		if(itf.name.startswith('/')):#ignore code we dont care, mainly from /usr/include etc.
			continue
		#process vertex by their topo order.
		vproc=toposort(itf.entry_bid,itf.blocks)
		dd[itf.entry_bid]=vinf_t(itf.entry_bid,calcmtv(itf.blocks[itf.entry_bid].probs),set([itf.entry_bid]))
		for it in vproc:
			blk=itf.blocks[it[0]]
			for bid,p in blk.probs:
				if(bid not in dd):
					dd[bid]=vinf_t(bid,calcmtv(itf.blocks[bid].probs),set())
				if(p>0.95):
					dd[bid].bidfw.update(dd[blk.bid].bidfw)
				else:
					dd[bid].bidfw.add(blk.bid)
	return sorted([(x.metval,sorted(map(lambda y:dd[y].metval,x.bidfw)))for x in dd.itervalues() if x.metval>1e-6])

def diffv(a,b):
#	print str(10.0/(0.1+math.fabs(a-b)/max((a,b,1-a,1-b)))),
	return 10.0/(0.1+math.fabs(a-b))

def maxfitting(la,lb,wgtfunc):
	a=len(la)
	b=len(lb)
	m=[[0.0 for y in xrange(0,b+1)] for x in xrange(0,a+1)]
	for i in xrange(1,a+1):
		for j in xrange(1,b+1):
			m[i][j]=max(m[i-1][j-1]+wgtfunc(la[i-1],lb[j-1]),\
					m[i-1][j] if j<b else 0.0,\
					m[i][j-1] if i<a else 0.0)
	return m[a][b]

def calcmatch(lla,llb):
#print lla,llb
	return maxfitting(lla,llb,lambda ai,aj:diffv(ai[0],aj[0])*3+maxfitting(ai[1],aj[1],diffv))

