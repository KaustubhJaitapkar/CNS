import hashlib

def calculate_sha1(text):
    encoded_text = text.encode()
    sha1_hash = hashlib.sha1(encoded_text)
    return sha1_hash.hexdigest()

text = input("Enter text to hash: ")

digest = calculate_sha1(text)
print(f"\nOriginal Text: {text}")
print(f"SHA-1 Message Digest: {digest}")

modified_text = text + "!"
modified_digest = calculate_sha1(modified_text)

print("\nAfter modifying the input slightly:")
print(f"Modified Text: {modified_text}")
print(f"SHA-1 Message Digest: {modified_digest}")
