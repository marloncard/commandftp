import credentials
from ftplib import FTP
import ftplib
import os
## TODO:
# Add move file (mv)
# Add local files functions(Use "swap" to switch between "REMOTE" & "LOCAL")
	# - 'ls local' to view local files??
	# - 'cd local' to change local dir??
# Add ability to change file permissions?
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
		print('')
		print('type [help] to view a list of commands')
	fftp.login(credentials.user, credentials.passw) # enters login info
	fftp.dir				# view current directory listing
	return fftp

ftp = connect(url)
	
def disconnect():
	really = input('Really end session? ').lower().strip()
	if really == 'y' or really == 'yes':
		ftp.quit()
	else:
		command_line()

def getfile(path):
	try:
		filename = path
		localfile = open(filename, 'wb')
		ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
		localfile.close()
	except ftplib.all_errors as err:
		print('')
		print(err) # Print python generated error messages
		localfile.close()
		if os.path.exists(filename):	# Delete empty file created locally
			os.unlink(filename)
		command_line()
	else:
		print('')
		print('Download of {} sucessful!'.format(filename))
		print('')
		command_line()

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
	command_line()

def putfile(path):
	try:
		filename = path
		ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
	except ftplib.all_errors as err:
		print('')
		print(err) # Print python generated error messages
	else:
		print('')
		print('Upload of {} sucessful!'.format(filename))
		print('')
	command_line()

def pwd(): # Show current working directory
	print('')
	print(ftp.pwd())
	print('')
	command_line()
	
def pwd_local(): # Show local current working directory
	print('')
	print(os.getcwd())
	print('')
	command_line()
	
def viewdir():
	ftp.retrlines('LIST') 	# List directory contents
	print('')
	command_line()

def viewdir_local(path):
	try:
		local_dir = os.listdir(path)
		print('')
		print(path)
		print('')
		for f in local_dir:
			print(f)
	except FileNotFoundError as e:
		print('')
		print(e.strerror) # Print system generated error message
	print('')
	command_line()

def cwd(path):
	try:
		ftp.cwd(path) # Change current directory.
	except ftplib.all_errors as err:
		print('')
		print(err) # Print python generated error messages
	print('')
	command_line()
	
def cwd_local(path):
	try:
		os.chdir(path) # Change current local directory.
	except FileNotFoundError as e:
		print('')
		print(e.strerror) # Print system generated error message
	print('')
	command_line()
	
def remove(path):
	rm_file = path
	try:
		ftp.delete(rm_file) # Delete a file.
	except ftplib.all_errors as err:
		print('')
		print(err) # Print python generated error messages
	else:
		print('')
		print('{} has been deleted.'.format(rm_file))
		print('')
	command_line()
	
def help():
	print('')
	print('=' * 10)
	print('[help] to view this list of commands')
	print('[q] to quit')
	print('[ls] to list dir contents')
	print('[ls -l] to list local dir contents')
	print('[pwd] to show working dir')
	print('[pwd -l] to show local working dir')
	print('[cd] to change dir')
	print('[cd -l] to change local dir')
	print('[get] to download file, [getall] to download directory')
	print('[put] to send file')
	print('[rm] to delete')
	print('=' * 10)
	print('')
	command_line()

def command_line():
	current_dir = ftp.pwd()
	command = input('root{}:> '.format(current_dir))
	if command == 'h' or command =='help':
		help()
	elif command == 'q' or command =='quit' or command =='exit':
		disconnect()
	elif command == 'ls':
		viewdir()
	elif command[0:5] == 'ls -l':
		if command[6:] == '':
			path = '.'
			viewdir_local(path)
		else:
			path = command[6:]
			viewdir_local(path)
	elif command[0:5] == 'cd -l':
		if command[6:] == '':
			path = '.'
			cwd_local(path)
		else:
			path = command[6:]
			cwd_local(path)
	elif command[0:3] == 'cd ':
		path = command[3:]
		cwd(path)
	elif command == 'pwd':
		pwd()
	elif command == 'pwd -l':
		pwd_local()
	elif command[0:4] == 'get ':
		path = command[4:]
		getfile(path)
	elif command == 'getall':
		getall()
	elif command[0:4] == 'put ':
		path = command[4:]
		putfile(path)
	elif command[0:3] == 'rm ':
		path = command[3:]
		remove(path)
	else:
		print("")
		print("=====Command Unknown=====")
		print("")
		command_line()


command_line()