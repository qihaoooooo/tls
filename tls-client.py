import socket
import ssl
import pprint

HOSTNAME, TLS_PORT = "localhost", 1002
ROOT_CA_PATH = "certs/root_ca.crt"
CERT_PATH = "certs/client_cert.crt"
CERT_KEY_PATH = "certs/client_cert.key"

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_cert_chain(certfile=CERT_PATH, keyfile=CERT_KEY_PATH)
context.load_verify_locations(cafile=ROOT_CA_PATH)

def main():

    bsock = socket.socket()

    tls_sock = context.wrap_socket(bsock, server_hostname=HOSTNAME)
    tls_sock.connect((HOSTNAME, TLS_PORT))

    server_cert = tls_sock.getpeercert()
    if server_cert is not None:
        pprint.pprint(server_cert)
        print()
    else:
        print("No server certificate received")

    print("(TLS) Sending data...")
    tls_sock.send(b"TLS TEST")

    # Get echo
    data = tls_sock.recv(2048)
    if data:
        print("(TLS) Received data: {}".format(data.decode()))

if __name__ == "__main__":
    main()
