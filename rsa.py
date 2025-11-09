import random
import math

# --- Primality Testing (Miller-Rabin for Speed) ---

def mod_pow(base, exp, mod):
    """Computes (base^exp) % mod efficiently."""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def is_prime(n, k=20):
    """Probabilistic primality test (Miller-Rabin)."""
    if n <= 3:
        return n > 1
    if n % 2 == 0:
        return False
    
    # Write n as (2^r) * d + 1
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Witness Loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        composite = True
        for _ in range(r - 1):
            x = mod_pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def generate_prime(bits):
    """Generates a large prime number with the specified number of bits."""
    while True:
        # Generate a random odd number of the required size
        num = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(num):
            return num

# --- Extended Euclidean Algorithm ---

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """Calculates modular inverse (d) using Extended Euclidean Algorithm."""
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        # Inverse exists only if gcd(e, phi) = 1
        return None 
    # Ensure result is positive
    return x % phi

# --- RSA Core Functions ---

def generate_keys(key_size):
    """Generates RSA Public and Private Keys."""
    # Step 1: Generate two large primes, p and q
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    
    # Ensure they are distinct, though highly unlikely with large random numbers
    while p == q:
        q = generate_prime(key_size // 2)

    # Step 2: Calculate modulus n and Euler's Totient phi
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Step 3: Choose public exponent e
    e = 65537 # Common choice, small prime, efficient for encryption
    
    # Step 4: Calculate private exponent d
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    """Encrypts the integer plaintext C = M^e mod n."""
    e, n = public_key
    # pow(base, exp, mod) is Python's optimized modular exponentiation
    return pow(plaintext, e, n)

def decrypt(ciphertext, private_key):
    """Decrypts the integer ciphertext M = C^d mod n."""
    d, n = private_key
    return pow(ciphertext, d, n)

# --- Execution ---

if __name__ == "__main__":
    # NOTE: Using 32 bits for INSTANT DEMONSTRATION. 
    # Real-world security requires 2048+ bits.
    DEMO_KEY_SIZE = 32 
    MESSAGE = 123456789
    
    print(f"--- Generating {DEMO_KEY_SIZE}-bit RSA Keys (Fast Demo) ---")
    
    # Generate Keys
    public_key, private_key = generate_keys(DEMO_KEY_SIZE)
    
    # Encrypt
    encrypted = encrypt(MESSAGE, public_key)
    
    # Decrypt
    decrypted = decrypt(encrypted, private_key)
    
    print(f"Public Key (e, n): {public_key[0]}, {public_key[1]}")
    print(f"Private Key (d, n): {private_key[0]}, {private_key[1]}")
    print("-" * 40)
    print(f"Original Message: {MESSAGE}")
    print(f"Encrypted Ciphertext: {encrypted}")
    print(f"Decrypted Message: {decrypted}")
    print("-" * 40)
    print(f"Verification Success: {MESSAGE == decrypted}")