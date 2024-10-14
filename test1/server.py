import h2.connection
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 7700))
sock.listen(5)

conn, addr = sock.accept()
h2_conn = h2.connection.H2Connection(config=h2.config.H2Configuration(client_side=False))
h2_conn.initiate_connection()

# Receive and process data
data = conn.recv(65535)
events = h2_conn.receive_data(data)

# Check if the non-conformant header was received
for event in events:
    if isinstance(event, h2.events.RequestReceived):
        print("Received headers:", event.headers)  # Check for the 'connection' header

conn.close()
sock.close()
