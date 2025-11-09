# Euclidean Algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Extended Euclidean Algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0  # gcd, x, y
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

# Modular Inverse using Extended Euclidean Algorithm
def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None  # No inverse if gcd != 1
    else:
        return x % m

# =============================
# Example Usage
# =============================
if __name__ == "__main__":
    a, b = 56, 15
    print("Euclidean Algorithm:")
    print(f"GCD({a}, {b}) =", gcd(a, b))

    a, m = 17, 43
    print("\nExtended Euclidean Algorithm:")
    g, x, y = extended_gcd(a, m)
    print(f"gcd({a}, {m}) = {g}")
    print(f"Bézout coefficients: x = {x}, y = {y}")
    print(f"Check: {a}*{x} + {m}*{y} = {a*x + m*y}")

    inv = mod_inverse(a, m)
    print(f"\nModular Inverse of {a} mod {m} = {inv}")
