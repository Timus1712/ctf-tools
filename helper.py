import subprocess
import telnetlib
import time
import os
from multiprocessing import Pool, Manager, Process

# jury submit server
# URY_HOST = "10.10.10.3"
# PORT = 80

#our submit server info
HOST = "10.60.156.3"
PORT = 1992

TEAM_HOST = "team{team_number}.e.ructf.org"

MAX_TEAM_NUMBER = 324
OUR_TEAM_NUMBER = 156

DEVNULL = open(os.devnull, 'wb')


def ips_generator():
	i = 1
	while True:
		ip = TEAM_HOST.format(team_number=i)
#		ip = "10." + str(60 + i / 255) + "." + str(i % 255) + ".2"
		if i != OUR_TEAM_NUMBER:
			yield (ip, i)
		i += 1
		if i == MAX_TEAM_NUMBER + 1:
			break


def check_ip(ip):
	response = subprocess.call(["ping", "-c 1", "-W 1", ip],
		stdout=DEVNULL, stderr=subprocess.STDOUT)
	return response == 0


def submit(flag):
	while True:
		try:
			tn = telnetlib.Telnet(HOST, PORT)
			tn.write(bytes(str(flag) + "\n"))
			print tn.read_all()
			break
		except:
			print "Error while connection to submitter"
			time.sleep(15)
			continue


def parallelize_wrapper(func, q, ip, team_id):
	if check_ip(ip):
		flag = func(ip, team_id)
		q.put(flag)


def parallelize_sender(q):
	while True:
		flag = q.get()
		if flag is None:
			break
		if type(flag) == str:
			print "Send ", flag
			submit(flag)
		else:
			for f in flag:
				print "Send ", f
				submit(f)


def parallelize(flag_getter, threads=5):
	ips = ips_generator()
	try:
		m = Manager()
		p = Pool(threads)
		q = m.Queue()
		submitter = Process(target=parallelize_sender, args=(q,))
		submitter.start()
		while True:
			for ip, team_id in ips:
				# for ip, team_id in ips_generator():
				# print "stealing flag from {1} with ip: {0}".format(ip, team_id)
				p.apply_async(parallelize_wrapper, args=(flag_getter, q, ip, team_id,))
	except KeyboardInterrupt:
		submitter.terminate()
		p.terminate()
		p.join()


def get_flag(ip, team_id=None):
	pass # return flag from team_id with ip (possible to return a list of flags)


parallelize(get_flag, threads=5)
