from ftplib import FTP
import ftplib

# Add better error handling especially for getfile(trying to get it to work) **REVIEW TREEHOUSE LESSON**
# Add delete remote file (rm)
# Add move file (mv)
# Add ability to change file permissions?

user = 'qualico@qualicotrading.com'
passw = '987!2Hpu8$9'
url = input('Enter FTP url: ') #'ftp.qualicotrading.com'


def connect(url):
	try:
		fftp = FTP(url)		#connect to the host, default port
	except ftplib.all_errors:
		print('Could not connect to {}'.format(url))
		#print(str(e))
	else:
		print('Connected to {}'.format(url))
		print('Welcome message is:')
		welcome = fftp.getwelcome()
		print(welcome)
	fftp.login(user, passw) # enters login info
	fftp.dir				# view current directory listing
	menu()
	return fftp

def disconnect():
	really = input('Really end session? ').lower().strip()
	if really == 'y':
		ftp.quit()
	else:
		menu()
		
def getfile():
	filename = input('Name of file: ')
	localfile = open(filename, 'wb')
	ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
	localfile.close()
	menu()
	
def getall():
	pass
	
def putfile():
	filename = input('Name of file: ')
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
	
def menu():
	print('')
	print('*' * 10)
	print('[q] to quit')
	print('[ls] to list dir contents')
	print('[pwd] to show working dir')
	print('[cd] to change dir')
	print('[get] to download file')
	print('[put] to send file')
	
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
	elif command == 'put':
		putfile()
	else:
		print("***Unknown command***")
		print("")
		menu()

ftp = connect(url)