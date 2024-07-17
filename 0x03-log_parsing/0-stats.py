#!/usr/bin/python3
import sys
import signal

# Initialize variables to keep track of metrics
total_size = 0
status_count = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

def print_metrics():
    """Print the metrics gathered so far."""
    print(f"File size: {total_size}")
    for status in sorted(status_count):
        if status_count[status] > 0:
            print(f"{status}: {status_count[status]}")

def signal_handler(sig, frame):
    """Handle keyboard interruption signal (CTRL + C) to print metrics."""
    print_metrics()
    sys.exit(0)

# Set up signal handler for keyboard interruption (CTRL + C)
signal.signal(signal.SIGINT, signal_handler)

# Process each line from stdin
for line in sys.stdin:
    try:
        parts = line.split()
        if len(parts) < 9:
            continue
        ip_address = parts[0]
        date = parts[3] + " " + parts[4]
        request = parts[5] + " " + parts[6] + " " + parts[7]
        status_code = int(parts[8])
        file_size = int(parts[9])

        # Update total file size
        total_size += file_size

        # Update status count
        if status_code in status_count:
            status_count[status_code] += 1

        # Update line count
        line_count += 1

        # Print metrics every 10 lines
        if line_count % 10 == 0:
            print_metrics()
    except (ValueError, IndexError):
        continue

# Print remaining metrics after the loop ends
print_metrics()
