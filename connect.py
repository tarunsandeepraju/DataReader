from kafka import KafkaConsumer, KafkaProducer
from redis import StrictRedis
import json

# Connect to Redis
redis_client = StrictRedis(
    host='redis.finvedic.in',
    port=6379,
    db=0
)

# Set up Kafka Producer and Consumer
kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
kafka_consumer = KafkaConsumer(
    'market_data',
    bootstrap_servers='pkc-w77k7w.centralus.azure.confluent.cloud:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def run_microservice():
    for message in kafka_consumer:
        data = message.value
        print(f"Received data: {data}")
        # Process data and interact with Redis if needed
        redis_client.set('some_key', json.dumps(data))

if __name__ == "__mai_n_":
    run_microservice()