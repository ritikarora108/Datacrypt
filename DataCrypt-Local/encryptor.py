from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import ec
import os

def encrypt_file(file_path, public_key_str):
    """Encrypt file using ECDH for key exchange and AES for data encryption."""
    # Reconstruct PEM format from base64 key content
    public_key_pem = '-----BEGIN PUBLIC KEY-----\n' + '\n'.join([public_key_str[i:i+64] for i in range(0, len(public_key_str), 64)]) + '\n-----END PUBLIC KEY-----\n'
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    # Generate ephemeral private key
    ephemeral_private_key = ec.generate_private_key(ec.SECP384R1())
    shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)

    # Derive AES key
    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # Read file data
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Encrypt with AES (CBC)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Pad file data
    pad_len = 16 - (len(file_data) % 16)
    padded_data = file_data + bytes([pad_len] * pad_len)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Save ephemeral public key
    ephemeral_public_pem = (
        ephemeral_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    with open(file_path + ".key", "wb") as f:
        f.write(ephemeral_public_pem)

    # Save encrypted file
    with open(file_path + ".enc", "wb") as f:
        f.write(iv + encrypted_data)

    print("Encryption successful!")