from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PRIVATE_PATH = 'keys/private.key'
PUBLIC_PATH = 'keys/public.key'

private = rsa.generate_private_key(65537, 2048)
public = private.public_key()

pub_pem = public.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(PUBLIC_PATH, 'wb') as f:
    f.write(pub_pem)

prv_pem = private.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

with open(PRIVATE_PATH, 'wb') as f:
    f.write(prv_pem)