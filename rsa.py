import random
import math

def gcd(a, b):
    """Compute the greatest common divisor using Euclid's algorithm."""
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime_candidate(length):
    """Generate an odd prime candidate."""
    p = random.getrandbits(length)
    return p | (1 << length - 1) | 1  # Ensure it's odd and has the correct length

def generate_prime_number(length=8):
    """Generate a prime number of specified bit length."""
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def generate_keypair(bits):
    """Generate a public/private keypair."""
    p = generate_prime_number(bits)
    q = generate_prime_number(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)  # Modular inverse of e mod phi

    return ((e, n), (d, n))  # Public and private keys

def encrypt(public_key, plaintext):
    """Encrypt a message using the public key."""
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

def decrypt(private_key, ciphertext):
    """Decrypt a message using the private key."""
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext

# Example usage
if __name__ == "__main__":
    bits = 8  # For demonstration; use larger bits in production
    public_key, private_key = generate_keypair(bits)

    message = "HELLO"
    
    print("Original Message:", message)
    
    encrypted_msg = encrypt(public_key, message)
    print("Encrypted Message:", encrypted_msg)
    
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print("Decrypted Message:", decrypted_msg)
