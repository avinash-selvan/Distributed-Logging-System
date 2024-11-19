#!/usr/bin/env python3

import time
import uuid
import json
import logging
from threading import Thread

# Setting up logging to separate files for different log types
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Handlers for different log types
log_handler = logging.FileHandler('./logs/microservices_logs.log')
heartbeat_handler = logging.FileHandler('./logs/heartbeat_logs.log')
alert_handler = logging.FileHandler('./logs/alert_logs.log')

log_handler.setLevel(logging.INFO)
heartbeat_handler.setLevel(logging.INFO)
alert_handler.setLevel(logging.WARNING)  # Alerts are typically warnings or higher

# Separate loggers for each type
log_logger = logging.getLogger('log_logger')
heartbeat_logger = logging.getLogger('heartbeat_logger')
alert_logger = logging.getLogger('alert_logger')

# Assign handlers to each logger
log_logger.addHandler(log_handler)
heartbeat_logger.addHandler(heartbeat_handler)
alert_logger.addHandler(alert_handler)

node_id = str(uuid.uuid4())
service_name = 'OrderService'

# Register the microservice
def register_service():
    registration_message = {
        "node_id": node_id,
        "message_type": "REGISTRATION",
        "service_name": service_name,
        "timestamp": int(time.time())
    }
    log_logger.info(json.dumps(registration_message))
    print(f"Registered {service_name} with node id {node_id}")

# Function to simulate service tasks and logs accordingly
def process_payment():
    while True:
        try:
            transaction_id = str(uuid.uuid4())
            response_time = int(time.time() % 500)
            threshold = 300 #this is for later simulating the warning log
            log_message = {
                "log_id": str(uuid.uuid4()),
                "node_id": node_id,
                "log_level": "INFO",
                "message_type": "LOG",
                "message": f"Processing Payment with transaction id : {transaction_id}",
                "service_name": service_name,
                "timestamp": int(time.time())
            }
            log_logger.info(json.dumps(log_message))
            print(f"INFO log sent for transaction ID {transaction_id}")

            if response_time > threshold:
                warn_log = {
                    "log_id": str(uuid.uuid4()),
                    "node_id": node_id,
                    "log_level": "WARN",
                    "message": "High response time detected",
                    "service_name": service_name,
                    "response_time_ms": response_time,
                    "threshold_limit_ms": threshold,
                    "timestamp": int(time.time())
                }
                alert_logger.warning(json.dumps(warn_log))

            # Simulate occasional errors in payment processing
            if int(time.time()) % 10 == 0:
                error_log = {
                    "log_id":str(uuid.uuid4()),
                    "node_id": node_id,
                    "log_level": "ERROR",
                    "message_type": "LOG",
                    "message": f"Error processing payment for transaction id : {transaction_id}",
                    "service_name": service_name,
                    "timestamp": int(time.time())
                }
                alert_logger.error(json.dumps(error_log))
                print("ERROR log sent for payment processing")

            # Simulate critical issues
            if int(time.time()) % 20 == 0:
                critical_log = {
                    "log_id": str(uuid.uuid4()),
                    "node_id": node_id,
                    "log_level": "CRITICAL",
                    "message_type": "LOG",
                    "message": "Database connection failure detected.",
                    "service_name": service_name,
                    "timestamp": int(time.time())
                }
                alert_logger.critical(json.dumps(critical_log))
                print("CRITICAL log sent for database failure")

            time.sleep(5)

        except Exception as e:
            error_log = {
                "log_id": str(uuid.uuid4()),
                "node_id": node_id,
                "log_level": "ERROR",
                "message_type": "LOG",
                "message": f"Unhandled exception: {str(e)}",
                "service_name": service_name,
                "timestamp": int(time.time())
            }
            alert_logger.error(json.dumps(error_log))
            print(f"Unhandled Exception logged: {e}")
            time.sleep(5)

# Heartbeat generator
def send_heartbeat():
    while True:
        heartbeat_message = {
            "node_id": node_id,
            "log_level": "HEARTBEAT",
            "message_type": "HEARTBEAT",
            "status": "UP",
            "timestamp": int(time.time())
        }
        heartbeat_logger.info(json.dumps(heartbeat_message))
        print("Heartbeat Sent")
        time.sleep(10)

if __name__ == "__main__":
    register_service()
    Thread(target=process_payment).start()
    Thread(target=send_heartbeat).start()
