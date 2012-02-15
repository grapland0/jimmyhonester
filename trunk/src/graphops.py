#!/usr/bin/python

from basictype import *

def update_entry(func):
	dk=set(func.blocks.keys())
	for ib in func.blocks.itervalues():
		for ia in ib.arcs:
			if(ia.dest in dk):
				dk.remove(ia.dest)
	if(len(dk)!=1):
		raise Exception("The func %s has no block or not only one entry."%func.name)
	func.entry_bid=list(dk)[0]

def erase_ntv(func):
	'''this routine will remove all arcs which transed less than 1 time or marked fail in gcov_mod.'''
	for ib in func.blocks.itervalues():
		ib.arcs=filter(lambda x:not(x.hit==0 or x.fake),ib.arcs)

def calc_in_out(func):
	for ib in func.blocks.itervalues():
		ib.cnt_out=len(ib.arcs)
		ib.cnt_in=0
	for ib in func.blocks.itervalues():
		for ia in ib.arcs:
			func.blocks[ia.dest].cnt_in+=1

def combine_1in1out_block(func):
	markasdel=set()
	for ib in func.blocks.itervalues():
		if(ib.cnt_out!=1 or ib.cnt_out!=1 or ib.bid in markasdel):
			continue
		tmp_bk=ib
		tmp_target=func.blocks[ib.arcs[0].dest]
		while tmp_target.cnt_out==1 and tmp_target.cnt_in==1:
			if(tmp_bk.arcs[0].hit!=tmp_target.arcs[0].hit):raise Exception()
		 	tmp_bk=tmp_target
		 	tmp_target=func.blocks[tmp_bk.arcs[0].dest]
			markasdel.add(tmp_bk.bid)
		ib.arcs[0].dest=tmp_target.bid
	for it in markasdel:
		del func.blocks[it]

def calc_branch_p(func):
	for ib in func.blocks.itervalues():
		ttl=float(reduce(lambda x,y:x+float(y.hit),ib.arcs,0.0))
		if(ttl<0.5):
			ib.probs=[]
			continue
		ib.probs=filter(lambda x:x>1e-6 and x<1-1e-6,\
				map(lambda y:float(y.hit/ttl),ib.arcs))

def check_DAG_dfs(bid_unused,bid_dc,entry_bid,blks):
	if(entry_bid not in bid_unused):
		return
	bid_unused.remove(entry_bid)
	bid_dc.add(entry_bid)
	for ia in blks[entry_bid].arcs:
		if(ia.dest not in bid_dc):
			check_DAG_dfs(bid_unused,bid_dc,ia.dest,blks)
		else:
			ia.cycle=True
	bid_dc.remove(entry_bid)

def check_DAG(func):
	'''this routine will remove all arcs or blocks that has not connected to entry block, and remove cycle edge, but it remains probs which has been claced in calc_branch_p'''
	bid_unused=set(func.blocks.keys())
	bid_dc=set()
	check_DAG_dfs(bid_unused,bid_dc,func.entry_bid,func.blocks)
	for it in bid_unused:
		del func.blocks[it]
	for ib in func.blocks.itervalues():
		ib.arcs=filter(lambda x:x.dest not in bid_unused and not x.cycle,ib.arcs)

