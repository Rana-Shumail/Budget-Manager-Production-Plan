import sqlite3

class ConnectDB:
    def __init__(self):
        self.database = 'database/budget.db'
        self.database = 'database/goal.db'
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

        def close_connection(self):
            self.conn.commit()
            self.conn.close()