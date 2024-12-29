from flask import Flask, request, jsonify
import subprocess
import redis
from kafka import KafkaAdminClient

app = Flask(__name__)

# Configure Redis
redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0
)

# Configure Kafka
kafka_admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')


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