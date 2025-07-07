# DataCrypt Local - Desktop Encryption Application

A secure desktop application built with PyQt6 for local file encryption and decryption using ECDH key exchange and AES-256 encryption.

## 🔐 Features

- **ECDH Key Generation**: Generate secure elliptic curve key pairs
- **File Encryption**: Encrypt files with recipient's public key
- **File Decryption**: Decrypt files with your private key
- **Modern UI**: Clean, intuitive PyQt6 interface
- **Key Management**: Automatic key storage and retrieval
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd DataCrypt-Local
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### 1. Generate Key Pair

1. Launch the application
2. Click the **"🔑 Generate Keys"** button
3. Keys will be automatically generated and stored in the `keys/` directory
4. Your public key will be displayed and can be copied to share with others

### 2. Encrypt a File

1. Click **"📂 Select File"** to choose a file to encrypt
2. Ensure you have the recipient's public key (they should share it with you)
3. Click **"🔐 Encrypt File"**
4. The encrypted file will be saved as `filename.enc`
5. The ephemeral key will be saved as `filename.key`
6. Share both files with the recipient

### 3. Decrypt a File

1. Click **"📂 Select File"** to choose the encrypted file (`.enc` file)
2. Ensure you have the corresponding key file (`.key` file)
3. Ensure you have your private key in the `keys/` directory
4. Click **"🔓 Decrypt File"**
5. The decrypted file will be saved as `filename-decrypted.ext`

## 🔧 Technical Details

### Cryptographic Implementation

- **Key Exchange**: ECDH using SECP384R1 curve
- **Encryption**: AES-256 in CBC mode
- **Key Derivation**: HKDF with SHA-256
- **Padding**: PKCS7 padding for AES

### File Structure

```
DataCrypt-Local/
├── main.py              # Application entry point
├── ui.py                # PyQt6 user interface
├── encryptor.py         # File encryption logic
├── decryptor.py         # File decryption logic
├── key_manager.py       # Key pair generation and management
├── requirements.txt     # Python dependencies
├── logo.png            # Application logo
└── keys/               # Generated key pairs (created automatically)
    ├── public_key.pem   # Your public key
    └── private_key.pem  # Your private key (keep secure!)
```

### Key Management

Keys are stored in the `keys/` directory:

- `public_key.pem`: Your public key (safe to share)
- `private_key.pem`: Your private key (keep secure, never share)

**⚠️ Security Warning**: Never share your private key. Keep it secure and back it up safely.

## 🔒 Security Features

### ECDH Key Exchange

- Uses SECP384R1 elliptic curve
- Generates ephemeral keys for each encryption
- Provides perfect forward secrecy

### AES Encryption

- 256-bit AES encryption in CBC mode
- Random initialization vector (IV) for each encryption
- PKCS7 padding for variable-length data

### Key Derivation

- HKDF (HMAC-based Key Derivation Function)
- SHA-256 hash function
- Secure key derivation from shared secret

## 🛠️ Development

### Building from Source

1. **Install development dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run in development mode**
   ```bash
   python main.py
   ```

### Creating Executable

Use the provided batch file to create a standalone executable:

```bash
make_exe_no_console.bat
```

This creates a Windows executable without console window.

## 📋 Dependencies

- **PyQt6**: Modern Python bindings for Qt GUI framework
- **cryptography**: Cryptographic recipes and primitives
- **cffi**: C Foreign Function Interface
- **pycparser**: C parser in Python

## 🔍 Troubleshooting

### Common Issues

1. **"Keys already exist" message**

   - This is normal if you've already generated keys
   - Keys are stored in the `keys/` directory

2. **"Logo file not found" warning**

   - The application will still work without the logo
   - Ensure `logo.png` is in the same directory as `main.py`

3. **Decryption fails**

   - Ensure you have the correct `.key` file
   - Verify your private key is in the `keys/` directory
   - Check that the encrypted file is not corrupted

4. **Encryption fails**
   - Verify the recipient's public key is valid
   - Ensure the file is not locked by another application
   - Check available disk space

### Error Messages

- **"Invalid padding detected"**: The encrypted file may be corrupted
- **"Invalid sender public key"**: The public key format is incorrect
- **"File not found"**: Check the file path and permissions

## 🔄 Integration with Remote Component

This local application works seamlessly with the DataCrypt Remote component:

1. **Encrypt files locally** using this application
2. **Upload encrypted files** to the web platform
3. **Share with recipients** who can download and decrypt locally
4. **Maintain end-to-end encryption** throughout the process

## 📄 License

This component is part of the DataCrypt project and is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🆘 Support

For issues and questions:

- Check the troubleshooting section above
- Review the main project README
- Create an issue in the repository
