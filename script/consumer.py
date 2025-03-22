import boto3
import json
import time

# Initialize Kinesis client
kinesis = boto3.client('kinesis')

def consume_stream(stream_name):
    """Consume and process records from a Kinesis stream."""
    try:
        # Get shard iterator for the first shard (simplified for one shard)
        response = kinesis.describe_stream(StreamName=stream_name)
        shard_id = response['StreamDescription']['Shards'][0]['ShardId']
        shard_iterator = kinesis.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'  # Start from the oldest record
        )['ShardIterator']

        # Continuously read records from the stream
        while True:
            response = kinesis.get_records(ShardIterator=shard_iterator, Limit=100)
            records = response['Records']
            for record in records:
                data = json.loads(record['Data'].decode('utf-8'))
                process_record(data)
            shard_iterator = response['NextShardIterator']
            time.sleep(1)  # Avoid overwhelming the stream
    except Exception as e:
        print(f"Error in consumer: {e}")

def process_record(data):
    """Process a single record from the Kinesis stream."""
    # Example processing logic (e.g., store in DynamoDB or S3)
    print(f"Processed record: {data}")
    # Add your logic here, e.g., save to DynamoDB:
    # dynamodb.put_item(TableName='Payments', Item=data)

if __name__ == "__main__":
    stream_name = 'user-payment-events'  # Replace with your Kinesis stream name
    consume_stream(stream_name)
