from kafka import KafkaProducer
import json
import time
from datetime import datetime
import random

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulated machine IDs
machines = ['M1', 'M2', 'M3']

print("Sending simulated sensor data to Kafka...")
try:
    while True:
        data = {
            'machine_id': random.choice(machines),
            'temperature': round(random.uniform(60, 100), 2),
            'timestamp': datetime.now().isoformat()
        }
        print(f"Sending: {data}")
        producer.send('test-replicated', value=data)
        time.sleep(2)  # send every 2 seconds

except KeyboardInterrupt:
    print("Stopped.")
    producer.close()
