import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Use an absolute path for the keys directory
KEY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")

def generate_key_pair():
    """Generate an ECDH key pair and save them locally.

    Returns:
        bool: True if keys were generated, False if they already exist.
    """
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

    public_key_path = os.path.join(KEY_DIR, "public_key.pem")
    private_key_path = os.path.join(KEY_DIR, "private_key.pem")

    # Check if keys already exist
    if os.path.exists(public_key_path) and os.path.exists(private_key_path):
        print("Keys already exist. Skipping generation.")
        return False

    try:
        private_key = ec.generate_private_key(ec.SECP384R1())

        # Serialize and save private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        with open(private_key_path, "wb") as f:
            f.write(private_pem)

        # Generate and save public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        with open(public_key_path, "wb") as f:
            f.write(public_pem)

        print("[✅] ECDH key pair generated and saved.")
        return True

    except Exception as e:
        print(f"An error occurred during key generation: {e}")
        return False

if __name__ == "__main__":
    generate_key_pair()