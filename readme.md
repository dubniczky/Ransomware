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

