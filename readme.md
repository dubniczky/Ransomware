# Ransomware Demo

## Disclaimer

This python ransomware is for educational purposes for security engineers and analysts. Do not use for any purpose other than that and I am not responsible for your actions.

## Support ❤️

If you find the project useful, please consider supporting, or contributing.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dubniczky)

## Details

A ransomware is a type of malware that executes on a target's machine and encrypts files that it deems useful with a symmetric key. After encryption only the hackers have the option to recover the original files.

At this point, the hackers usually ask for money in the form of cryptocurrencies, gift cards, or other hard to trace means in exchange for the decryption keys.

A more complex ransomware system might have other components, like a way to spread to other devices on the network, or email itself to other people on the victim's contact list.

## Implementation

This implementation uses a `hybrid key` method. This means that the data is encrypted with a symmetric key, then the key is saved on the drive encrypted with a public key.  
Thanks to this, it's not not required to transmit the key to a remote server, instead the victim will be able to attach it to their payment, to which the hacker will (in some cases) send the original key as a response.

### Stages:

1. **Key generation**: the hacker generates an asymmetric key pair. They will then attack the public key to the payload script.
2. **Infection**: The hacker will find a way to infect a target computer. There are countless methods for this, but not important in our case.
3. **Encryption**: The infected machine will run the payload and have (presumably) all of it's important files encrypted and practically unusable.
4. **Extortion**: The hacker will display some message, informing the victim that their machine has been hijacked and the only way to recover the files is to pay the ransome and send the saved key.
5. **Decryption**: Given the victim pays the ransome, the hacker decrypts the key with their asymmetric private key and transmits the plain key to the victim, who is then able to decrypt all the files.

## Technical details

1. The hacker generates a `2048` bit asymmetric key pair. Attaches the public key to the payload and keeps the private key.
2. In the encryption step, a random key is generated, then, all files that match the pre-determined glob patterns are encrypted. The key is then encrypted with the public key in the payload and written to the storage device alongside a map of the enrypted files.
3. The encrypted key can then be decrypted with the private asymmetric key generated in step 1.
4. The data can then be decrypted using the decrypted random key generated in step 2.

The data is encrypted with a simple encryption library in python called Fernet. The key is encrypted with RSA.

## Usage

### Test run

Reset the demo project

```bash
make reset
```

Encrypt files, save key and map

```bash
make encrypt
```

Decrypt key with private key, then decrypt files

```bash
make decrypt
```

After the test run, the demo folder should look the same as it did before

### Detailed usage

1. Reset demo folder

```bash
make reset
```

2. Generate key pair

```bash
mkdir -p keys
python3 generate.py 'keys/private.key' 'keys/private.key'
```

3. Replace the contents of the `PUBLIC_KEY` variable inside `encrypt.py` with the generated public key in `keys/private.key`

4. Update `ENCRYPT_GLOBS` variable in `encrypt.py` to include any other globs, then run the encryption.

```bash
python3 encrypt.py
```

5. Decrypt the key saved in the local directory.

```bash
python3 unlock.py 'keys/private.key' $(cat secret.key)
```

6. Take the output of the previous command and use it to decrypt the files

```bash
python3 decrypt.py map.log DECYPTED_KEY
```

At this point you have successfully decrypted the files.

## Resources

Cryptography library documentation: [docs](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/)