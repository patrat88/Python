# Script for load database under Windows environment

"""Requried prequisities:
Script require pyodbc module 

If pyodbc module is not present, in windows cmd line:
pip install pyodbc

1. Script should be executed from Windows command line
2. win_load.py --help provide usage of script

    Script for load database under WinNT environment
    win_load.py
    --server        <server_name>
    --user          <user>
    --password      <password>
    --dir           <directory>

    Example:

    For load
    win_load.py --server [SERVER_NAME] --user [USER] --password [PASSWORD] --dir [DUMP_DIRECTORY]
    
3. All parameters are required """

__author__ = "Patryk Walaszkowski"
__email__ = "pwalaszkowski@gmail.com"

import pyodbc
import getopt
import sys
import os 
import stat
import errno

from common.general_helpers import CheckIsDir
from common.db_helpers import connect, db_list

def load(cursor, directory, db_list):
    """Load databases from specified directory"""
    
    if not CheckIsDir(directory):
        print ("Directory {0} not exist".format(directory))
        return False  
    
    database = "" 
    db_list = [str(database) for database in db_list]
    print("Available databases")
    print(os.listdir(directory))
    
    for database in db_list:
        
        load_db = "RESTORE DATABASE {0} FROM DISK = N'{1}\{0}.bak' WITH  FILE = 1,  NOUNLOAD,  REPLACE,  STATS = 10".format(database, directory)
        print(load_db)
        cursor.execute(load_db)
        while cursor.nextset():
            pass
    
    return cursor 

def usage():
    """Print usage"""
    print("Script for load database under WinNT environment\n"
            "win_load.py \n"
            "--server        <server_name>\n"
            "--user          <user>\n"
            "--password      <password>\n"
            "--dir           <directory>\n"
            
            "Example: \n\n"
            
            "win_load.py --server [SERVER_NAME] --user [USER] --password [PASSWORD] --dir [DUMP_DIRECTORY]")
    
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
         
            load_db = load(cursor, directory, get_list)
            cursor.close()
   
if __name__ == "__main__":
   main(sys.argv[1:])