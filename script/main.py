import os
import sys
from app import app
from consumer import consume_stream

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [api|consumer]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "api":
        # Start the Flask API; use FLASK_DEBUG=1 to enable debug mode (development only)
        debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
        app.run(host='127.0.0.1', port=5000, debug=debug_mode)
    elif command == "consumer":
        # Start the Kinesis consumer
        consume_stream('user-payment-events')  # Replace with your stream name
    else:
        print(f"Unknown command: {command}. Use 'api' or 'consumer'.")
        sys.exit(1)
