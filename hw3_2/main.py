import random
from phe import paillier
import numpy as np


class Person:
    def __init__(self, bits):
        self.pk, self.sk = paillier.generate_paillier_keypair(None, bits)

    def encrypt(self, m):
        return self.pk.encrypt(m)

    def decrypt(self, c):
        return self.sk.decrypt(c)


for i in range(2):
    if i == 0:
        bits = 512
    else:
        bits = 1024
    # Create Alice with her own public and secret keys
    Alice = Person(bits)
    # Create Bob with her own public and secret keys
    Bob = Person(bits)

    # Alice generates her message
    A = []
    for i in range(5):
        tmp = []
        for j in range(8):
            tmp.append(random.randint(0, 10000))
        A.append(tmp)

    # Alice encrypts her message with her own public key and sends encrypted message to Bob
    A_encrypted = []
    for i in range(5):
        tmp = []
        for j in range(8):
            tmp.append(Alice.encrypt(A[i][j]))
        A_encrypted.append(tmp)

    # Bob generates his message
    B = []
    for i in range(8):
        tmp = []
        for j in range(4):
            tmp.append(random.randint(0, 100000))
        B.append(tmp)

    # Bob computes the dot product with Alice's cipher-texts and his plain-texts. Bob sends result to Alice.
    alice_cipher = np.array(A_encrypted)
    bob_plain = np.array(B)
    result_encrypted = alice_cipher @ bob_plain
    result_encrypted = np.ndarray.tolist(result_encrypted)

    # Alice decrypts Bob's result. Now Alice has the final result.
    Alice_result = []
    for i in range(5):
        tmp = []
        for j in range(4):
            tmp.append(Alice.decrypt(result_encrypted[i][j]))
        Alice_result.append(tmp)

    # Alice encrypts the final result with Bob's public key and sends the encrypted data to Bob.
    Alice_result_encrypted = []
    for i in range(5):
        tmp = []
        for j in range(4):
            tmp.append(Bob.encrypt(Alice_result[i][j]))
        Alice_result_encrypted.append(tmp)

    # Convert Alice_result_encrypted from paillier.EncryptedNumber objects to ciphertexts for printing
    final_ciphertexts = []
    for i in range(5):
        tmp = []
        for j in range(4):
            tmp.append(Alice_result_encrypted[i][j].ciphertext())
        final_ciphertexts.append(tmp)

    # Bob decrypts the final cipher-text, yielding the final result.
    Bob_result = []
    for i in range(5):
        tmp = []
        for j in range(4):
            tmp.append(Bob.decrypt(Alice_result_encrypted[i][j]))
        Bob_result.append(tmp)

    print(f"bits: {bits}")
    print("A:")
    print(np.array(A))
    print("B:")
    print(np.array(B))
    print("Last ciphertext before decryption:")
    print(np.array(final_ciphertexts))
    print("Expected A @ B:")
    print(np.array(A) @ np.array(B))
    print("Alice's Result:")
    print(np.array(Alice_result))
    print("Bob's Result:")
    print(np.array(Bob_result))
    print()

