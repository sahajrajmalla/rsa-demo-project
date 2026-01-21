import random
import hashlib

def is_prime(n, k=5):
    """
    Miller-Rabin primality test.
    Returns True if n is likely prime, False if composite.
    """
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """
    Generate a random prime number with specified bit length.
    """
    while True:
        # Generate random odd number
        p = random.getrandbits(bits)
        # Ensure it has the correct bit length and is odd
        p |= (1 << (bits - 1)) | 1
        
        if is_prime(p):
            return p

def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(e, phi):
    """
    Compute modular inverse of e modulo phi.
    Returns d such that (d * e) % phi == 1
    """
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

def generate_keypair(bits=1024):
    """
    Generates a public/private key pair.
    Returns ((e, n), (d, n), p, q, phi)
    """
    # 1. Generate p and q
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    # Ensure p != q
    while p == q:
        q = generate_prime(bits // 2)

    # 2. Compute n
    n = p * q

    # 3. Compute phi(n)
    phi = (p - 1) * (q - 1)

    # 4. Choose e
    # Common choice is 65537 (2^16 + 1)
    e = 65537
    
    # Ensure gcd(e, phi) == 1. If not, pick another e (rare for 65537 but good to check)
    # Or just regenerate p, q. For this demo, we'll just check.
    # If 65537 shares a factor, we can just increment or pick random odd.
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)

    # 5. Compute d
    d = mod_inverse(e, phi)

    # Return public and private key parts
    # Public: (e, n)
    # Private: (d, n)
    return ((e, n), (d, n), p, q, phi)

def encrypt_message(public_key, message):
    """
    Encrypts a string message using the public key.
    Returns a list of encrypted integers (one per character).
    """
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

def decrypt_message(private_key, ciphertext):
    """
    Decrypts a list of encrypted integers using the private key.
    Returns the plaintext string.
    """
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

def compute_hash(message):
    """Compute SHA-256 hash of message."""
    return hashlib.sha256(message.encode()).hexdigest()
