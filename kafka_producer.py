from kafka import KafkaProducer
import time
import os

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'test_topic4'
source_directory = 'data/source_data'

def send_logs_to_kafka():
    for file_name in os.listdir(source_directory):
        if file_name.endswith('.xml'):
            file_path = os.path.join(source_directory, file_name)
            with open(file_path, 'r') as file:
                data = file.read()
                print(data)
                producer.send(topic, value=data.encode('utf-8'))
            os.remove(file_path)
            time.sleep(1)

if __name__ == "__main__":
    while True:
        print("Producing data to Kafka topic", topic)
        send_logs_to_kafka()
        time.sleep(10)
