# S-DES Implementation

def permute(bits, table):
    """Permute bits according to the given table."""
    return [bits[i - 1] for i in table]

def left_shift(bits, shifts):
    """Left shift the bits by the specified number of shifts."""
    return bits[shifts:] + bits[:shifts]

def generate_keys(key):
    """Generate two subkeys from the original key."""
    key = permute(key, [2, 6, 3, 1, 4, 8, 5, 7])  # P10 permutation
    left = key[:5]
    right = key[5:]

    # Generate K1
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    K1 = permute(left + right, [3, 6, 4, 8, 5, 7, 9, 10])  # P8 permutation

    # Generate K2
    left = left_shift(left, 2)
    right = left_shift(right, 2)
    K2 = permute(left + right, [3, 6, 4, 8, 5, 7, 9, 10])  # P8 permutation

    return K1, K2

def fk(subkey, bits):
    """Feistel function."""
    left = bits[:4]
    right = bits[4:]

    # Expansion/Permutation (E/P)
    right_expanded = permute(right, [4, 1, 2, 3])  
    xor_result = [right_expanded[i] ^ subkey[i] for i in range(4)]

    # S-Boxes
    s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

    row_s0 = (xor_result[0] << 1) | xor_result[3]
    col_s0 = (xor_result[1] << 1) | xor_result[2]
    
    row_s1 = (xor_result[2] << 1) | xor_result[3]
    col_s1 = (xor_result[0] << 1) | xor_result[1]

    sbox_output = []
    
    # S-Box lookups
    sbox_output += list(map(int,
        format(s0[row_s0][col_s0], '02b')))
    
    sbox_output += list(map(int,
        format(s1[row_s1][col_s1], '02b')))

    # P4 permutation
    return permute(sbox_output[:4], [2, 4, 3, 1])

def encrypt(plaintext_bits):
    """Encrypt the plaintext using S-DES."""
    key = [int(x) for x in '1010000010'] # Example key
    K1, K2 = generate_keys(key)

    # Initial Permutation (IP)
    bits = permute(plaintext_bits,
                   [2,6,3,1,
                    4,8,5,7])

    # Round Function
    bits = fk(K1,bits)
    
    # Swap halves
    bits = bits[4:] + bits[:4]

    # Second round with K2
    bits = fk(K2,bits)

    # Final Permutation (FP)
    ciphertext_bits = permute(bits,
                               [4 ,1 ,3 ,5 ,
                                7 ,2 ,8 ,6])
    
    return ciphertext_bits

def decrypt(ciphertext_bits):
    """Decrypt the ciphertext using S-DES."""
    key = [int(x) for x in '1010000010'] # Example key
    K1,K2=generate_keys(key)

   # Initial Permutation (IP)
   bits=permute(ciphertext_bits,[2 ,6 ,3 ,1 ,4 ,8 ,5 ,7])

   # Round Function with K2 first
   bits=fk(K2,bits)

   # Swap halves
   bits=bits[4:]+bits[:4]

   # Second round with K1
   bits=fk(K1,bits)

   # Final Permutation (FP)
   plaintext_bits=permute(bits,[4 ,1 ,3 ,5 ,7 ,2 ,8 ,6])
   
   return plaintext_bits

# Example usage:
if __name__ == "__main__":
   plaintext='10101010'     # Example plaintext
   plaintext_bits=[int(x) for x in plaintext]
   
   print("Plaintext:", plaintext)
   
   ciphertext=encrypt(plaintext_bits)
   print("Ciphertext:", ''.join(map(str,ciphertext)))
   
   decrypted_text=decrypt(ciphertext)
   print("Decrypted Text:", ''.join(map(str,decrypted_text)))
