# DataCrypt Architecture Documentation

## 🏗️ System Overview

DataCrypt is a comprehensive end-to-end encrypted file storage and transfer system consisting of two main components that work together to provide secure file sharing capabilities.

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DataCrypt System                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐                    ┌─────────────────┐    │
│  │   DataCrypt     │                    │   DataCrypt     │    │
│  │     Local       │                    │     Remote      │    │
│  │   (Desktop)     │                    │   (Web App)     │    │
│  │                 │                    │                 │    │
│  │ • PyQt6 UI      │                    │ • React Frontend│    │
│  │ • ECDH Keys     │                    │ • Node.js API   │    │
│  │ • AES Encryption│                    │ • MongoDB DB    │    │
│  │ • File I/O      │                    │ • AWS S3 Storage│    │
│  └─────────────────┘                    └─────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

### 1. File Encryption Flow

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

### 2. Detailed Encryption Process

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Original      │    │   ECDH Key      │    │   Encrypted     │
│     File        │───►│   Exchange      │───►│     File        │
│                 │    │                 │    │                 │
│ • Any format    │    │ • Generate      │    │ • AES-256 CBC   │
│ • Any size      │    │   ephemeral key │    │ • Random IV     │
│ • Binary data   │    │ • Derive shared │    │ • PKCS7 padding │
└─────────────────┘    │   secret        │    └─────────────────┘
                       └─────────────────┘
```

## 🏛️ Component Architecture

### DataCrypt Local Component

```
┌─────────────────────────────────────────────────────────────┐
│                    DataCrypt Local                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │    UI.py    │    │  encryptor  │    │  decryptor  │     │
│  │  (PyQt6)    │◄──►│    .py      │◄──►│    .py      │     │
│  │             │    │             │    │             │     │
│  │ • File      │    │ • ECDH      │    │ • ECDH      │     │
│  │   Selection │    │ • AES       │    │ • AES       │     │
│  │ • Key       │    │ • File I/O  │    │ • File I/O  │     │
│  │   Display   │    │ • Key       │    │ • Key       │     │
│  │ • User      │    │   Derivation│    │   Derivation│     │
│  │   Actions   │    └─────────────┘    └─────────────┘     │
│  └─────────────┘                                         │
│           │                                               │
│           ▼                                               │
│  ┌─────────────┐                                          │
│  │ key_manager │                                          │
│  │    .py      │                                          │
│  │             │                                          │
│  │ • ECDH Key  │                                          │
│  │   Generation│                                          │
│  │ • Key       │                                          │
│  │   Storage   │                                          │
│  │ • PEM       │                                          │
│  │   Format    │                                          │
│  └─────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

### DataCrypt Remote Component

```
┌─────────────────────────────────────────────────────────────┐
│                   DataCrypt Remote                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐              ┌─────────────────┐      │
│  │   Frontend      │              │    Backend      │      │
│  │  (React/TS)     │◄────────────►│   (Node.js)     │      │
│  │                 │              │                 │      │
│  │ • File Upload   │              │ • API Routes    │      │
│  │ • User Auth     │              │ • Socket.IO     │      │
│  │ • Real-time UI  │              │ • File Storage  │      │
│  │ • Responsive    │              │ • Email Service │      │
│  └─────────────────┘              └─────────────────┘      │
│                                                             │
│  ┌─────────────────┐              ┌─────────────────┐      │
│  │   External      │              │   Database      │      │
│  │   Services      │              │   (MongoDB)     │      │
│  │                 │              │                 │      │
│  │ • AWS S3        │              │ • Users         │      │
│  │ • SMTP Email    │              │ • Transfers     │      │
│  │ • JWT Auth      │              │ • File Metadata │      │
│  └─────────────────┘              └─────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 🔐 Security Architecture

### Cryptographic Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layer                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   ECDH      │    │   AES-256   │    │   HKDF      │     │
│  │  Key Exchange│   │  Encryption │    │ Key Derivation│   │
│  │             │    │             │    │             │     │
│  │ • SECP384R1 │    │ • CBC Mode  │    │ • SHA-256   │     │
│  │ • Ephemeral │    │ • Random IV │    │ • Salt      │     │
│  │ • Perfect   │    │ • PKCS7     │    │ • Info      │     │
│  │   Forward   │    │   Padding   │    │ • Length    │     │
│  │   Secrecy   │    └─────────────┘    └─────────────┘     │
│  └─────────────┘                                         │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   JWT       │    │   bcrypt    │    │   TOTP      │     │
│  │  Tokens     │    │  Password   │    │  2FA Auth   │     │
│  │             │    │   Hashing   │    │             │     │
│  │ • Session   │    │ • Salt      │    │ • Time-based│     │
│  │   Management│    │ • Rounds    │    │ • Email     │     │
│  │ • Expiration│    │ • Secure    │    │   Delivery  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   Frontend  │    │   Backend   │
│  (Browser)  │    │  (React)    │    │  (Node.js)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       │ 1. Register       │                   │
       │──────────────────►│                   │
       │                   │ 2. POST /register │
       │                   │──────────────────►│
       │                   │                   │ 3. Hash Password
       │                   │                   │ 4. Generate OTP
       │                   │                   │ 5. Send Email
       │                   │ 6. Success        │
       │                   │◄──────────────────│
       │ 7. Verify Email   │                   │
       │──────────────────►│                   │
       │                   │ 8. POST /verify   │
       │                   │──────────────────►│
       │                   │                   │ 9. Verify OTP
       │                   │ 10. Success       │
       │                   │◄──────────────────│
       │ 11. Login         │                   │
       │──────────────────►│                   │
       │                   │ 12. POST /login   │
       │                   │──────────────────►│
       │                   │                   │ 13. Verify Credentials
       │                   │                   │ 14. Generate JWT
       │                   │ 15. JWT Token     │
       │                   │◄──────────────────│
       │ 16. Authenticated │                   │
       │◄──────────────────│                   │
```

## 📊 Database Schema

### User Model

```javascript
{
  _id: ObjectId,
  name: String (required),
  email: String (required, unique),
  password: String (hashed, required),
  publicKey: String (ECDH public key),
  otpSecret: String (TOTP secret),
  isVerified: Boolean (default: false),
  createdAt: Date (default: now)
}
```

### Transfer Model

```javascript
{
  _id: ObjectId,
  fileName: String (required),
  fileSize: Number (required),
  filePath: String (S3 key, required),
  encryptedKeyPath: String (S3 key, required),
  sender: ObjectId (ref: User, required),
  recipient: {
    email: String (required),
    userId: ObjectId (ref: User, optional)
  },
  accessToken: String (unique, required),
  downloaded: Boolean (default: false),
  expiresAt: Date (default: 7 days),
  createdAt: Date (default: now)
}
```

## 🔄 API Architecture

### RESTful Endpoints

```
Authentication:
├── POST /api/auth/register     # User registration
├── POST /api/auth/login        # User login
├── POST /api/auth/verify-otp   # Email verification
└── POST /api/auth/send-otp     # Send login OTP

File Transfer:
├── POST /api/transfers/upload  # Upload encrypted file
├── GET  /api/transfers/inbox   # Get received files
├── GET  /api/transfers/sent    # Get sent files
└── GET  /api/transfers/file/:token # Download file

User Management:
├── GET  /api/users/public-key/:email # Get public key
└── POST /api/invite/send       # Send invitation
```

### WebSocket Events

```
Client → Server:
├── join:room                    # Join user's notification room
└── leave:room                   # Leave user's notification room

Server → Client:
└── new-file:fileInfo            # New file notification
```

## 🏗️ Deployment Architecture

### Development Environment

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Vite Dev)    │◄──►│   (Node.js)     │◄──►│   (MongoDB)     │
│   localhost:5173│    │   localhost:5000│    │   localhost:27017│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Production Environment

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Vercel)      │◄──►│   (Railway)     │◄──►│   (MongoDB Atlas)│
│   https://...   │    │   https://...   │    │   mongodb+srv:// │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AWS S3        │
                       │   (File Storage)│
                       │   s3://bucket   │
                       └─────────────────┘
```

## 🔧 Technical Decisions

### Frontend Technology Stack

- **React 18**: Modern component-based UI library
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server
- **Socket.IO Client**: Real-time communication

### Backend Technology Stack

- **Node.js**: JavaScript runtime
- **Express.js**: Web application framework
- **MongoDB**: NoSQL database
- **Socket.IO**: Real-time bidirectional communication
- **JWT**: Stateless authentication

### Security Decisions

- **ECDH over RSA**: Better performance and smaller key sizes
- **AES-256**: Industry standard symmetric encryption
- **- **Rate Limiting**: Protection against abuse
  **: Secure key derivation function
- **bcrypt**: Secure password hashing
- **TOTP**: Time-based one-time passwords for 2FA

### Storage Decisions

- **AWS S3**: Scalable cloud storage for encrypted files
- **MongoDB**: Flexible document storage for metadata
- **Signed URLs**: Time-limited secure file access
- **Local Key Storage**: Private keys never leave user's device

## 📈 Scalability Considerations

### Horizontal Scaling

- **Stateless Backend**: JWT-based authentication enables horizontal scaling
- **Load Balancing**: Multiple backend instances can be deployed
- **CDN**: Static assets served via CDN
- **Database Sharding**: MongoDB supports horizontal scaling

### Performance Optimization

- **File Streaming**: Large files handled via streams
- **Caching**: Redis can be added for session caching
- **Compression**: Gzip compression for API responses
- **Lazy Loading**: Frontend components loaded on demand

## 🔍 Monitoring and Logging

### Application Monitoring

- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Response time monitoring
- **User Analytics**: Usage pattern tracking
- **Security Events**: Authentication and access logging

### Infrastructure Monitoring

- **Database Performance**: MongoDB query optimization
- **Storage Metrics**: S3 usage and performance
- **Network Latency**: API response times
- **Resource Utilization**: CPU, memory, and disk usage
