import sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PRIVATE_PATH = 'keys/private.key'
PUBLIC_PATH = 'keys/public.key'

if len(sys.argv) > 2:
    PRIVATE_PATH = sys.argv[1]
    PUBLIC_PATH = sys.argv[2]

# Private key
private = rsa.generate_private_key(65537, 2048)
private_pem = private.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

with open(PRIVATE_PATH, 'wb') as f:
    f.write(private_pem)


# Public key
public = private.public_key()
public_pem = public.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(PUBLIC_PATH, 'wb') as f:
    f.write(public_pem)
