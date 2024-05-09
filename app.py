from flask import Flask, render_template
import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
QUEUE_NAME = os.getenv("QUEUE_NAME")

def callback(ch, method, properties, body):
    data = json.loads(body)
    # Burada veriyi istenilen veritabanına kaydedebilirsiniz
    print("Received data from RabbitMQ:", data)

@app.route("/")
def index():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print("Error consuming data from RabbitMQ:", e)
    return render_template("index.html", data={})

if __name__ == "__main__":
    app.run(debug=True)
