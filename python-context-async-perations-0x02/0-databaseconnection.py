import sqlite3

class DatabaseConnection:
    def __init__(self):  #
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect("users.db")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# Required usage
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
