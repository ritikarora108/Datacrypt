# DataCrypt Security Documentation

## 🔐 Security Overview

DataCrypt implements a comprehensive security architecture that ensures end-to-end encryption, secure authentication, and protection against various attack vectors.

## 🛡️ Security Principles

### 1. Defense in Depth

- Multiple layers of security controls
- No single point of failure
- Comprehensive threat modeling

### 2. Zero Trust Architecture

- Never trust, always verify
- Continuous authentication
- Least privilege access

### 3. Privacy by Design

- End-to-end encryption
- Minimal data collection
- User data sovereignty

## 🔐 Cryptographic Implementation

### ECDH Key Exchange

**Algorithm**: Elliptic Curve Diffie-Hellman (ECDH)
**Curve**: SECP384R1 (NIST P-384)
**Key Size**: 384 bits

```python
# Key Generation
private_key = ec.generate_private_key(ec.SECP384R1())
public_key = private_key.public_key()

# Key Exchange
shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
```

**Security Benefits**:

- Perfect forward secrecy
- Smaller key sizes than RSA
- Resistance to quantum attacks (compared to RSA)
- Efficient computation

### AES Encryption

**Algorithm**: Advanced Encryption Standard (AES)
**Mode**: Cipher Block Chaining (CBC)
**Key Size**: 256 bits
**Padding**: PKCS7

```python
# Encryption
iv = os.urandom(16)  # Random IV
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
encryptor = cipher.encryptor()

# PKCS7 Padding
pad_len = 16 - (len(data) % 16)
padded_data = data + bytes([pad_len] * pad_len)
encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
```

**Security Benefits**:

- Industry standard encryption
- Random IV prevents pattern analysis
- PKCS7 padding ensures proper block alignment

### Key Derivation Function

**Algorithm**: HKDF (HMAC-based Key Derivation Function)
**Hash Function**: SHA-256
**Salt**: None (for simplicity, can be enhanced)

```python
# Key Derivation
aes_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,  # 256 bits
    salt=None,
    info=b'handshake data',
).derive(shared_key)
```

**Security Benefits**:

- Deterministic key derivation
- Resistance to rainbow table attacks
- Configurable output length

## 🔑 Key Management

### Key Generation

```python
def generate_key_pair():
    """Generate ECDH key pair with SECP384R1 curve"""
    private_key = ec.generate_private_key(ec.SECP384R1())

    # Serialize private key (unencrypted for simplicity)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serialize public key
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_pem, public_pem
```

### Key Storage

**Local Component**:

- Private keys stored locally in `keys/` directory
- Never transmitted over network
- File system permissions protection

**Remote Component**:

- Only public keys stored in database
- Private keys never uploaded to server
- Encrypted at rest in database

### Key Lifecycle

1. **Generation**: ECDH key pair created locally
2. **Storage**: Private key stored securely, public key shared
3. **Usage**: Ephemeral keys generated for each encryption
4. **Rotation**: Manual key rotation supported
5. **Destruction**: Secure key deletion when needed

## 🔐 Authentication Security

### JWT Implementation

**Algorithm**: HMAC SHA-256
**Expiration**: 24 hours
**Claims**: User ID, email, timestamp

```javascript
// JWT Generation
const token = jwt.sign(
  {
    email: user.email,
    id: user._id,
    iat: Math.floor(Date.now() / 1000),
  },
  process.env.JWT_SECRET,
  { expiresIn: "24h" }
);

// JWT Verification
const decoded = jwt.verify(token, process.env.JWT_SECRET);
```

**Security Features**:

- Short expiration time
- Secure secret key
- Stateless authentication
- Automatic token validation

### Password Security

**Hashing Algorithm**: bcrypt
**Salt Rounds**: 10
**Password Requirements**: Minimum 8 characters

```javascript
// Password Hashing
const salt = await bcrypt.genSalt(10);
const hashedPassword = await bcrypt.hash(password, salt);

// Password Verification
const isMatch = await bcrypt.compare(password, hashedPassword);
```

**Security Features**:

- Adaptive hashing
- Salt protection
- Slow computation prevents brute force
- Constant-time comparison

### Two-Factor Authentication

**Method**: TOTP (Time-based One-Time Password)
**Algorithm**: HMAC-SHA1
**Time Step**: 300 seconds (5 minutes)
**Digits**: 6

```javascript
// TOTP Generation
const otp = speakeasy.totp({
  secret: user.otpSecret,
  encoding: "base32",
  step: 300,
  window: 1, // Allow 1 step before and after
});

// TOTP Verification
const isValid = speakeasy.totp.verify({
  secret: user.otpSecret,
  encoding: "base32",
  token: otp,
  step: 300,
  window: 1,
});
```

**Security Features**:

- Time-based tokens
- Short expiration
- Email delivery
- Rate limiting

## 🛡️ File Security

### End-to-End Encryption

```
User A (Sender)                    User B (Recipient)
     │                                   │
     │ 1. Generate ephemeral key         │
     │ 2. ECDH with User B's public key  │
     │ 3. Derive AES key                 │
     │ 4. Encrypt file with AES          │
     │ 5. Upload encrypted file          │
     │                                   │ 6. Download encrypted file
     │                                   │ 7. ECDH with ephemeral key
     │                                   │ 8. Derive AES key
     │                                   │ 9. Decrypt file
```

### File Storage Security

**AWS S3 Configuration**:

- Server-side encryption (SSE-S3)
- Bucket policies for access control
- Signed URLs with expiration
- CORS configuration

```javascript
// S3 Upload with Encryption
const uploadParams = {
  Bucket: process.env.AWS_S3_BUCKET_NAME,
  Key: fileKey,
  Body: fileBuffer,
  ServerSideEncryption: "AES256",
  ContentType: file.mimetype,
};

// Signed URL Generation
const signedUrl = await getSignedUrl(
  s3Client,
  new GetObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET_NAME,
    Key: fileKey,
  }),
  { expiresIn: 300 } // 5 minutes
);
```

### Access Control

**File Access Tokens**:

- UUID-based unique tokens
- Time-limited expiration (7 days)
- One-time use tracking
- Automatic cleanup

## 🌐 Network Security

### HTTPS/TLS

**Protocol**: TLS 1.3
**Certificate**: Valid SSL certificate
**HSTS**: HTTP Strict Transport Security
**CSP**: Content Security Policy

### CORS Configuration

```javascript
// CORS Setup
app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin) return callback(null, true);
      if (allowedOrigins.indexOf(origin) === -1) {
        return callback(new Error("CORS policy violation"), false);
      }
      return callback(null, true);
    },
    credentials: true,
  })
);
```

**Security Features**:

- Whitelist-based origin control
- Credential support
- Preflight request handling

### Rate Limiting

```javascript
// Rate Limiting Implementation
const rateLimit = require("express-rate-limit");

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: "Too many authentication attempts",
});

app.use("/api/auth", authLimiter);
```

**Protection Against**:

- Brute force attacks
- DDoS attacks
- API abuse

## 🔍 Input Validation

### Server-Side Validation

```javascript
// Input Validation Example
const { body, validationResult } = require("express-validator");

const validateRegistration = [
  body("email").isEmail().normalizeEmail(),
  body("password").isLength({ min: 8 }),
  body("name").trim().isLength({ min: 2, max: 50 }),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
];
```

### File Upload Security

```javascript
// File Upload Validation
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 100 * 1024 * 1024, // 100MB limit
    files: 2, // Max 2 files per request
  },
  fileFilter: (req, file, cb) => {
    // Validate file type
    if (file.mimetype.startsWith("application/")) {
      cb(null, true);
    } else {
      cb(new Error("Invalid file type"), false);
    }
  },
});
```

## 🚨 Security Monitoring

### Logging

**Security Events**:

- Authentication attempts
- File access patterns
- Error occurrences
- Rate limit violations

```javascript
// Security Logging
const securityLogger = (req, res, next) => {
  const logData = {
    timestamp: new Date().toISOString(),
    ip: req.ip,
    method: req.method,
    path: req.path,
    userAgent: req.get("User-Agent"),
    userId: req.user?.id,
  };

  console.log("Security Event:", logData);
  next();
};
```

### Error Handling

```javascript
// Secure Error Handling
app.use((error, req, res, next) => {
  // Don't expose internal errors
  const message =
    process.env.NODE_ENV === "production"
      ? "Internal server error"
      : error.message;

  res.status(500).json({
    error: message,
    timestamp: new Date().toISOString(),
  });
});
```

## 🔒 Privacy Protection

### Data Minimization

**Stored Data**:

- User email and name
- Public keys only
- File metadata (name, size, timestamps)
- No file content stored

**Not Stored**:

- Private keys
- File contents
- Decryption keys
- User passwords (only hashes)

### GDPR Compliance

**User Rights**:

- Right to access personal data
- Right to deletion
- Right to data portability
- Right to rectification

**Data Retention**:

- Files: 7 days automatic expiration
- User accounts: Until deletion request
- Logs: 30 days retention

## 🛡️ Threat Model

### Attack Vectors

1. **Man-in-the-Middle (MITM)**

   - **Mitigation**: HTTPS/TLS, certificate pinning
   - **Risk**: Low (encrypted communication)

2. **Brute Force Attacks**

   - **Mitigation**: Rate limiting, strong passwords, bcrypt
   - **Risk**: Low (slow hashing, rate limits)

3. **SQL Injection**

   - **Mitigation**: Parameterized queries, input validation
   - **Risk**: Low (MongoDB ODM protection)

4. **XSS Attacks**

   - **Mitigation**: Input sanitization, CSP headers
   - **Risk**: Low (React XSS protection)

5. **CSRF Attacks**

   - **Mitigation**: CORS policies, token validation
   - **Risk**: Low (stateless JWT)

6. **File Upload Attacks**
   - **Mitigation**: File type validation, size limits
   - **Risk**: Low (encrypted files only)

### Security Controls

**Preventive Controls**:

- Input validation
- Authentication
- Authorization
- Encryption

**Detective Controls**:

- Logging
- Monitoring
- Error tracking
- Rate limiting

**Corrective Controls**:

- Automatic cleanup
- Error handling
- Backup and recovery
- Incident response

## 🔐 Security Best Practices

### For Developers

1. **Never log sensitive data**
2. **Use environment variables for secrets**
3. **Validate all inputs**
4. **Implement proper error handling**
5. **Keep dependencies updated**
6. **Use HTTPS in production**
7. **Implement rate limiting**
8. **Regular security audits**

### For Users

1. **Keep private keys secure**
2. **Use strong passwords**
3. **Enable 2FA**
4. **Verify email addresses**
5. **Don't share access tokens**
6. **Report suspicious activity**
7. **Regular key rotation**
8. **Secure device access**

## 🔄 Security Updates

### Regular Maintenance

- **Dependency Updates**: Monthly security patches
- **Certificate Renewal**: SSL certificate monitoring
- **Security Audits**: Quarterly code reviews
- **Penetration Testing**: Annual security assessments

### Incident Response

1. **Detection**: Automated monitoring and alerts
2. **Analysis**: Security team investigation
3. **Containment**: Immediate threat isolation
4. **Eradication**: Root cause elimination
5. **Recovery**: Service restoration
6. **Lessons Learned**: Process improvement

## 📋 Security Checklist

### Development

- [ ] Input validation implemented
- [ ] Authentication required
- [ ] Authorization checks in place
- [ ] HTTPS enforced
- [ ] Error handling secure
- [ ] Logging configured
- [ ] Rate limiting active
- [ ] CORS properly configured

### Deployment

- [ ] Environment variables set
- [ ] SSL certificate valid
- [ ] Database secured
- [ ] File permissions correct
- [ ] Monitoring active
- [ ] Backups configured
- [ ] Security headers set
- [ ] Dependencies updated
