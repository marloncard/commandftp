from ftplib import FTP
import ftplib

# Add move file (mv)
# Add view local files
# Add ability to change file permissions?

user = 'qualico@qualicotrading.com'
passw = '987!2Hpu8$9'
url = input('Enter FTP url: ') #'ftp.qualicotrading.com'


def connect(url):
	try:
		fftp = FTP(url)		#connect to the host, default port
	except ftplib.all_errors as err:
		print('Could not connect to {}'.format(url)) # message if unable to connect
		print(err) # print actual error message
		quit()
		
	else:
		print('Connected to {}'.format(url))
		print('Welcome message is:')
		welcome = fftp.getwelcome()
		print(welcome)
	fftp.login(user, passw) # enters login info
	fftp.dir				# view current directory listing
	return fftp

ftp = connect(url)
	
def disconnect():
	really = input('Really end session? ').lower().strip()
	if really == 'y':
		ftp.quit()
	else:
		menu()
		
def getfile():
	filename = input('Filename: ')
	localfile = open(filename, 'wb')
	ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
	localfile.close()
	menu()
	
def getall():
	for file in ftp.retrlines('LIST'):
		localfile = open(file, 'wb')
		ftp.retrbinary('RETR ' + file, localfile.write, 1024)
		localfile.close()
		print(file + ' download successful!')
	menu()
		
def putfile():
	filename = input('Filename: ')
	ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
	menu()
	
	
def pwd(): #Sort of works...
	print('')
	print(ftp.pwd())
	menu()
	
def viewdir():
	ftp.retrlines('LIST') 	# List directory contents
	menu()
	
def cwd():
	ftp.cwd(input('path: ')) # Change current directory.
	menu()
	
def remove():
	ftp.delete(input('Filename: ')) # Delete a file.
	menu()
	
def menu():
	print('')
	print('*' * 10)
	print('[q] to quit')
	print('[ls] to list dir contents')
	print('[pwd] to show working dir')
	print('[cd] to change dir')
	print('[get] to download file, [getall] to download directory')
	print('[put] to send file')
	print('[rm] to delete')
	
	command = input('What is your command: ').lower().strip()
	if command == 'q':
		disconnect()
	elif command == 'ls':
		viewdir()
	elif command == 'pwd':
		pwd()
	elif command == 'cd':
		cwd()
	elif command == 'get':
		getfile()
	elif command == 'getall':
		getall()
	elif command == 'put':
		putfile()
	elif command == 'rm':
		remove()
	else:
		print("***Unknown command***")
		print("")
		menu()

menu()
