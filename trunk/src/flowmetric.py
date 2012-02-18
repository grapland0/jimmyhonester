#!/usr/bin/python

import os,sys,math
from basictype import *

#TO MANY mass fucking in this code, so if you find some formulas hard to understand, ignore them please.
mseg=(0.1,0.3,0.7,0.9)
def calcmtv(pbs):
	return reduce(lambda x,y:x+min(map(lambda x:math.fabs(y-x),mseg)),filter(lambda x:x>0.05 and x<0.95,pbs),0.0)

def calcmetric(rr):
	ret=[]
	for itf in rr.funcs.itervalues():
		if(itf.name.startswith('/')):
			continue
		for ib in itf.blocks.itervalues():
			if(len(ib.probs)<2):
				continue
			ret.append(calcmtv(ib.probs))
	return sorted(filter(lambda x:x>0.001,ret))

def diffv(a,b):
#	print str(10.0/(0.1+math.fabs(a-b)/max((a,b,1-a,1-b)))),
	return 10.0/(0.1+math.fabs(a-b))

def calcmatch(la,lb):
	a=len(la)
	b=len(lb)
#print la
#	print lb
	m=[[0.0 for y in xrange(0,b+1)] for x in xrange(0,a+1)]
	dc=[[[0,0] for y in xrange(0,b+1)] for x in xrange(0,a+1)]
	for i in xrange(1,a+1):
		for j in xrange(1,b+1):
			xxx=[(m[i-1][j-1]+diffv(la[i-1],lb[j-1]),i-1,j-1),\
					((m[i-1][j] if j<b else 0.0),i-1,j),\
					((m[i][j-1] if i<a else 0.0),i,j-1)]

			xxx.sort(key=lambda x:x[0])
#	print xxx
			m[i][j]=xxx[2][0]
			dc[i][j]=xxx[2][1:]
			
			"""
			m[i][j]=max(\
					m[i-1][j-1]+diffv(la[i-1],lb[j-1]),\
					m[i-1][j]+diffv(la[i-1],lb[j]) if j<b else 0.0,\
					m[i][j-1]+diffv(la[i],lb[j-1]) if i<a else 0.0\
					)
			"""
#print m
	ai=a
	bi=b
#	print la
#	print lb
	while dc[ai][bi][0]!=0 or dc[ai][bi][1]!=0:
#print dc[ai][bi]
		(ai,bi)=dc[ai+0][bi+0]
	return m[a][b]

