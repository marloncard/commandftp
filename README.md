# commandftp
A simple command line FTP client in python using ftplib (python 3.0).

This project is primarily practice but I plan on using it myself when in need of a quick ftp client. 

1. Nothing to install, just type 'python commandftp.py'
2. At the **root:>** prompt enter simple linux like commands: 

  - **ls** to list directory contents
  - **ls -l** <*path*> to list local directory contents
  - **cd** <*path*> to change working directory
  - **cd -l** <*path*> to change local working directory
  - **rm** <*file*> to delete file
  - **get** <*file*> to download a file
  - **getall** to download all files in current working directory
  - **put** <*file*> to upload a file
  - **q** or **quit** or **exit** to disconnect
  - **help** to show a list of commands

3. Currently you can hard code your login info to credentials.py instead of constantly entering it in the prompt however you don't have to.

##Upcoming Additions

1. "Put" a local directory and all it's contents.
2. Create local directory
3. Create remote directory

