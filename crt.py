def extended_gcd(a, b):

    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def mod_inverse(a, m):

    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m} (gcd={g})")
    return x % m

def chinese_remainder_ext(a, n):

    # Product of all moduli
    N = 1
    for ni in n:
        N *= ni

    total = 0
    for ai, ni in zip(a, n):
        Ni = N // ni                 # Partial product
        Mi = mod_inverse(Ni, ni)     # Inverse via extended Euclid
        total += ai * Ni * Mi

    return total % N

# ---------- Example usage ----------
a = [2, 3, 2]  # remainders
n = [3, 4, 5]  # moduli

print("Given system of congruences:")
for ai, ni in zip(a, n):
    print(f"x ≡ {ai} (mod {ni})")

x = chinese_remainder_ext(a, n)
print("\nSolution: x =", x)
