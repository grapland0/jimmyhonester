#!/usr/bin/python

import os,sys,sqlite3,urllib,subprocess,threading


#access_need indicates all files need to be modified in this app, remember to update this after create/remove some files.
#CAUTION: ALL file you list here will be erased after app running.
access_need=('~tmp.c','~tmp.cpp','~tmp.java','~tmpexec','bbtrack.out','~tmp.gcno','~tmp.gcda')

class tle_runner:
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout,data):
		fn=open("/dev/null","w")
		def target():
			self.process = subprocess.Popen(self.cmd,stdin=subprocess.PIPE,stdout=fn,stderr=fn)
			self.pid=self.process.pid
			self.process.communicate(data)

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		fn.close()
		if thread.is_alive():
			sys.stdout.write('[TLE]')
#os.system("kill -9 %d"%self.pid)
			self.process.terminate()
			thread.join()
			return False
		return True

def main(pk,orr):
	#check environment
	try:
		for it in access_need:
			if(os.path.isfile(it)):
				raise Exception("Please delete these file in order to make sure they are useless to you: %s.\nWarning: DO NOT TRY to start more than one pk2rr process in one directory."%" ".join(access_need))
		if(not os.path.isfile('gcov_mod')):
			raise Exception("Cannot find gcov_mod. Copy it to the running directory.")
	except Exception,x:
		print x
		return
	#load db
	db=sqlite3.connect(pk)
	c=db.cursor()
	c.row_factory=sqlite3.Row

	#prepare rr file
	fr=open(orr,'w')

	#run them!
	c.execute('select cid,lid,uid,pid,code from codes')
	drd=db.cursor()
	for ir in c:
		cid=int(ir['cid'])
		lid=int(ir['lid'])
		uid=int(ir['uid'])
		pid=int(ir['pid'])
		code=ir['code']
		drd.execute('select data from datas where pid=?',(pid,))
		dr=drd.fetchone()
		sys.stdout.write(" %d[%d]"%(cid,pid))
		sys.stdout.flush()
		if(dr==None):
			#this will ignore the DATA_NOT_FOUND and continue, if you dont want it, just return 1 to terminate the process.	
			sys.stdout.write('[NoData]')
			sys.stdout.flush()
			continue
		data_in=dr[0]
		sys.stdout.flush()
		compilecmd=''
		codefn=''
		#erase exist ~tmpexec
		if(os.path.isfile('~tmpexec')):
			os.remove('~tmpexec')
		#running diff lang:
		#C
		if(lid==0):
			codefn="~tmp.c"
			compilecmd='gcc %s -ftest-coverage -fprofile-arcs -lgcov -o ~tmpexec 1>/dev/null 2>/dev/null'%codefn
		#C++
		elif(lid==1):
			codefn="~tmp.cpp"
			compilecmd='g++ %s -ftest-coverage -fprofile-arcs -lgcov -o ~tmpexec 1>/dev/null 2>/dev/null'%codefn
		#we dont care others than C or C++
		else:
			continue

		#complie,run,and gcov_mod
		fcd=open(codefn,"w")
		exec("code_uq=\'%s\'"%code.replace(r"'",r"\'"))
		fcd.write(code_uq)
		fcd.close()
		os.system(compilecmd)
		if(not os.path.isfile('~tmpexec')):
			sys.stdout.write('[CE]')
			sys.stdout.flush()
			#this will ignore the CE and continue, if you dont want it, just return 1 to terminate the process.	
			continue
		
		runner=tle_runner('./~tmpexec')
		if(not runner.run(3,data_in)):
			continue

		os.system("./gcov_mod %s 1>/dev/null 2>/dev/null"%codefn)
		if(os.path.isfile('bbtrack.out') and os.path.getsize('bbtrack.out')!=0):
			fi=open("bbtrack.out",'r')
			fr.write("@rr %d\n @uid %d\n @pid %d\n"%(cid,uid,pid))
			for ln in fi:
				fr.write(ln)
			fr.write("@.rr\n")
			fi.close()
			os.remove('bbtrack.out')
		else:
			sys.stdout.write('[GCOV_ERR]')
			sys.stdout.flush()
	fr.close()
	db.close()
	os.system('rm %s'%' '.join(access_need))

if __name__=='__main__':
	if(3==len(sys.argv)):
		main(sys.argv[1],sys.argv[2])
	else:
		print("Usage: %s <pk file> <opt rr file>"%sys.argv[0])

