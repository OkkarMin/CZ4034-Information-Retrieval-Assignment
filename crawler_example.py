import requests
import random
from faker import Faker
from time import sleep

fake = Faker()


def crawl_for_data():
    # Crawling for data
    data = {
        "name": fake.name(),
        "gender": random.choice(["Male", "Female", "Non-binary"]),
        "age": random.randrange(1, 100),
        "job": fake.job(),
        "favourite_movie": fake.text(max_nb_chars=20)
    }

    return data


def post_to_logstash(data_in_json):
    logstash_http_endpoint = "http://irgroup13.ml:5151"

    requests.post(logstash_http_endpoint, json=data_in_json)


while True:
    try:
        data = crawl_for_data()
        print(data)

        post_to_logstash(data)

        sleep(1)
    except Exception as e:
        print(e)
