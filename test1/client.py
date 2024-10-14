import h2.connection
import socket

# Establish a TCP connection
sock = socket.create_connection(('localhost', 7700), timeout=10)
conn = h2.connection.H2Connection()

# Initialize the HTTP/2 connection
conn.initiate_connection()
sock.sendall(conn.data_to_send())

# Create a non-conformant HTTP/2 request
headers = [
    (':method', 'GET'),
    (':authority', 'localhost'),
    (':scheme', 'http'),
    (':path', '/'),
    ('connection', 'keep-alive')  # Non-conformant header
]

# Send headers frame
conn.send_headers(1, headers)
sock.sendall(conn.data_to_send())

# Close the connection
conn.close_connection()
sock.sendall(conn.data_to_send())
sock.close()