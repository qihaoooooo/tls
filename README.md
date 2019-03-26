## Certificate set-up

### Root CA generation

Generate a Root CA certificate with its private key:

```bash
openssl req \
    -newkey rsa:2048 -nodes -keyout root_ca.key \
    -new -x509 -nodes -days 365 -out root_ca.crt \
    -subj "/CN=Tressider"
```

If the message "unable to write 'random state'" appears, these commands will have to be run as root.

### Generating certificates

Generate a new certificate signing request:

```bash
# Set FQDN of broker (IP address or domain name)
export FQDN=192.168.8.160 # replace as appropriate

# Create server CSR
openssl req \
    -newkey rsa:2048 -nodes -keyout server_cert.key \
    -out server_cert.csr \
    -subj "/CN=$FQDN"
    
# Create client CSR
openssl req \
    -newkey rsa:2048 -nodes -keyout client_cert.key \
    -out client_cert.csr \
    -subj "/CN=$FQDN"
```

Sign the request with the Root CA:

```bash
# Sign server CSR
openssl x509 -sha256 \
    -req -in server_cert.csr \
    -CA root_ca.crt \
    -CAkey root_ca.key \
    -CAcreateserial \
    -days 365 -out server_cert.crt
    
# Sign client CSR
openssl x509 -sha256 \
    -req -in client_cert.csr \
    -CA root_ca.crt \
    -CAkey root_ca.key \
    -CAcreateserial \
    -days 365 -out client_cert.crt
```

### Useful commands

Verify the certificate chain:

```bash
openssl verify -CAfile root_ca.crt server_cert.crt &&
openssl verify -CAfile root_ca.crt client_cert.crt
```

View the certificate:

```bash
openssl x509 -text -noout -in cert.crt
```

For convenience, run the `fcert.py` script to format the PEM file:

```bash
python3 cert-format.py root_ca.crt
```

Copy this output (**inclusive of the last \n**) to a `char[]`. This will be passed in as an argument in `TLSSocket::set_root_ca_cert()`.

## Configuring for MQTT

### mosquitto

The TLS configuration used by `mosquitto` is handled by the `mosquitto.conf` file. It is recommended you do not directly edit the original file.

Change the to be used to the recommended 8883:

```python
# Port to use for the default listener
port 8883
```

Set the certificates:

```python
# At least one of cafile or capath must be defined. They both
# define methods of accessing the PEM encoded Certificate
...
cafile path_to_cert/root_ca.crt

# Path to the PEM encoded server certificate.
certfile path_to_cert/server_cert.crt

# Path to the PEM encoded keyfile.
keyfile path_to_cert/server_cert.key
```

Start the broker with the configuration file (in this case `mosquitto_tls.conf`):

```bash
mosquitto -c mosquitto_tls.conf -v
```

### MQTT.fx

Under settings, enable SSL/TLS and select TLSv1.2 as the protocol.

Set the location of the CA Certificate file, but leave the CA certificate keystore empty.