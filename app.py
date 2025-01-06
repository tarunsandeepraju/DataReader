from flask import Flask, request, jsonify
import subprocess
import redis
from kafka import KafkaAdminClient

app = Flask(__name__)

# Configure Redis
redis_client = redis.StrictRedis(
    host='redis.finvedic.in',
    port=6379,
    db=0
)

# Configure Kafka
kafka_admin_client = KafkaAdminClient(bootstrap_servers='pkc-w77k7w.centralus.azure.confluent.cloud:9092')


@app.route('/start', methods=['POST'])
def start_services():
    try:
        print("Starting services...")
        # Start Microservice 1
        subprocess.Popen(['python', 'E:\Finvedic Hackathon\MarketDataSimulator/app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Start Microservice 2
        subprocess.Popen(['python', 'E:\Finvedic Hackathon\DataConsumer/app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Start Microservice 3
        subprocess.Popen(['python', 'E:\Finvedic Hackathon\DataConsumer/consumer.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Microservices started")
        return jsonify({"message": "Microservices started successfully!"}), 200
    except Exception as e:
        print(f"Error starting services: {e}")
        return jsonify({"error": str(e)}), 500



@app.route('/stop', methods=['POST'])
def stop_services():
    try:
        print("Stopping services...")
        subprocess.call(['taskkill', '/IM', 'python.exe', '/F'])
        return "Microservices stopped  successfully!"
    except Exception as e:
        print(f"Error stopping services: {e}")  # Debug
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,port=5001)

'''from flask import Flask, jsonify
from redis import StrictRedis

app = Flask(__name__)

# Connect to Redis
redis_client = StrictRedis(
    host='localhost',
    port=6379,
    db=0
)


@app.route('/data', methods=['GET'])
def get_data():
    # Retrieve all keys from the Redis hash 'my_hash'
    keys = redis_client.hkeys('my_hash')

    # Initialize a dictionary to store the retrieved data
    data = {}

    for key in keys:
        value = redis_client.hget('my_hash', key)
        # Decode the key and value from bytes to string
        data[key.decode('utf-8')] = value.decode('utf-8')

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(port=5003, debug=True)'''
