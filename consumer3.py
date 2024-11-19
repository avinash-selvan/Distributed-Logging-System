from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Create Kafka consumer for alert logs
consumer_alerts = KafkaConsumer(
    'alert',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer_alerts:
    alert_data = message.value
    # Store alert data in Elasticsearch
    es.index(index='alert-logs', body=alert_data)
    print(f"Alert received: {alert_data}")

    # Trigger alert response if needed
    if alert_data.get('log_level') == 'CRITICAL':
        # Custom alert action, e.g., send an email, trigger a webhook, etc.
        print("CRITICAL ALERT! Immediate attention required.")
