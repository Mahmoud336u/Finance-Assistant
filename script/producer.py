import boto3
import json

# Initialize Kinesis client
kinesis = boto3.client('kinesis')

def produce_record(stream_name, data):
    """Send a record to a Kinesis stream."""
    try:
        response = kinesis.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey='partition-key'  # Adjust based on your partitioning strategy
        )
        print(f"Record sent: {response['SequenceNumber']}")
        return response
    except Exception as e:
        print(f"Error producing record: {e}")
        return None

if __name__ == "__main__":
    stream_name = 'user-payment-events'  # Replace with your Kinesis stream name
    # Example data (e.g., a payment event)
    sample_data = {
        'user_id': '123',
        'amount': 100.0,
        'timestamp': '2023-01-01T00:00:00Z'
    }
    produce_record(stream_name, sample_data)
