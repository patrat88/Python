# Script for dump database under Windows environment

"""Requried prequisities:
Script require pyodbc module 

If pyodbc module is not present, in windows cmd line:
pip install pyodbc

1. Script should be executed from Windows command line
2. win_dump.py --help provide usage of script

    Script for dump database under WinNT environment
    win_dump.py
    --server        <server_name>
    --user          <user>
    --password      <password>
    --dir           <directory>
    Example:

    For dump
    win_dump.py --server [SERVER_NAME] --user [USER] --password [PASSWORD] --dir [DUMP_DIRECTORY] 
    
3. All parameters are required """

__author__ = "Patryk Walaszkowski"
__email__ = "pwalaszkowski@gmail.com"

import pyodbc
import getopt
import sys
import os 

from common.general_helpers import CheckIsDir
from common.db_helpers import connect, db_list

def backup(cursor, directory, db_list):
    """Make backup of existing databases to specified directory"""
    
    if not CheckIsDir(directory):
        print ("Directory {0} not exist".format(directory))
        return False  
    
    database = "" 
    db_list = [str(database) for database in db_list]
    for database in db_list :
        try:
            backup_db = "BACKUP DATABASE [{0}] TO  DISK = N'{1}\{0}.bak' WITH NOFORMAT, NOINIT,  NAME = N'{0}-Full Database Backup', SKIP, NOREWIND, NOUNLOAD,  STATS = 10 ".format(database, directory)
            print(backup_db)
            cursor.execute(backup_db)
            while cursor.nextset():
                pass
        except:
            print("Unexpected error")

    print("Check that backup has been done correctly")
    backup_files = os.listdir(directory)
    backup_files = map(lambda file:file.replace('.bak',''), backup_files)
    print("Backed up following databases {0}".format(backup_files)) 
    
    difference = set(backup_files).symmetric_difference(db_list)
    if difference != "":
        print("Not backed up databases {0}".format(difference))
    
    return difference 
         
def usage():
    """Print usage"""
    print("Script for dump database under WinNT environment\n"
            "win_dump.py \n"
            "--server        <server_name>\n"
            "--user          <user>\n"
            "--password      <password>\n"
            "--dir           <directory>\n"
            
            "Example: \n\n"
            
            "win_dump.py --server [SERVER_NAME] --user [USER] --password [PASSWORD] --dir [DUMP_DIRECTORY]")
    
    return True 
    
def main(argv):
    """Main function"""
    server = ""
    user = ""
    password = ""
    directory = ""
   
    try:
        opts, args = getopt.getopt(argv,"h:s:u:p:f",["server=","user=","password=", "dir=",])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage()
            sys.exit()
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", "--password"):
            password = arg
         
            print("Server:   ", server)
            print("User:     ", user)
            print("Password: ", password )

            print "Establish connection to DB"
            cursor = connect(server, user, password)
             
            get_list = db_list(cursor)
      
        elif opt in ("-f", "--dir"):
            directory = arg 
            
            backup_db = backup(cursor, directory, get_list)
            cursor.close()
   
if __name__ == "__main__":
   main(sys.argv[1:])
    
   