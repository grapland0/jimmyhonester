#!/usr/bin/python
import os,sys

class GrammerError:
	def __init__(self,err,line):
		self.msg="Grammer error '%s' in Line: '%s'.\n"%(err,line)
	def __repr__(self):
		return self.msg

def parse_rr(fn):
	while True:
		ln=fn.next()
		parts=ln.strip().split()
		if(len(parts)==0):
			continue
		ide=ln.find('@')
		if(ide<0 or len(parts)<1 or not parts[0].startswith('@')):
			raise GrammerError('Illegal marking format',ln)
#print ((ide,parts[0][1:],parts[1:],ln))
		return (ide,parts[0][1:],parts[1:],ln)

class arc_t:
	def __init__(self,dest,hit,isfake,iscycle):
		self.dest=dest
		self.hit=long(hit)
		self.fake=isfake
		self.cycle=iscycle
	def parse(self,fi,tide):
		while True:
			(ide,var,conts,ln)=parse_rr(fi)
			if(ide==tide and var=='.arc'):
				break
			if(ide!=tide+1):
				raise GrammerError('Illegal indent',ln)
			if(var=='dest'):
				self.dest=conts[0]
			elif(var=='hit'):
				self.hit=long(conts[0])
			elif(var=='cycle'):
			 	self.cycle=bool(int(conts[0]))
			elif(var=='fake'):
				self.fake=bool(int(conts[0])==1)
			else:
				raise GrammerError('Illegal mark:'+var,ln)
	def __repr__(self):
		return "ARC_TO: %s, FAKE:%d, HIT:%d\n"%(self.dest,1 if self.fake else 0,self.hit)

class block_t:
	def __init__(self,bid,lines,arcs):
		self.bid=bid
		self.lines=lines
		self.arcs=arcs
	def parse(self,fi,tide):
		while True:
			(ide,var,conts,ln)=parse_rr(fi)
			if(ide==tide and var=='.block'):
				break
			if(ide!=tide+1):
				raise GrammerError('Illegal indent',ln)
			if(var=='lines'):
				self.lines=map(lambda x:int(x),conts)
			elif(var=='arc'):
				arc=arc_t('',0,False,False)
				arc.parse(fi,ide)
				self.arcs.append(arc)
			else:
				raise GrammerError('Illegal mark:'+var,ln)
	def __repr__(self):
		return "BLOCK: %s, ARC_CNT: %d\n"%(self.bid,len(self.arcs))
	
class func_t:
	def __init__(self,name,src,blocks):
		self.name=name
		self.src=src
		self.blocks=blocks
	def parse(self,fi,tide):
		while True:
			(ide,var,conts,ln)=parse_rr(fi)
			if(ide==tide and var=='.func'):
				break
			if(ide!=tide+1):
				raise GrammerError('Illegal indent',ln)
			if(var=='src'):
				self.src=conts[0]
			elif(var=='block'):
				blk=block_t(conts[0],[],[])
				blk.parse(fi,ide)
				self.blocks[blk.bid]=blk
			else:
				raise GrammerError('Illegal mark:'+var,ln)
	def __repr__(self):
		return "FUNC: %s, BLOCK_CNT: %d\n"%(self.name,len(self.blocks))

class rr_t:
	def __init__(self,rid,funcs):
		self.rid=rid
		self.funcs=funcs
	def parse(self,fi,tide):
		while True:
			(ide,var,conts,ln)=parse_rr(fi)
			if(ide==tide and var=='.rr'):
				break
			if(ide!=tide+1):
				raise GrammerError('Illegal indent',ln)
			elif(var=='func'):
				func=func_t(conts[0],'',{})
				func.parse(fi,ide)
				self.funcs[func.name]=func
			else:
				raise GrammerError('Illegal mark:'+var,ln)
	def __repr__(self):
		return "RR: %s, FUNC_CNT: %d\n"%(self.rid,len(self.funcs))

class rrreader:
	def __init__(self,fname):
		self.f=open(fname,'r')
		self.fi=self.f.__iter__();
	def __del__(self):
		self.f.close()
	def __iter__(self):
		return self
	def next(self):
		(ide,var,[cont],ln)=parse_rr(self.fi)
		if(ide!=0):
			raise GrammerError('Illegal indent',ln)
		if(var=='rr'):
			rr=rr_t(cont,{})
			rr.parse(self.fi,ide)
			return rr
		else:
			raise GrammerError('Illegal mark:'+var,ln)

