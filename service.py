import socket
import mysql.connector
import sys

port_list = [5101,5102,5201,5202]

def check_service(host, port, content):
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.connect((host, int(port)))
    	s.sendall(content)
       	s.settimeout(5.0)
	data = s.recv(1024)
	if not data: #Cannot receive data after 5s timeout
		connect = mysql.connector.connect(user='root', password='addevteam', host='127.0.0.1', database='ad')
		cursor.execute("SELECT score FROM team WHERE team_id=%s", (challenge_table[0],))
		score = cursor.fetchall() - 50
		cursor.execute("UPDATE team SET score=%s WHERE team_id=%s", (score, challenge_table[0]))		
		connect.commit()
		connect.close()
       		
    	s.close()

for port in port_list:
	check_service('192.168.34.11',port,'Checking service')
