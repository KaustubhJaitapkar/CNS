def left_rotate(n, b):
    """Performs a circular left bit rotation on a 32-bit integer."""
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1(message):
    """Calculates the SHA-1 message digest for the given input message."""
    
    # 1. Initialize Hash Registers (H0 to H4)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # --- 2. Padding ---
    
    message_bytes = message.encode('utf-8')
    bit_len = len(message_bytes) * 8
    
    # Append the mandatory '1' bit (0x80)
    message_bytes += b'\x80'
    
    # Append padding zeros until length is 56 bytes short of a multiple of 64
    while len(message_bytes) % 64 != 56:
        message_bytes += b'\x00'
        
    # Append the original message length (64 bits)
    message_bytes += bit_len.to_bytes(8, 'big')
    
    # --- 3. Processing Blocks (Compression Function) ---
    
    for i in range(0, len(message_bytes), 64):
        w = [0] * 80 # Word array for 80 rounds
        chunk = message_bytes[i:i+64]
        
        # Fill first 16 words (W0 to W15) from the current 512-bit chunk
        for j in range(16):
            w[j] = int.from_bytes(chunk[j*4:(j+1)*4], 'big')
        
        # Expand 16 words into 80 words (W16 to W79)
        for j in range(16, 80):
            w[j] = (left_rotate((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]), 1)) & 0xFFFFFFFF
        
        # Initialize working variables A, B, C, D, E
        a, b, c, d, e = h0, h1, h2, h3, h4
        
        # 80 Rounds of Mixing
        for j in range(80):
            # Define Logic Function (f) and Round Constant (k)
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else: # 60 <= j <= 79
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            # Core mixing step
            temp = (left_rotate(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            
            # Update working variables (Chain Reaction)
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
            
        # Update permanent Hash Registers
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        
    # --- 4. Final Output ---
    # Concatenate the five 32-bit registers (160 bits total)
    return f'{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}'


# --- Demonstration ---

if __name__ == "__main__":
    
    # 1. Accept input text
    print("--- SHA-1 Message Digest Calculation ---")
    message_original = input("Enter the input text (Message 1): ")
    
    # 2. Calculate and output SHA-1 digest
    digest1 = sha1(message_original)
    print("\n[Message 1]")
    print(f"Text: '{message_original}'")
    print(f"Digest: {digest1}")
    
    # 3. Demonstrate Avalanche Effect
    print("\n--- Demonstrating Data Integrity (Avalanche Effect) ---")
    
    # Attempt a small modification (e.g., changing case or adding a space)
    if message_original:
        # Simplest tamper: change case of first letter or add a period
        tampered_message = message_original + " " 
        
        digest2 = sha1(tampered_message)
        
        print("\n[Message 2 - Tampered]")
        print(f"Text: '{tampered_message}' (Original + Space)")
        print(f"Digest: {digest2}")
        
        print("\nVerification:")
        print(f"Original Digest Matches Tampered: {digest1 == digest2}")
        print("Conclusion: Even a single space causes the entire 160-bit digest to change.")
    else:
        print("Please enter text to demonstrate the avalanche effect.")