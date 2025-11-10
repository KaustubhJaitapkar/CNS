from des import DesKey

def main():
    plaintext = input("Enter plaintext message: ")

    key_input = input("Enter 8-character key: ")
    if len(key_input) != 8:
        print("Key must be exactly 8 characters (64 bits).")
        return

    key = DesKey(key_input.encode())

    encrypted = key.encrypt(plaintext.encode(), padding=True)
    print("Encrypted (hex):", encrypted.hex())

    decrypted = key.decrypt(encrypted, padding=True).decode()
    print("Decrypted text:", decrypted)

if __name__ == "__main__":
    main()
