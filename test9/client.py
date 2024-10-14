import h2.connection
import socket

# Establish a TCP connection
sock = socket.create_connection(('localhost', 8080), timeout=10)
conn = h2.connection.H2Connection()

# Initialize the HTTP/2 connection
conn.initiate_connection()
sock.sendall(conn.data_to_send())

# Send a request with the END_STREAM flag to close the stream
headers = [
    (':method', 'GET'),
    (':authority', 'localhost'),
    (':scheme', 'http'),
    (':path', '/')
]
conn.send_headers(1, headers, end_stream=True)  # This closes the stream
sock.sendall(conn.data_to_send())

# Now try to send another HEADERS frame on the closed stream (non-conformant)
new_headers = [
    (':method', 'POST'),
    (':authority', 'localhost'),
    (':scheme', 'http'),
    (':path', '/new')
]
conn.send_headers(1, new_headers)  # Sending on the closed stream
sock.sendall(conn.data_to_send())

# Close the connection
conn.close_connection()
sock.sendall(conn.data_to_send())
sock.close()