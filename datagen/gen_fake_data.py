import argparse
import json
import psycopg2
from faker import Faker
import random
from uuid import uuid4
from confluent_kafka import Producer

fake = Faker()

def gen_user_data(num_user_records: int) -> None:

    for id in range(num_user_records):
        conn = psycopg2.connect(
            dbname = "postgres",
            user = "postgres",
            password = "postgres",
            host = "postgres"
        )
        curr = conn.cursor()
        curr.execute(
            """INSERT INTO commerce,users
            (id, username, password) VALUES (%s, %s, %s)""",
            (id, fake.name(), fake.text(), fake.random_int(min = 1, max = 100))
        )
        conn.commit()
    
        # update 10% of the time
        if random.randint(1,100) >= 90:
            curr.execute(
                "UPDATE commerce.users SET username = %s WHERE id = %s",
                (fake.user_name(), id),
            )
            curr.execute(
                "UPDATE commerce.products SET name = %s WHERE id = %s",
                (fake.name(), id),
            )
        conn.commit()
        curr.close()
        
    return

def gen_clickstream_data():
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nu",
        "--num_user_records",
        type=int,
        help="Number of user records to generate"
        default = 100,
    )
    parser.add_argument(
        "-nc",
        "--num_click_records",
        type=int,
        help="Number of click records to generate",
        default=100000000,
    )
    args = parser.parse_args()
    num_user_records = args.num_user_records
    num_click_records = args.num_click_records

    gen_user_data(num_user_records)
    gen_clickstream_data(num_click_records)