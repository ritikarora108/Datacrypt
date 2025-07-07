# DataCrypt - Secure File Encryption & Transfer System

A comprehensive end-to-end encrypted file storage and transfer solution with both local encryption capabilities and secure cloud-based file sharing.

## 🏗️ Project Architecture

DataCrypt consists of two main components:

1. **DataCrypt-Local**: A PyQt6-based desktop application for local file encryption/decryption
2. **DataCrypt-Remote**: A full-stack web application for secure file transfer between users

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DataCrypt     │    │   DataCrypt     │    │   DataCrypt     │
│     Local       │    │     Remote      │    │     Remote      │
│   (Desktop)     │    │   (Frontend)    │    │   (Backend)     │
│                 │    │                 │    │                 │
│ • File Encrypt  │    │ • React/TS      │    │ • Node.js/Express│
│ • File Decrypt  │    │ • File Upload   │    │ • MongoDB       │
│ • Key Management│    │ • User Auth     │    │ • AWS S3        │
│ • PyQt6 UI      │    │ • Real-time     │    │ • Socket.IO     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔐 Security Features

- **ECDH Key Exchange**: Elliptic Curve Diffie-Hellman for secure key generation
- **AES-256 Encryption**: Advanced Encryption Standard for file encryption
- **End-to-End Encryption**: Files are encrypted client-side before upload
- **Public Key Infrastructure**: Users have public/private key pairs
- **Secure File Transfer**: Encrypted files stored in AWS S3 with signed URLs
- **Two-Factor Authentication**: TOTP-based email verification
- **JWT Authentication**: Secure session management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (for Local component)
- Node.js 18+ (for Remote component)
- MongoDB database
- AWS S3 bucket
- SMTP email service

### Local Component Setup

```bash
cd DataCrypt-Local
pip install -r requirements.txt
python main.py
```

### Remote Component Setup

```bash
cd DataCrypt-Remote

# Install frontend dependencies
npm install

# Install backend dependencies
cd server
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development servers
npm run dev:both
```

## 📁 Project Structure

```
Datacrypt-final-year-project/
├── DataCrypt-Local/           # Desktop encryption application
│   ├── main.py               # Application entry point
│   ├── ui.py                 # PyQt6 user interface
│   ├── encryptor.py          # File encryption logic
│   ├── decryptor.py          # File decryption logic
│   ├── key_manager.py        # Key pair generation
│   └── requirements.txt      # Python dependencies
│
└── DataCrypt-Remote/         # Web-based file transfer system
    ├── src/                  # React frontend
    │   ├── components/       # React components
    │   ├── pages/           # Page components
    │   ├── contexts/        # React contexts
    │   └── utils/           # Utility functions
    ├── server/              # Node.js backend
    │   ├── routes/          # API routes
    │   ├── models/          # MongoDB schemas
    │   ├── middleware/      # Express middleware
    │   └── utils/           # Backend utilities
    └── package.json         # Frontend dependencies
```

## 🔧 Configuration

### Environment Variables (Remote Component)

Create a `.env` file in the `DataCrypt-Remote/server/` directory:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/datacrypt

# JWT
JWT_SECRET=your-secret-key

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket-name

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Client URL
CLIENT_URL=http://localhost:5173
```

## 📖 Usage

### Local Component

1. **Generate Keys**: Click "Generate Keys" to create your ECDH key pair
2. **Select File**: Choose a file to encrypt or decrypt
3. **Encrypt**: Click "Encrypt File" to encrypt with a recipient's public key
4. **Decrypt**: Click "Decrypt File" to decrypt with your private key

### Remote Component

1. **Register**: Create an account with email verification
2. **Upload**: Select encrypted file and key, specify recipient
3. **Share**: Recipient receives email notification with download link
4. **Download**: Recipient downloads and decrypts files locally

## 🔒 Security Architecture

```
User A (Sender)                    User B (Recipient)
     │                                   │
     │ 1. Generate ECDH key pair         │ 1. Generate ECDH key pair
     │ 2. Share public key               │ 2. Share public key
     │                                   │
     │ 3. Encrypt file with User B's     │
     │    public key                     │
     │ 4. Upload encrypted file to S3    │
     │ 5. Send notification email        │
     │                                   │ 6. Receive email notification
     │                                   │ 7. Download encrypted file
     │                                   │ 8. Decrypt with private key
```

## 🛠️ Development

### Local Development

```bash
# Frontend (React + TypeScript)
cd DataCrypt-Remote
npm run dev

# Backend (Node.js + Express)
cd DataCrypt-Remote/server
npm run dev

# Both simultaneously
npm run dev:both
```

### Building for Production

```bash
# Frontend build
npm run build

# Backend deployment
npm start
```

## 📊 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/verify-otp` - Email verification
- `POST /api/auth/send-otp` - Send login OTP

### File Transfer Endpoints

- `POST /api/transfers/upload` - Upload encrypted file
- `GET /api/transfers/inbox` - Get received files
- `GET /api/transfers/sent` - Get sent files
- `GET /api/transfers/file/:token` - Download file

### User Management Endpoints

- `GET /api/users/public-key/:email` - Get user's public key
- `POST /api/invite/send` - Send invitation email

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation in each component's README
- Review the architecture diagrams in the `docs/` folder

## 🔄 Version History

- **v1.0.0**: Initial release with local encryption and remote file transfer
- Features: ECDH key exchange, AES encryption, secure file sharing, real-time notifications
