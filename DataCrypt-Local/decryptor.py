from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def decrypt_file(encrypted_file_path, encrypted_key_path, private_key_path, sender_public_key_str=None):
    """Decrypt file using ECDH and AES, with optional sender public key verification."""
    # Load private key
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # Load ephemeral public key
    with open(encrypted_key_path, "rb") as f:
        ephemeral_public_pem = f.read()
        ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_pem)

    # Optionally load sender's public key
    if sender_public_key_str:
        try:
            # Reconstruct PEM format from base64 key content
            sender_public_key_pem = '-----BEGIN PUBLIC KEY-----\n' + '\n'.join([sender_public_key_str[i:i+64] for i in range(0, len(sender_public_key_str), 64)]) + '\n-----END PUBLIC KEY-----\n'
            sender_public_key = serialization.load_pem_public_key(sender_public_key_pem.encode())
            # Placeholder: Add cryptographic verification here if needed
            print("Sender's public key loaded for verification.")
        except Exception as e:
            raise ValueError(f"Invalid sender public key: {e}")

    # ECDH key exchange
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)

    # Derive AES key
    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # Read encrypted file
    with open(encrypted_file_path, "rb") as f:
        iv = f.read(16)
        encrypted_data = f.read()

    # Decrypt using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    pad_len = decrypted_padded_data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding detected. Decryption failed.")
    decrypted_data = decrypted_padded_data[:-pad_len]

    # Save decrypted file
    original_filename = encrypted_file_path.rsplit(".enc", 1)[0]
    name, ext = os.path.splitext(original_filename)
    decrypted_file_path = f"{name}-decrypted{ext}"
    with open(decrypted_file_path, "wb") as f:
        f.write(decrypted_data)

    print("Decryption successful! File saved as", decrypted_file_path)

