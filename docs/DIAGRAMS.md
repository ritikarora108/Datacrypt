# DataCrypt System Diagrams

## 🏗️ System Architecture Overview

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

### File Encryption and Transfer Flow

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

### Detailed Encryption Process

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

```
┌─────────────────────────────────────────────────────────────┐
│                        User Model                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │     _id     │    │    name     │    │    email    │     │
│  │  ObjectId   │    │   String    │    │   String    │     │
│  │  (Primary)  │    │ (Required)  │    │ (Required)  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  password   │    │ publicKey   │    │ otpSecret   │     │
│  │   String    │    │   String    │    │   String    │     │
│  │ (Hashed)    │    │ (ECDH Key)  │    │ (TOTP)      │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ isVerified  │    │ createdAt   │    │  updatedAt  │     │
│  │   Boolean   │    │    Date     │    │    Date     │     │
│  │ (Default: F)│    │ (Default)   │    │ (Auto)      │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Transfer Model

```
┌─────────────────────────────────────────────────────────────┐
│                     Transfer Model                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │     _id     │    │  fileName   │    │  fileSize   │     │
│  │  ObjectId   │    │   String    │    │   Number    │     │
│  │  (Primary)  │    │ (Required)  │    │ (Required)  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  filePath   │    │encryptedKey │    │   sender    │     │
│  │   String    │    │   Path      │    │  ObjectId   │     │
│  │ (S3 Key)    │    │   String    │    │ (Ref: User) │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ recipient   │    │accessToken  │    │ downloaded  │     │
│  │   Object    │    │   String    │    │   Boolean   │     │
│  │ {email, id} │    │ (Unique)    │    │ (Default:F) │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  expiresAt  │    │  createdAt  │    │  updatedAt  │     │
│  │    Date     │    │    Date     │    │    Date     │     │
│  │ (7 days)    │    │ (Default)   │    │ (Auto)      │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 API Architecture

### RESTful Endpoints

```
┌─────────────────────────────────────────────────────────────┐
│                     API Endpoints                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Authentication:                                            │
│  ├── POST /api/auth/register     # User registration       │
│  ├── POST /api/auth/login        # User login              │
│  ├── POST /api/auth/verify-otp   # Email verification      │
│  └── POST /api/auth/send-otp     # Send login OTP          │
│                                                             │
│  File Transfer:                                              │
│  ├── POST /api/transfers/upload  # Upload encrypted file   │
│  ├── GET  /api/transfers/inbox   # Get received files      │
│  ├── GET  /api/transfers/sent    # Get sent files          │
│  └── GET  /api/transfers/file/:token # Download file       │
│                                                             │
│  User Management:                                            │
│  ├── GET  /api/users/public-key/:email # Get public key    │
│  └── POST /api/invite/send       # Send invitation         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### WebSocket Events

```
┌─────────────────────────────────────────────────────────────┐
│                   WebSocket Events                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Client → Server:                                           │
│  ├── join:room                    # Join user's room       │
│  └── leave:room                   # Leave user's room      │
│                                                             │
│  Server → Client:                                           │
│  └── new-file:fileInfo            # New file notification  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
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

### Docker Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Frontend      │    │   Backend       │                │
│  │   Container     │◄──►│   Container     │                │
│  │   (Nginx)       │    │   (Node.js)     │                │
│  │   Port: 80      │    │   Port: 5000    │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   MongoDB       │    │   Docker        │                │
│  │   Container     │    │   Network       │                │
│  │   Port: 27017   │    │   (Internal)    │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Volume        │    │   Environment   │                │
│  │   (Data)        │    │   Variables     │                │
│  │   (Persistent)  │    │   (Config)      │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Technical Decisions

### Frontend Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                  Frontend Stack                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   React 18  │    │ TypeScript  │    │ Tailwind CSS│     │
│  │             │    │             │    │             │     │
│  │ • Components│    │ • Type Safe │    │ • Utility   │     │
│  │ • Hooks     │    │ • IntelliSense│  │   First     │     │
│  │ • Context   │    │ • Compile   │    │ • Responsive│     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │    Vite     │    │ Socket.IO   │    │   Axios     │     │
│  │             │    │   Client     │    │             │     │
│  │ • Fast Dev  │    │ • Real-time │    │ • HTTP      │     │
│  │ • HMR       │    │ • Events    │    │   Client    │     │
│  │ • Build     │    │ • Rooms     │    │ • Interceptors│   │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Backend Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                   Backend Stack                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Node.js   │    │  Express.js │    │  MongoDB    │     │
│  │             │    │             │    │             │     │
│  │ • Runtime   │    │ • Framework │    │ • Database  │     │
│  │ • Event Loop│    │ • Middleware│    │ • Document  │     │
│  │ • NPM       │    │ • Routing   │    │   Store     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Socket.IO  │    │   JWT       │    │   bcrypt    │     │
│  │             │    │             │    │             │     │
│  │ • Real-time │    │ • Auth      │    │ • Password  │     │
│  │ • WebSocket │    │ • Tokens    │    │   Hashing   │     │
│  │ • Events    │    │ • Stateless │    │ • Salt      │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 🔒 Security Architecture

### Defense in Depth

```
┌─────────────────────────────────────────────────────────────┐
│                   Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Application   │    │   Transport     │                │
│  │     Layer       │    │     Layer       │                │
│  │                 │    │                 │                │
│  │ • Input Val.    │    │ • HTTPS/TLS     │                │
│  │ • Auth/Author.  │    │ • Certificates  │                │
│  │ • Rate Limiting │    │ • CORS          │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Data Layer    │    │   Network       │                │
│  │                 │    │     Layer       │                │
│  │ • Encryption    │    │                 │                │
│  │ • Hashing       │    │ • Firewall      │                │
│  │ • Key Mgmt.     │    │ • VPN           │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Threat Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Threat Model                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   MITM      │    │   Brute     │    │   SQL       │     │
│  │   Attacks   │    │   Force     │    │ Injection   │     │
│  │             │    │             │    │             │     │
│  │ • HTTPS     │    │ • Rate Lim. │    │ • ODM       │     │
│  │ • Cert. Pin │    │ • bcrypt    │    │ • Validation│     │
│  │ • CORS      │    │ • 2FA       │    │ • Sanitize  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │     XSS     │    │    CSRF     │    │   File      │     │
│  │   Attacks   │    │   Attacks   │    │   Upload    │     │
│  │             │    │             │    │             │     │
│  │ • React     │    │ • JWT       │    │ • Type Val. │     │
│  │ • CSP       │    │ • CORS      │    │ • Size Lim. │     │
│  │ • Sanitize  │    │ • Tokens    │    │ • Encryption│     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 📈 Performance Architecture

### Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                   Caching Layers                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Browser       │    │   Application   │                │
│  │     Cache       │    │     Cache       │                │
│  │                 │    │                 │                │
│  │ • Static Assets │    │ • Session Data  │                │
│  │ • API Responses │    │ • User Data     │                │
│  │ • Images        │    │ • File Metadata│                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   CDN Cache     │    │   Database      │                │
│  │                 │    │     Cache       │                │
│  │ • Global Assets │    │                 │                │
│  │ • File Delivery │    │ • Query Cache   │                │
│  │ • Edge Locations│    │ • Index Cache   │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Scalability Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Scalability Model                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Horizontal    │    │   Vertical      │                │
│  │   Scaling       │    │   Scaling       │                │
│  │                 │    │                 │                │
│  │ • Load Balancer │    │ • CPU Increase  │                │
│  │ • Multiple      │    │ • Memory Boost  │                │
│  │   Instances     │    │ • Better HW     │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Database      │    │   Storage       │                │
│  │   Scaling       │    │   Scaling       │                │
│  │                 │    │                 │                │
│  │ • Read Replicas │    │ • CDN           │                │
│  │ • Sharding      │    │ • Multi-region  │                │
│  │ • Clustering    │    │ • Compression   │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Integration Architecture

### Local-Remote Integration

```
┌─────────────────────────────────────────────────────────────┐
│                Local-Remote Integration                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Local App     │    │   Remote App    │                │
│  │                 │    │                 │                │
│  │ 1. Encrypt File │    │ 1. Upload File  │                │
│  │ 2. Generate Key │    │ 2. Store in S3  │                │
│  │ 3. Create Bundle│    │ 3. Send Email   │                │
│  └─────────────────┘    └─────────────────┘                │
│           │                       │                        │
│           ▼                       ▼                        │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   File Bundle   │    │   Notification  │                │
│  │                 │    │                 │                │
│  │ • .enc file     │    │ • Email Alert   │                │
│  │ • .key file     │    │ • Real-time     │                │
│  │ • Metadata      │    │ • Download Link │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Recipient     │    │   Decryption    │                │
│  │                 │    │                 │                │
│  │ 1. Download     │    │ 1. Load Keys    │                │
│  │ 2. Extract      │    │ 2. Decrypt File │                │
│  │ 3. Decrypt      │    │ 3. Save File    │                │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Monitoring Architecture

### Observability Stack

```
┌─────────────────────────────────────────────────────────────┐
│                  Monitoring Stack                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Application   │    │   Infrastructure│                │
│  │   Monitoring    │    │   Monitoring    │                │
│  │                 │    │                 │                │
│  │ • Error Tracking│    │ • CPU Usage     │                │
│  │ • Performance   │    │ • Memory Usage  │                │
│  │ • User Analytics│    │ • Disk Usage    │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Logging       │    │   Alerting      │                │
│  │                 │    │                 │                │
│  │ • Structured    │    │ • Email Alerts  │                │
│  │   Logs          │    │ • SMS Alerts    │                │
│  │ • Log Aggregation│   │ • Slack Notifications│           │
│  └─────────────────┘    └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Development Workflow

### Git Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Git Workflow                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  main branch                                                │
│     │                                                       │
│     ├── feature/encryption                                  │
│     │   │                                                   │
│     │   ├── commit: "Add ECDH key generation"              │
│     │   ├── commit: "Implement AES encryption"             │
│     │   └── merge: "Merge encryption feature"              │
│     │                                                       │
│     ├── feature/authentication                              │
│     │   │                                                   │
│     │   ├── commit: "Add JWT authentication"               │
│     │   ├── commit: "Implement 2FA"                        │
│     │   └── merge: "Merge auth feature"                    │
│     │                                                       │
│     ├── feature/file-transfer                               │
│     │   │                                                   │
│     │   ├── commit: "Add file upload"                      │
│     │   ├── commit: "Implement S3 storage"                 │
│     │   └── merge: "Merge file transfer"                   │
│     │                                                       │
│     └── release/v1.0.0                                      │
│         │                                                   │
│         ├── tag: "v1.0.0"                                  │
│         └── deploy: "Production deployment"                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### CI/CD Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │     Git     │    │   GitHub    │    │   Build     │     │
│  │    Push     │───►│   Actions   │───►│   Process   │     │
│  │             │    │             │    │             │     │
│  │ • Code      │    │ • Trigger   │    │ • Install   │     │
│  │ • Tests     │    │ • Run Tests │    │ • Build     │     │
│  │ • Lint      │    │ • Security  │    │ • Package   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Deploy    │    │   Monitor   │    │   Rollback  │     │
│  │             │    │             │    │             │     │
│  │ • Vercel    │    │ • Health    │    │ • Auto      │     │
│  │ • Railway   │    │   Checks    │    │ • Manual    │     │
│  │ • AWS       │    │ • Metrics   │    │ • Version   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
``` 