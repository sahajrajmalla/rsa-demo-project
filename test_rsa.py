import rsa_lib
import random

def test_rsa():
    print("Testing RSA Library...")
    
    # Test 1: Primality Test
    print("\n[1] Testing Primality Test...")
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101]
    composites = [4, 6, 8, 9, 10, 12, 14, 15, 21, 25, 27, 100]
    
    for p in primes:
        assert rsa_lib.is_prime(p), f"Failed: {p} should be prime"
    for c in composites:
        assert not rsa_lib.is_prime(c), f"Failed: {c} should be composite"
    print("    Passed!")

    # Test 2: Key Generation
    print("\n[2] Testing Key Generation (small bits)...")
    ((e, n), (d, n), p, q, phi) = rsa_lib.generate_keypair(bits=32)
    print(f"    p={p}, q={q}, n={n}, phi={phi}, e={e}, d={d}")
    
    assert p * q == n, "n != p * q"
    assert (p-1) * (q-1) == phi, "phi != (p-1)(q-1)"
    assert (e * d) % phi == 1, "(e * d) % phi != 1"
    print("    Passed!")

    # Test 3: Encryption/Decryption
    print("\n[3] Testing Encryption/Decryption...")
    message = "Hello World!"
    print(f"    Original: {message}")
    
    public_key = (e, n)
    private_key = (d, n)
    
    cipher = rsa_lib.encrypt_message(public_key, message)
    print(f"    Cipher: {cipher}")
    
    decrypted = rsa_lib.decrypt_message(private_key, cipher)
    print(f"    Decrypted: {decrypted}")
    
    assert message == decrypted, "Decryption failed!"
    print("    Passed!")
    
    print("\nAll Tests Passed Successfully!")

if __name__ == "__main__":
    test_rsa()
