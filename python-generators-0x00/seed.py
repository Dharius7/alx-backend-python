import mysql.connector
import csv
import uuid

DB_NAME = "ALX_prodev"


def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # or your MySQL username
            password="",  # add password if required
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="", database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            );
        """
        )
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    cursor = connection.cursor()
    try:
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]
                # Avoid duplicates using INSERT IGNORE or REPLACE as needed
                cursor.execute(
                    """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """,
                    (user_id, name, email, age),
                )
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
