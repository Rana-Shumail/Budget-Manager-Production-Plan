import user_db
import psycopg2

def add_email_column():
    print("Connecting to database...")
    conn = user_db.connect()
    cur = conn.cursor()
    try:
        # Add the 'email' column
        cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
        conn.commit()
        print("SUCCESS: Added 'email' column to users table.")
    except psycopg2.errors.DuplicateColumn:
        print("INFO: 'email' column already exists.")
        conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_email_column()
