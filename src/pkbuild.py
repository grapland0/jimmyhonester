#!/usr/bin/python
import os,sys,sqlite3

"""this app recevice a sql bulk export from your OJ and a data file,
	output a sqlite db which contain these info.
	the sql bulk info must be all this:
	insert into codes (cid,code,lid) values (zzzzzz)
"""

#when use multi_line,this func return a sql stmt when given a file reader iter.
def getnxtsql(ifi):
	a=ifi.next().strip()
	return a+ifi.next().strip()

def main(fsql,fdata,opt):
	db=sqlite3.connect(opt)
	c=db.cursor()
	try:
		c.execute("drop table codes")
		c.execute("drop table data")
	except sqlite3.OperationalError,x:pass
	c.execute("create table codes(cid  int,lid  int,code text)")
	c.execute("create table data(data  BLOB)")
	db.commit()
	fs=open(fsql,'r')
	ifs=fs.__iter__()
	try:
		while True:
			stmt=getnxtsql(ifs)
			c.execute(stmt)
	except StopIteration:pass
	db.commit()
	fs.close()
	fd=open(fdata,'rb')
	c.execute("insert into data values (?)",(sqlite3.Binary(fd.read()),))
	fd.close()
	db.commit()
	db.close()

if __name__=="__main__":
	if(len(sys.argv)==4):
		main(sys.argv[1],sys.argv[2],sys.argv[3])
	else:
		print("Usage: %s <sql input> <data input> <opt>"%sys.argv[0])
	
