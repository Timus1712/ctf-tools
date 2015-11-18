import subprocess
import telnetlib
import os

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


def chooseGoodIp(l):
	a = []
	for x in l:
		response = subprocess.call(["ping", "-c 1", "-W 3", x], stdout=DEVNULL, stderr=subprocess.STDOUT)
		if response == 0:
			print x, "is ok"
			yield x
		else:
			print x, "is not ok"


def submit(flag):
	tn = telnetlib.Telnet(HOST, PORT)
	tn.write(bytes(str(flag) + "\n", 'utf-8'))
	print(tn.read_all())


def get_flag(ip):
	pass #get flag from team with ip


ips = getIpList()

while True:
	for ip in chooseGoodIp(ips): #just try to get flag from servers which respons in 3 seconds
		flag = get_flag(ip)
		submit(flag)
	time.sleep(5) #if needed
