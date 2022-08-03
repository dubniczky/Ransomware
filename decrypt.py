import os
import sys
import json
from cryptography.fernet import Fernet


def decrypt_files(files, key):
    fernet = Fernet(key)
    for file in files:
        f_in = file['in']
        f_out = file['out']
        try:
            with open(f_out, "rb") as f:
                data = f.read()
            data = fernet.decrypt(data)
            with open(f_in, "wb") as f:
                f.write(data)
            os.remove(f_out)
            print(f'Decrypted: {f_out} -> {f_in}')
        except Exception:
            print(f'Error decrypting: {f_out} -> {f_in}')
            pass


def load_encryption_logs(file):
    with open(file, 'r') as f:
        return json.load(f)


def main():
    if len(sys.argv) < 3:
        print('Usage: python3 decrypt.py <encrypt_log_path> <encryption_key>')
        sys.exit(1)

    log = load_encryption_logs(sys.argv[1])
    count = len(log)
    print(f'Loaded {count} files to decrypt')
    key = bytes(sys.argv[2], 'utf-8')

    decrypt_files(log, key)


if __name__ == '__main__':
    main()