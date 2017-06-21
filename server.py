import socket
import sys
import mysql.connector
 
HOST = ''   
PORT = 8888 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print '[*] Socket created'
 
#Bind socket to local host and port
try:
    	s.bind((HOST, PORT))
except socket.error as msg:
    	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    	sys.exit()
     
print '[*] Socket bind complete'
 
#Start listening on socket
s.listen(10)
print '[*] Socket now listening'

#Check flag and update score
def check_flag(submit_team_id,chal_id,flag): 

	
	connect = mysql.connector.connect(user='root', password='addevteam', host='127.0.0.1', database='ad')
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM available")
	rows = cursor.fetchall()
	
	existed_chal_id = False
	for avai in rows:
		if int(avai[0]) == int(chal_id):
			existed_chal_id = True
			available_table = avai
			break
	if not existed_chal_id:
		connect.close()
		return "Challenge ID not exists!"
	
	if int(submit_team_id) != available_table[2]: #not the owner
		valid = False
		team_submitted = available_table[1][:-1].split(',')
		if submit_team_id not in team_submitted: #not yet summitted 
			valid = True

		if valid:
			cursor.execute("SELECT team_id,flag,point FROM challenge WHERE challenge_id=%s", (chal_id,))					
			challenge_table = cursor.fetchone()
			if flag.strip() == challenge_table[1]: #correct flag
				#Give point for submit team for correct flag and add that team to team_submit in available
				cursor.execute("SELECT score FROM team WHERE team_id=%s", (submit_team_id,))
				score = cursor.fetchone()
				print score
				print challenge_table[2]
				score = score[0] + challenge_table[2]
				print score
				cursor.execute("UPDATE team SET score=%s WHERE team_id=%s", (score, submit_team_id))	
				cursor.execute("UPDATE available SET team_submit=concat(team_submit,%s,',') WHERE chal_id=%s", (submit_team_id,chal_id))
				
				#Take point from team whose flag is submmited by another team
				cursor.execute("SELECT score FROM team WHERE team_id=%s", (challenge_table[0],))
				score = cursor.fetchone()
				score = score[0] - challenge_table[2]
				print score
				cursor.execute("UPDATE team SET score=%s WHERE team_id=%s", (score, challenge_table[0]))
				
				connect.commit()
				connect.close()
				return "Correct flag!! Your team got " + str(challenge_table[2]) + " points from team " + str(challenge_table[0])
		else:
			connect.close()
			return "Flag is already submitted!"
	else:
		connect.close()
		return "You cannot submit your own flag!"

	connect.close()
	return "Incorrect flag!!!"	

def check_sb():
	connect = mysql.connector.connect(user='root', password='addevteam', host='127.0.0.1', database='ad')
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM team")
	sb = cursor.fetchall()
	sb_list = []
	sb_string = ''
	for i in sb:
		for j in i:
			sb_list.append(j)
	sb_string = ','.join(map(str,sb_list))
	return sb_string

#now keep talking with the client
while 1:
 	#wait to accept a connection - blocking call
   	conn, addr = s.accept()
    	print 'Connected with ' + addr[0] + ':' + str(addr[1])
     	data = conn.recv(1024)
	if not data:
		continue

	data = data.split('_')
	team_id = data[0]
	chal_id = data[1]
	flag = data[2]
	sb = data[3]

	if team_id == 'x':
		result = check_sb()
	else:
		if sb == '0':
			result = check_flag(team_id,chal_id,flag)
		else:
			result = check_flag(team_id,chal_id,flag) + '@' + check_sb()
 
	conn.send(result)		

	
s.close()
