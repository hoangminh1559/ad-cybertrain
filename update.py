#!/usr/bin/env python
import mysql.connector
import random
import time
import string
from ftplib import FTP

id_list = [5101,5102,5201,5202]
app1 = [5101,5102]
app2 = [5201,5202]

def init_db():
	connect = mysql.connector.connect(user='root', password='addevteam', host='127.0.0.1', database='ad')
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM team")
	rows = cursor.fetchall()
	for team in rows:
		current_id = team[0]
		cursor.execute("UPDATE team SET score=0 WHERE team_id=%s", (current_id,))	
	cursor.execute("UPDATE available SET team_submit=''")
	connect.commit()
	connect.close()

def connect_db():
	connect = mysql.connector.connect(user='root', password='addevteam', host='127.0.0.1', database='ad')
	print "[*] Connected to database\n"
	return connect

def disconnect_db(connect):
	connect.close()
	print "[*] Disconnected from database\n"

def random_md5():
	pool = string.letters + string.digits
    	return ''.join(random.choice(pool) for i in xrange(32))

def update_flag(connect):
	cursor = connect.cursor()
	for current_id in id_list:
		new_flag = random_md5()
		cursor.execute("UPDATE challenge SET flag=%s WHERE challenge_id=%s", (new_flag, current_id))	
	connect.commit()
	print "[*] Database updated\n"

def print_table(connect,table_name):
	cursor = connect.cursor()
	if str(table_name) == 'challenge':
		print "team_id\tchallenge_id\tflag\n"
		cursor.execute("SELECT * FROM challenge")
		rows = cursor.fetchall()
		for i in rows:
			print str(i) + "\n"
	elif str(table_name) == 'team':
		print "team_id\tscore\n"
		cursor.execute("SELECT * FROM team")
		rows = cursor.fetchall()
		for i in rows:
			print str(i) + "\n"
	else:
		print "challenge_id\tsubmit_team\towner\n"
		cursor.execute("SELECT * FROM available")
		rows = cursor.fetchall()
		for i in rows:
			print str(i) + "\n"		
	print "\n[*] Table printed\n" 

def file_export(file_name,connect):
	file = open(str(file_name),"w")
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM challenge")
	rows = cursor.fetchall()
	for i in rows:
		if str(i[1]) == str(file_name):
			file.write(str(i[2]))
			break
	file.close()

def send_flag(ip,app):
	ftp = FTP(ip)
	ftp.login(user='ftp_user', passwd='addevteam')
	ftp.cwd('/files/')
	
	for file in app:
    		ftp.storbinary('STOR ' + str(file), open(str(file), 'rb'))
    	
	ftp.quit()

def defense_points(connect):
	cursor = connect.cursor()
	cursor.execute("SELECT SUM(point) FROM challenge WHERE team_id=1")
	total_points = cursor.fetchone()
	cursor.execute("SELECT * FROM team")
	rows = cursor.fetchall()
	for element in rows: 
		current_id = element[0]
		current_point = element[1] + total_points[0]	
		cursor.execute("UPDATE team SET score=%s WHERE team_id=%s", (current_point, current_id))	
	connect.commit()
	print "[*] Teams' defense points updated\n"

init_db()
while (1):
	conn = connect_db()
	update_flag(conn)
	defense_points(conn)
	for chal in id_list:
		file_export(chal,conn)
	send_flag('192.168.32.11',app1) 
	send_flag('192.168.32.13',app2)
	print_table(conn,'team')
	print_table(conn,'challenge')
	print_table(conn,'available')
	disconnect_db(conn)
	time.sleep(1800)

