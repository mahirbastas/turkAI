import pika
import json
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

INTERPOL_API_URL = "https://api.interpol.int/public/Data/WANTED"
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
QUEUE_NAME = os.getenv("QUEUE_NAME")
INTERVAL = int(os.getenv("INTERVAL"))

def fetch_interpol_data():
    try:
        response = requests.get(INTERPOL_API_URL)
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching Interpol data:", e)
        return None

def publish_to_rabbitmq(data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=json.dumps(data))
        print("Data published to RabbitMQ:", data)
        connection.close()
    except Exception as e:
        print("Error publishing data to RabbitMQ:", e)

if __name__ == "__main__":
    while True:
        interpol_data = fetch_interpol_data()
        if interpol_data:
            publish_to_rabbitmq(interpol_data)
        time.sleep(INTERVAL)
