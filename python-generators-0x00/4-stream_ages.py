# 3-avg_age.py
seed = __import__("seed")


def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row["age"]
    connection.close()


def average_user_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count > 0:
        print(f"Average age of users: {total_age / count:.2f}")
    else:
        print("No users found.")


# Run only when executed as a script
if __name__ == "__main__":
    average_user_age()
