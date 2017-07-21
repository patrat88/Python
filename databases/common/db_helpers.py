# Helper functions for load/dump DB scripts 
__author__ = "Patryk Walaszkowski"
__email__ = "patryk.walaszkowski@misys.com, QAKPlusTech@misys.com"

import pyodbc
import getopt
import sys
import os 

def connect(server, user, password):
    """Connect to database instance"""
    connection = pyodbc.connect('Driver={0};Server={1};Database=master;uid={2};pwd={3};'.format("SQL Server", server, user, password), trusted_connection='yes', autocommit=True)
    cursor = connection.cursor()
    return cursor
    
def db_list(cursor):
    """Provide list of K+ and K+TP databases"""
    
    db_list = []
    get_db_list = "SELECT name FROM master.dbo.sysdatabases where sid <>0x01"
    
    try:
        cursor.execute(get_db_list)
    except:
        print("Unexpected error")
        
    rows = cursor.fetchall()
    
    for db in rows:
        db_list.append(db[0])
        
    print("Provided databases {0}".format(db_list))
    return db_list
    
if __name__ == "__main__":
   main(sys.argv[1:])