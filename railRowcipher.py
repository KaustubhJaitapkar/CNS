# 1. Rail Fence Cipher
def rail_fence_encrypt(text, key):
    rail = [['\n' for i in range(len(text))]
            for j in range(key)]

    dir_down = False
    row, col = 0, 0

    for i in range(len(text)):
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        rail[row][col] = text[i]
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return ("".join(result))


def rail_fence_decrypt(cipher, key):
    rail = [['\n' for i in range(len(cipher))]
            for j in range(key)]

    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        rail[row][col] = '*'
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if (rail[i][j] == '*') and (index < len(cipher)):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        if (rail[row][col] != '*'):
            result.append(rail[row][col])
            col += 1

        if dir_down:
            row += 1
        else:
            row -= 1
    return ("".join(result))



# 2. Row & Column Transposition Cipher
import math


def row_column_encrypt(text, key):
    text = text.replace(" ", "").upper()
    col = len(key)
    row = math.ceil(len(text) / col)

    fill_null = int((row * col) - len(text))
    text += '_' * fill_null

    matrix = [list(text[i:i + col]) for i in range(0, len(text), col)]

    key_order = sorted(list(key))

    cipher = ""
    for k in key_order:
        col_idx = key.index(k)
        cipher += ''.join([row[col_idx] for row in matrix])
    return cipher


def row_column_decrypt(cipher, key):
    col = len(key)
    row = int(len(cipher) / col)

    key_order = sorted(list(key))

    matrix = [['' for _ in range(col)] for _ in range(row)]

    index = 0
    for k in key_order:
        col_idx = key.index(k)
        for r in range(row):
            matrix[r][col_idx] = cipher[index]
            index += 1

    text = ''.join([''.join(r) for r in matrix])
    return text.replace('_', '')


# Example Usage
if __name__ == "__main__":
    # Rail Fence Cipher Example
    message = "HELLO WORLD"
    key_rf = 3
    encrypted_rf = rail_fence_encrypt(message, key_rf)
    decrypted_rf = rail_fence_decrypt(encrypted_rf, key_rf)

    print("=== Rail Fence Cipher ===")
    print("Original Message:", message)
    print("Encrypted Message:", encrypted_rf)
    print("Decrypted Message:", decrypted_rf)

    # Row Column Cipher Example
    message2 = "WEAREDISCOVERED"
    key_rc = "4312567"
    encrypted_rc = row_column_encrypt(message2, key_rc)
    decrypted_rc = row_column_decrypt(encrypted_rc, key_rc)

    print("\n=== Row & Column Cipher ===")
    print("Original Message:", message2)
    print("Encrypted Message:", encrypted_rc)
    print("Decrypted Message:", decrypted_rc)
