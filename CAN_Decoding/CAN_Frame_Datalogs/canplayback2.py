"""
canplayback.py

This program reads a RealDash CAN log file and streams the CAN frames from log
to RealDash.

Usage:
- Start the canplayback program
$ python3 canplayback.py CSVFILE PORT [BAUD_RATE]

- Start RealDash and create 'RealDash CAN' connection
- Configure connection to IP address and port shown by the canplayback program
"""

import socket
import csv
import time
import sys

def get_next_line(csvfile):
    line = csvfile.readline()
    if not line:
        csvfile.seek(0)
        _ = csvfile.readline()
        line = csvfile.readline()

    return line

def send_next_frame(client, csvfile, baud_rate):
    line = get_next_line(csvfile)
    if line:
        values = next(csv.reader([line], delimiter=',', skipinitialspace=True))
        # index = values[0]
        # time = values[1]
        # channel = values[2]
        # direction = values[3]
        # frame_id = values[4]
        # frame_data = values[5]
        
        print("send:", values[4], values[5])
        frame_id = int(values[4], 0)
        client.sendall(bytes([0x44, 0x33, 0x22, 0x11]))
        client.sendall(frame_id.to_bytes(4, 'little'))
        
        frame_data = [int(value, 16) for value in values[5].split(' ') if value != 'x|']
        # Do not pad frames with zeros
        client.sendall(bytes(frame_data))
        
        # Compute bits per frame based on actual data length
        data_length = len(frame_data)
        # Estimate bits per frame: overhead + data bits
        bits_per_frame = 47 + (data_length * 8) + 20  # Adjusted for variable data length
        time_per_frame = bits_per_frame / baud_rate
        time.sleep(time_per_frame)

def main(filename, port, baud_rate):
    with open(filename) as csvfile:
        _ = csvfile.readline()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", port))
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.listen(2)
        print("Listening at", server.getsockname())

        try:
            while True:
                client, address = server.accept()
                print("Connected to", address)

                try:
                    while True:
                        send_next_frame(client, csvfile, baud_rate)
                except Exception as e:
                    print(e)
                    client.close()
                    csvfile.seek(0)
                    _ = csvfile.readline()

                print("Listening at", server.getsockname())
            
        except (KeyboardInterrupt, Exception):
            server.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 canplayback.py CSVFILE PORT [BAUD_RATE]")
        sys.exit(1)

    CSV_FILE = sys.argv[1]
    port = int(sys.argv[2])

    if len(sys.argv) > 3:
        baud_rate = int(sys.argv[3])
    else:
        baud_rate = 500000  # Default baud rate

    main(CSV_FILE, port, baud_rate)
