import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load params
if len(sys.argv) < 3:
    print('Usage: python3 unlock.py <private_key_path> <encrypted_key>')
    sys.exit(1)
key_file = sys.argv[1]
enc_key = sys.argv[2]

# Load private key
private = None
with open(key_file, 'rb') as f:
    private = serialization.load_pem_private_key(f.read(), None)

# Load encrypted key
enc_key = bytes.fromhex(enc_key)

# Decrypt
key = private.decrypt(
    enc_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(str(key, 'utf-8'))
