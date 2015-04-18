import credentials
from ftplib import FTP
import ftplib
import os
## TODO:
# Remove default menu; User types "help" for command list
# Add confirmations for all actions
# Add error handling
# Add move file (mv)
# Add local files functions(Use "swap" to switch between "REMOTE" & "LOCAL")
	# - 'ls local' to view local files
	# - 'cd local' to change local dir
# Add ability to change file permissions?
# Move to 2.0 and make command entry more like linux
# Add ability to put and get directories and contents


url = input('Enter FTP url: ')

def connect(url):
	try:
		fftp = FTP(url)		#connect to the host, default port
	except ftplib.all_errors as err:
		print('Could not connect to {}'.format(url)) # message if unable to connect
		print(err) # Print python generated error messages
		quit()
	else:
		print('Connected to {}'.format(url))
		print('Welcome message is:')
		welcome = fftp.getwelcome()
		print(welcome)
	fftp.login(credentials.user, credentials.passw) # enters login info
	fftp.dir				# view current directory listing
	return fftp

ftp = connect(url)
	
def disconnect():
	really = input('Really end session? ').lower().strip()
	if really == 'y' or really == 'yes':
		ftp.quit()
	else:
		menu()

def getfile():
	try:
		filename = input('Filename: ')
		localfile = open(filename, 'wb')
		ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
		localfile.close()
	except ftplib.all_errors as err:
		print('')
		print(err) # Print python generated error messages
		localfile.close()
		if os.path.exists(filename):	# Delete empty file created locally
			os.unlink(filename)
		menu()
	else:
		print('')
		print('Download of {} sucessful!'.format(filename))
		print('')
		menu()

def getall():
	file_list = []
	ftp.retrlines('NLST', file_list.append) # append list of files in directory using callback
	file_list.remove('.') # remove current directory '.'
	file_list.remove('..') # remove previous directory '..'
	print('')
	print('=' * 10)
	print('<Retrieving ' + str(len(file_list)) + ' files>')
	print('')
	print('=' * 10)
	for filename in file_list:
		try:
			localfile = open(filename, 'wb')
			ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
			localfile.close()
			print('<' + filename + '> download successful!')
		except ftplib.all_errors as err:
			print('')
			print(err) # Print python generated error messages
			localfile.close()
			if os.path.exists(filename):	# Delete empty file created locally
				os.unlink(filename)
	menu()

def putfile():
	try:
		filename = input('Filename: ')
		ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
	except ftplib.all_errors as err:
		print('')
		print(err) # Print python generated error messages
	else:
		print('')
		print('Upload of {} sucessful!'.format(filename))
		print('')
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
	print('=' * 10)
	print('[q] to quit')
	print('[ls] to list dir contents')
	print('[pwd] to show working dir')
	print('[cd] to change dir')
	print('[get] to download file, [getall] to download directory')
	print('[put] to send file')
	print('[rm] to delete')
	
	command = input('What is your command: ').lower().strip()
	if command == 'q' or command =='quit' or command =='exit':
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
		print("")
		print("***Unknown command***")
		print("")
		menu()

menu()
