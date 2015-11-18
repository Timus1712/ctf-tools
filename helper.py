import subprocess
import telnetlib
import os
from multiprocessing import Pool, Queue, Manager, Process

#submit server info
HOST = "10.0.1.13"
PORT = 9000

MAX_TEAM_NUMBER = 312

DEVNULL = open(os.devnull, 'wb')

def getIpList():
	l = []
	for i in range(1, MAX_TEAM_NUMBER + 1):
		l.append("10." + str(60 + i / 255) + "." + str(i % 255) + ".3")
	return l


def check_ip(ip):
	response = subprocess.call(["ping", "-c 1", "-W 1", ip], stdout=DEVNULL, stderr=subprocess.STDOUT)
	return response == 0


def chooseGoodIp(ips):
	cur = 0
	while True:
		ip = ips[cur]
		team_id = cur + 1
		if check_ip(ip):
			yield (ip, team_id)
		cur += 1
		if cur == len(ips):
			cur = 0


def submit(flag):
	tn = telnetlib.Telnet(HOST, PORT)
	tn.write(bytes(str(flag) + "\n", 'utf-8'))
	print(tn.read_all())


def parallelize_wrapper(func, q, ip, team_id):
	flag = func(ip, team_id)
	q.put(flag)


def parallelize_sender(q):
	while True:
		flag = q.get()
		if flag == None:
			break
		if flag is str:
			print "Send ", flag
			submit(flag)
		else:
			for f in flag:
				print "Send ", f
				submit(f)


def parallelize(flag_getter, threads=5):
	try:
		ips = getIpList()
		m = Manager()
		p = Pool(threads)
		q = m.Queue()
		submitter = Process(target=parallelize_sender, args=(q,))
		submitter.start()
		for ip, team_id in chooseGoodIp(ips):
#			print "stealing flag from {1} with ip: {0}".format(ip, team_id)
			p.apply_async(parallelize_wrapper, args=(flag_getter, q, ip, team_id,))
	except KeyboardInterrupt:
		p.terminate()
		p.join()


def get_flag(ip, team_id=None):
	pass #return flag from team_id with ip (possible to return a list of flags)


parallelize(get_flag, threads=5)
