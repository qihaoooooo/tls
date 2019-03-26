import socket
import ssl

IP_ADDR, TLS_PORT = "localhost", 1002
ROOT_CA_PATH = "certs/root_ca.crt"
CERT_PATH = "certs/server_cert.crt"
CERT_KEY_PATH = "certs/server_cert.key"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=CERT_PATH, keyfile=CERT_KEY_PATH)
context.load_verify_locations(cafile=ROOT_CA_PATH)

bsock = socket.socket()
# Bind socket and wait for connection
bsock.bind((IP_ADDR, TLS_PORT))
bsock.listen(5)

def main():

    print("TLS Server started on {}:{}".format(IP_ADDR, TLS_PORT))

    while True:

        # Create server side TLS socket
        conn, addr = bsock.accept()
        tls_sock = context.wrap_socket(conn, server_side=True)

        try:
            data = tls_sock.recv(2048)
            # Received some packet
            if data:
                print("(TLS) Received data: {}".format(data.decode()))

                # echo data
                tls_sock.send(data)

                print("(TLS) Sending data...")

        finally:

            tls_sock.shutdown(socket.SHUT_RDWR)
            tls_sock.close()

if __name__ == "__main__":
    main()
