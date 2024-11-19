#!/usr/bin/env python3

from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Create Kafka consumer for general logs
consumer_logs = KafkaConsumer(
    'logs',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer_logs:
    log_data = message.value
    if log_data.get('log_level') not in ['ERROR', 'WARNING']:
        # Index the log in Elasticsearch
        es.index(index='microservice-logs', body=log_data)
        print(f"Indexed log in Elasticsearch: {log_data}")
