import random

def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

p = 23
g = 5
a = random.randint(2, p-2)
b = random.randint(2, p-2)
A = mod_pow(g, a, p)
B = mod_pow(g, b, p)
shared_key_alice = mod_pow(B, a, p)
shared_key_bob = mod_pow(A, b, p)
print(f"Shared Key Alice: {shared_key_alice}, Shared Key Bob: {shared_key_bob}")    