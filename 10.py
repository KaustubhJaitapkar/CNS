import random

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    g, x1, y1 = extended_gcd(b % a, a)
    
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, m):
    a = a % m 
    if a == 0:
        return None 
        
    g, x, y = extended_gcd(a, m)
    
    if g != 1:
        raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) = {g}")
    else:
        return x % m

def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1(message):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    message_bytes = message.encode('utf-8')
    bit_len = len(message_bytes) * 8
    
    message_bytes += b'\x80'
    while len(message_bytes) % 64 != 56:
        message_bytes += b'\x00'
    message_bytes += bit_len.to_bytes(8, 'big')
    
    for i in range(0, len(message_bytes), 64):
        w = [0] * 80
        chunk = message_bytes[i:i+64]
        
        for j in range(16):
            w[j] = int.from_bytes(chunk[j*4:(j+1)*4], 'big')
        
        for j in range(16, 80):
            w[j] = (left_rotate((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]), 1)) & 0xFFFFFFFF
        
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = (left_rotate(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
            
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        
    return h0

def generate_dsa_keys(p, q, g):
    x = random.randint(1, q-1)
    y = mod_pow(g, x, p)
    
    return (x), (p, q, g, y) 

def sign_message(message, private_key_x, p, q, g):
    h = sha1(message) % q 
    
    k = random.randint(1, q-1)
    
    r = (mod_pow(g, k, p)) % q
    
    if r == 0:
        return sign_message(message, private_key_x, p, q, g)
    
    k_inv = mod_inverse(k, q)
    
    s = (k_inv * (h + private_key_x * r)) % q
    
    if s == 0:
        return sign_message(message, private_key_x, p, q, g)
        
    return (r, s)

def verify_signature(message, signature, public_key_params):
    p, q, g, y = public_key_params
    r, s = signature
    
    if not (0 < r < q and 0 < s < q):
        return False
        
    h = sha1(message) % q
    
    s_inv = mod_inverse(s, q)
    
    u1 = (h * s_inv) % q
    u2 = (r * s_inv) % q
    
    g_u1 = mod_pow(g, u1, p)
    y_u2 = mod_pow(y, u2, p)
    
    v = ((g_u1 * y_u2) % p) % q
    
    return v == r

if __name__ == "__main__":
    P_DEMO = 23
    Q_DEMO = 11
    G_DEMO = 5

    try:
        private_key_x, public_key_params = generate_dsa_keys(P_DEMO, Q_DEMO, G_DEMO)
        print(f"--- DSA Key Generation (p={P_DEMO}, q={Q_DEMO}, g={G_DEMO}) ---")
        print(f"Private Key (x): {private_key_x}")
        print(f"Public Key (y):  {public_key_params[3]}")
        print("-" * 50)

        MESSAGE = "Hello CNS Lab"
        signature = sign_message(MESSAGE, private_key_x, P_DEMO, Q_DEMO, G_DEMO)
        print(f"Signing Message: '{MESSAGE}'")
        print(f"Signature (r, s): {signature}")
        print("-" * 50)

        valid = verify_signature(MESSAGE, signature, public_key_params)
        print(f"Verification Result (Correct Message): {valid}") 

        TAMPERED_MESSAGE = "Hella CNS Lab"
        tampered_valid = verify_signature(TAMPERED_MESSAGE, signature, public_key_params)
        print(f"Verification Result (Tampered Message '{TAMPERED_MESSAGE}'): {tampered_valid}")
        
    except ValueError as e:
        print(f"ERROR: {e}. Please check your math parameters (p, q, g).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
