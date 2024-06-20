import socket
import ssl

def create_ssl_connection():
    try:
        # Skapa en socket
        s = socket.socket()

        # Anslut till servern
        ai = socket.getaddrinfo("a2hf4qrddrew2u-ats.iot.eu-north-1.amazonaws.com", 443)
        addr = ai[0][-1]
        s.connect(addr)

        # Applicera SSL
        ss = ssl.wrap_socket(s)
        return ss
    except OSError as e:
        print("Error during SSL connection:", e)

# Använd funktionen i din kod
ssl_socket = create_ssl_connection()
if ssl_socket:
    print("SSL connection established successfully")
