#!/usr/bin/python          

import socket              
import sys, getopt

def submit_flag(result):
	print result + "\n"

def check_sb(data):
	print "TEAM\t\tSCORE\n"
	sb = data.split(',')
	for i in xrange(0,len(sb)/2+1,2):
		print str(sb[i]) + "\t\t" + str(sb[i+1]) + "\n"


def main(argv):
   	HOST = '192.168.33.11'   
	PORT = 8888 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
   	try:
      		opts, args = getopt.getopt(argv,"hs:c:",["submit=","checksb="])
   	except getopt.GetoptError as err:
        	print(err)
        	usage()
        	sys.exit(2)
	
	data = 'x_x_x'
	for opt, arg in opts:
      		if opt == '-h':
         		print 'test.py [-s <flag>] [-c scoreboard]\t\t# -s [--submit] : submit flag\t -c [--checksb] : check scoreboard'
         		sys.exit()

      		elif opt in ("-s", "--submit"):
			data = '' + arg
			
      		elif opt in ("-c", "--checksb"):
			data += '_1'
	check = data.split('_')
	if len(check) == 3:
		data += '_0'
	
	s.send(data)
	result = s.recv(1024)
	
	check = data.split('_')
	if check[3] == '0':
		submit_flag(result)
	else:
		if check[0] == 'x':
			check_sb(result)
		else:
			result = result.split('@')
			submit_flag(result[0])
			check_sb(result[1])


	s.close()       

if __name__ == "__main__":
   	main(sys.argv[1:])
