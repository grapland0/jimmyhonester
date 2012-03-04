#!/usr/bin/python
import os,sys,sqlite3

"""
	this app recevice a sql bulk export from your OJ and svevral data files.
	output a sqlite db which contain these info.
	Usage: prog <sql input filename> <data 1 pid> <data 1 filename> ... <data n pid> <data n filename> <output sqlite db>

	the sql bulk info must be all this:
	"insert into codes (cid,code,lid,pid,uid) values (zzzzzz)"
	cid:	code id,in INT, this id will be used to identify the code in output.
	code:	source code,in TEXT,quoted by SQL standard.
	lid:	language id, in INT, spec the language CODEs are. 0 for C, 1 for CPP, 2 for Java.
	pid:	problem id, in INT, spec the problem, used for selecting data and partition task.
	uname:	user name,in int,spec the user, used to avoid judge between codes written by same user.

	In data section, the pid must match the codes' you use in sql bulk.
"""

#when use multi_line,this func return a sql stmt when given a file reader iter.
def getnxtsql(ifi):
	sql=''
	while(True):
		sql+=ifi.next()
		if(sqlite3.complete_statement(sql)):
			if(sql.lstrip().upper().startswith("INSERT")):
				return sql
			else:
				raise Exception("The sql bulk file contains not only INSERTs.")

def main(fsql,fdata,opt):
	db=sqlite3.connect(opt)
	c=db.cursor()
	try:
		c.execute("drop table codes")
		c.execute("drop table datas")
	except sqlite3.OperationalError,x:pass
	c.execute("create table codes(cid int primary key,lid int,pid int,uid int,code text)")
	c.execute("create table datas(pid int primary key,data BLOB)")
	fs=open(fsql,'r')
	ifs=fs.__iter__()
	try:
		while True:
			stmt=getnxtsql(ifs)
			c.execute(stmt)
	except StopIteration:pass
	fs.close()
	for pid,fdname in fdata:
		fd=open(fdname,'rb')
		c.execute("insert into datas(pid,data) values (?,?)",(pid,sqlite3.Binary(fd.read())))
		fd.close()
	db.commit()
	db.close()

class ArgvException(BaseException):
	def __init__(self):
		pass
if __name__=="__main__":
	try:
		if(len(sys.argv)<5 or len(sys.argv)%2==0):
			raise ArgvException
		ld=[]
		for i in xrange(2,len(sys.argv)-1,2):
			ld.append((int(sys.argv[i]),sys.argv[i+1]))
		main(sys.argv[1],ld,sys.argv[-1])
	except ArgvException,x:
		print("Usage: %s <sql input filename> <data 1 pid> <data 1 filename> ... <data n pid> <data n filename> <output sqlite db>"%sys.argv[0])
	
