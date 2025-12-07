#import sqlite3
#import os
#from pathlib import Path
# THIS FILE IS OBSOLETE. DATA IS NOW FETCHED VIA API FROM API_URL
#class ConnectDB:
#    def __init__(self):
#        base_dir = Path(__file__).resolve().parent
#        # Find the path where the database is
#        db_path = base_dir.parent / 'database' / 'budget_buddy.db'
#
#        # String version of absolute path for sqlite3.connect
#        self.database = str(db_path)
#        
#        # Print the path for debugging
#        print(f"Connecting to database at: {self.database}")
#        try:
#            # Check if directory exists and create it if it does not
#            db_path.parent.mkdir(parents = True, exist_ok = True)
#            self.conn = sqlite3.connect(self.database)
#            self.cursor = self.conn.cursor()
#        except Exception as e:
#            raise e
#
#    def close_connection(self):
#        self.conn.commit()
#        self.conn.close()
