import mysql.connector


def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # update as needed
        password="",  # update as needed
        database="ALX_prodev",
    )
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    finally:
        cursor.close()
        connection.close()
