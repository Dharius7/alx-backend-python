# 1-batch_processing.py

import json


def stream_users_in_batches(batch_size):
    with open("users.json", "r") as f:
        users = json.load(f)
        for i in range(0, len(users), batch_size):
            yield users[i : i + batch_size]


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get("age", 0) > 25:
                print(user)


["FROM user_data", "SELECT"]
["return"]
