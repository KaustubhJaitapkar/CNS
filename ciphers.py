import numpy as np

# ------------------ 1. Caesar Cipher ------------------ #
def caesar_encrypt(text, key):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + key) % 26 + 65)
        else:
            result += char
    return result

def caesar_decrypt(cipher, key):
    return caesar_encrypt(cipher, -key)


# ------------------ 2. Playfair Cipher ------------------ #
def generate_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))  # remove duplicates, replace J with I
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = key + "".join([c for c in alphabet if c not in key])
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def format_text(text):
    text = text.upper().replace("J", "I")
    formatted = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            formatted += a + "X"
            i += 1
        else:
            formatted += a + b
            i += 2
    return formatted

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def playfair_encrypt(text, key):
    matrix = generate_matrix(key)
    text = format_text(text)
    cipher = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:  # same row
            cipher += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:  # same column
            cipher += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:  # rectangle
            cipher += matrix[row1][col2] + matrix[row2][col1]
    return cipher


# ------------------ 3. Hill Cipher ------------------ #
def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    while len(text) % len(key_matrix) != 0:
        text += "X"
    cipher = ""
    for i in range(0, len(text), len(key_matrix)):
        block = [ord(char) - 65 for char in text[i:i+len(key_matrix)]]
        block = np.dot(key_matrix, block) % 26
        cipher += "".join(chr(num + 65) for num in block)
    return cipher


# ------------------ 4. Vigenere Cipher ------------------ #
def vigenere_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    cipher = ""
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % len(key)]) - 65
            cipher += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            cipher += char
    return cipher

def vigenere_decrypt(cipher, key):
    text = ""
    key = key.upper()
    for i, char in enumerate(cipher):
        if char.isalpha():
            shift = ord(key[i % len(key)]) - 65
            text += chr((ord(char) - 65 - shift) % 26 + 65)
        else:
            text += char
    return text


# ------------------ Main (Testing) ------------------ #
if __name__ == "__main__":
    # Caesar
    text = "HELLO"
    caesar_key = 3
    caesar_enc = caesar_encrypt(text, caesar_key)
    caesar_dec = caesar_decrypt(caesar_enc, caesar_key)
    print("\n--- Caesar Cipher ---")
    print("Encrypted:", caesar_enc)
    print("Decrypted:", caesar_dec)

    # Playfair
    playfair_key = "KEYWORD"
    playfair_enc = playfair_encrypt("HELLO", playfair_key)
    print("\n--- Playfair Cipher ---")
    print("Encrypted:", playfair_enc)

    # Hill
    hill_key = np.array([[3, 3], [2, 5]])  # 2x2 matrix (invertible mod 26)
    hill_enc = hill_encrypt("HELLO", hill_key)
    print("\n--- Hill Cipher ---")
    print("Encrypted:", hill_enc)

    # Vigenere
    vigenere_key = "KEY"
    vigenere_enc = vigenere_encrypt("HELLO", vigenere_key)
    vigenere_dec = vigenere_decrypt(vigenere_enc, vigenere_key)
    print("\n--- Vigenere Cipher ---")
    print("Encrypted:", vigenere_enc)
    print("Decrypted:", vigenere_dec)
