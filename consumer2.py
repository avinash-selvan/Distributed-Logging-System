from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time
from threading import Thread

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Create Kafka consumer for heartbeat logs
consumer_heartbeat = KafkaConsumer(
    'heartbeat',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Dictionary to track the last heartbeat time for each node
last_heartbeat_times = {}
heartbeat_threshold = 30  # Time in seconds

def monitor_heartbeats():
    """
    Monitors the heartbeat timestamps for each node and prints alerts if a node's heartbeat is overdue.
    """
    while True:
        current_time = time.time()
        for node_id, last_time in last_heartbeat_times.items():
            elapsed_time = current_time - last_time
            if elapsed_time > heartbeat_threshold:
                print(f"ALERT! No heartbeat received from node {node_id} for {int(elapsed_time)} seconds.")
        time.sleep(5)  # Check every 5 seconds

# Start the monitoring thread
Thread(target=monitor_heartbeats, daemon=True).start()

# Process heartbeats from Kafka
for message in consumer_heartbeat:
    heartbeat_data = message.value
    node_id = heartbeat_data.get('node_id')

    # Store heartbeat data in Elasticsearch
    es.index(index='heartbeat-logs', body=heartbeat_data)
    print(f"Heartbeat received: {heartbeat_data}")

    # Update the last heartbeat time for the node
    if node_id:
        last_heartbeat_times[node_id] = time.time()
