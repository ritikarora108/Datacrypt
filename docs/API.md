# DataCrypt API Documentation

## 🌐 Base URL

```
Development: http://localhost:5000
Production: https://your-api-domain.com
```

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

JWT tokens are obtained through the login endpoint and are valid for 24 hours.

## 📊 API Endpoints

### Authentication Endpoints

#### 1. Register User

**Endpoint**: `POST /api/auth/register`

**Description**: Register a new user account with email verification

**Request Body**:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
}
```

**Response** (201 Created):

```json
{
  "message": "User registered. Please verify your email."
}
```

**Response** (400 Bad Request):

```json
{
  "message": "User already exists"
}
```

**Example**:

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
  }'
```

#### 2. Verify Email OTP

**Endpoint**: `POST /api/auth/verify-otp`

**Description**: Verify email address using OTP sent during registration

**Request Body**:

```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response** (200 OK):

```json
{
  "message": "Email verified successfully"
}
```

**Response** (400 Bad Request):

```json
{
  "message": "Invalid or expired OTP"
}
```

**Example**:

```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp": "123456"
  }'
```

#### 3. Login User

**Endpoint**: `POST /api/auth/login`

**Description**: Authenticate user and receive JWT token

**Request Body**:

```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):

```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
  },
  "message": "User Login Success"
}
```

**Response** (401 Unauthorized):

```json
{
  "success": false,
  "message": "Password is incorrect"
}
```

**Example**:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### 4. Send Login OTP

**Endpoint**: `POST /api/auth/send-otp`

**Description**: Send OTP for login verification

**Request Body**:

```json
{
  "email": "john@example.com"
}
```

**Response** (200 OK):

```json
{
  "message": "OTP sent successfully"
}
```

**Example**:

```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
```

#### 5. Login with OTP

**Endpoint**: `POST /api/auth/login-otp`

**Description**: Login using OTP instead of password

**Request Body**:

```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response** (200 OK):

```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
  },
  "message": "User Login Success"
}
```

### File Transfer Endpoints

#### 1. Upload Encrypted File

**Endpoint**: `POST /api/transfers/upload`

**Description**: Upload encrypted file and key for transfer

**Headers**:

```
Authorization: Bearer <jwt-token>
Content-Type: multipart/form-data
```

**Form Data**:

- `encryptedFile`: Encrypted file (required)
- `encryptedAESKey`: Encrypted AES key file (required)
- `recipientEmail`: Recipient's email address (required)
- `fileName`: Original file name (optional)

**Response** (201 Created):

```json
{
  "message": "Files uploaded and encrypted successfully",
  "transferId": "507f1f77bcf86cd799439011",
  "accessLink": "https://client-domain.com/download/abc123"
}
```

**Response** (400 Bad Request):

```json
{
  "message": "Both files are required"
}
```

**Example**:

```bash
curl -X POST http://localhost:5000/api/transfers/upload \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -F "encryptedFile=@document.enc" \
  -F "encryptedAESKey=@document.key" \
  -F "recipientEmail=jane@example.com" \
  -F "fileName=document.pdf"
```

#### 2. Get Inbox Files

**Endpoint**: `GET /api/transfers/inbox`

**Description**: Get list of files received by the authenticated user

**Headers**:

```
Authorization: Bearer <jwt-token>
```

**Response** (200 OK):

```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "fileName": "document.pdf",
    "fileSize": 1048576,
    "sender": {
      "_id": "507f1f77bcf86cd799439012",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "createdAt": "2024-01-15T10:30:00.000Z",
    "encryptedFileUrl": "https://s3.amazonaws.com/bucket/file.enc?signature=...",
    "encryptedKeyUrl": "https://s3.amazonaws.com/bucket/file.key?signature=..."
  }
]
```

**Example**:

```bash
curl -X GET http://localhost:5000/api/transfers/inbox \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 3. Get Sent Files

**Endpoint**: `GET /api/transfers/sent`

**Description**: Get list of files sent by the authenticated user

**Headers**:

```
Authorization: Bearer <jwt-token>
```

**Query Parameters**:

- `email`: User's email address (required)

**Response** (200 OK):

```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "fileName": "document.pdf",
    "fileSize": 1048576,
    "recipient": {
      "email": "jane@example.com",
      "userId": "507f1f77bcf86cd799439013"
    },
    "createdAt": "2024-01-15T10:30:00.000Z",
    "downloaded": false,
    "expiresAt": "2024-01-22T10:30:00.000Z"
  }
]
```

**Example**:

```bash
curl -X GET "http://localhost:5000/api/transfers/sent?email=john@example.com" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 4. Download File

**Endpoint**: `GET /api/transfers/file/:token`

**Description**: Download encrypted file using access token

**Parameters**:

- `token`: Access token for the file (required)

**Response** (200 OK):

```
Binary file data
```

**Response** (404 Not Found):

```json
{
  "message": "File not found"
}
```

**Response** (410 Gone):

```json
{
  "message": "Link has expired"
}
```

**Example**:

```bash
curl -X GET http://localhost:5000/api/transfers/file/abc123 \
  -o downloaded_file.enc
```

### User Management Endpoints

#### 1. Get User Public Key

**Endpoint**: `GET /api/users/public-key/:email`

**Description**: Get public key for a specific user

**Headers**:

```
Authorization: Bearer <jwt-token>
```

**Parameters**:

- `email`: User's email address (required)

**Response** (200 OK):

```json
{
  "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
}
```

**Response** (404 Not Found):

```json
{
  "message": "User not found"
}
```

**Example**:

```bash
curl -X GET http://localhost:5000/api/users/public-key/jane@example.com \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 2. Update Public Key

**Endpoint**: `PUT /api/users/public-key`

**Description**: Update user's public key

**Headers**:

```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
}
```

**Response** (200 OK):

```json
{
  "message": "Public key updated successfully"
}
```

**Example**:

```bash
curl -X PUT http://localhost:5000/api/users/public-key \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
  }'
```

### Invitation Endpoints

#### 1. Send Invitation

**Endpoint**: `POST /api/invite/send`

**Description**: Send invitation email to new user

**Headers**:

```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body**:

```json
{
  "email": "newuser@example.com"
}
```

**Response** (200 OK):

```json
{
  "message": "Invitation sent successfully"
}
```

**Response** (400 Bad Request):

```json
{
  "message": "User already exists"
}
```

**Example**:

```bash
curl -X POST http://localhost:5000/api/invite/send \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com"
  }'
```

## 🔄 WebSocket Events

### Connection

**Event**: `connect`

**Description**: Client connects to Socket.IO server

**Example**:

```javascript
const socket = io("http://localhost:5000", {
  withCredentials: true,
});

socket.on("connect", () => {
  console.log("Connected to server");
});
```

### Join User Room

**Event**: `join`

**Description**: Join user's personal notification room

**Data**:

```javascript
{
  email: "user@example.com";
}
```

**Example**:

```javascript
socket.emit("join", "user@example.com");
```

### Leave User Room

**Event**: `leave`

**Description**: Leave user's personal notification room

**Data**:

```javascript
{
  email: "user@example.com";
}
```

**Example**:

```javascript
socket.emit("leave", "user@example.com");
```

### New File Notification

**Event**: `new-file`

**Description**: Receive notification when new file is uploaded

**Data**:

```javascript
{
  fileName: "document.pdf",
  sender: {
    name: "John Doe",
    email: "john@example.com"
  },
  createdAt: "2024-01-15T10:30:00.000Z",
  transferId: "507f1f77bcf86cd799439011"
}
```

**Example**:

```javascript
socket.on("new-file", (fileInfo) => {
  console.log("New file received:", fileInfo.fileName);
  // Update UI or show notification
});
```

## 📊 Error Responses

### Standard Error Format

```json
{
  "message": "Error description",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "path": "/api/endpoint"
}
```

### HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Access denied
- **404 Not Found**: Resource not found
- **410 Gone**: Resource expired
- **500 Internal Server Error**: Server error

### Common Error Messages

```json
{
  "message": "User already exists"
}
```

```json
{
  "message": "Invalid or expired OTP"
}
```

```json
{
  "message": "Password is incorrect"
}
```

```json
{
  "message": "Both files are required"
}
```

```json
{
  "message": "Recipient not found"
}
```

```json
{
  "message": "File not found"
}
```

```json
{
  "message": "Link has expired"
}
```

## 🔧 Rate Limiting

### Authentication Endpoints

- **Rate Limit**: 5 requests per 15 minutes
- **Window**: 15 minutes
- **Scope**: Per IP address

### File Upload Endpoints

- **Rate Limit**: 10 requests per hour
- **Window**: 1 hour
- **Scope**: Per user

### General Endpoints

- **Rate Limit**: 100 requests per minute
- **Window**: 1 minute
- **Scope**: Per IP address

### Rate Limit Response

```json
{
  "message": "Too many requests, please try again later",
  "retryAfter": 900
}
```

## 📋 Request/Response Examples

### Complete File Transfer Flow

#### 1. Register User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
  }'
```

#### 2. Verify Email

```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp": "123456"
  }'
```

#### 3. Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### 4. Get Recipient's Public Key

```bash
curl -X GET http://localhost:5000/api/users/public-key/jane@example.com \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 5. Upload Encrypted File

```bash
curl -X POST http://localhost:5000/api/transfers/upload \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -F "encryptedFile=@document.enc" \
  -F "encryptedAESKey=@document.key" \
  -F "recipientEmail=jane@example.com" \
  -F "fileName=document.pdf"
```

#### 6. Check Inbox (Recipient)

```bash
curl -X GET http://localhost:5000/api/transfers/inbox \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### 7. Download File

```bash
curl -X GET "http://localhost:5000/api/transfers/file/abc123" \
  -o downloaded_file.enc
```

## 🔍 Testing

### Using Postman

1. **Import Collection**: Use the provided Postman collection
2. **Set Environment Variables**:
   - `base_url`: http://localhost:5000
   - `token`: JWT token from login
3. **Run Tests**: Execute the collection

### Using curl

```bash
# Test server health
curl http://localhost:5000/

# Test registration
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"password123","publicKey":"test"}'
```

### Using JavaScript

```javascript
// Test API with fetch
const response = await fetch("http://localhost:5000/api/auth/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email: "test@example.com",
    password: "password123",
  }),
});

const data = await response.json();
console.log(data);
```

## 📚 SDK Examples

### JavaScript/TypeScript

```javascript
class DataCryptAPI {
  constructor(baseURL, token = null) {
    this.baseURL = baseURL;
    this.token = token;
  }

  setToken(token) {
    this.token = token;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async login(email, password) {
    const data = await this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    this.setToken(data.token);
    return data;
  }

  async uploadFile(encryptedFile, encryptedKey, recipientEmail, fileName) {
    const formData = new FormData();
    formData.append("encryptedFile", encryptedFile);
    formData.append("encryptedAESKey", encryptedKey);
    formData.append("recipientEmail", recipientEmail);
    formData.append("fileName", fileName);

    return this.request("/api/transfers/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });
  }

  async getInbox() {
    return this.request("/api/transfers/inbox");
  }
}

// Usage
const api = new DataCryptAPI("http://localhost:5000");
await api.login("user@example.com", "password123");
const inbox = await api.getInbox();
```

### Python

```python
import requests
import json

class DataCryptAPI:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()

        if token:
            self.session.headers.update({
                'Authorization': f'Bearer {token}'
            })

    def set_token(self, token):
        self.token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def login(self, email, password):
        response = self.session.post(
            f'{self.base_url}/api/auth/login',
            json={'email': email, 'password': password}
        )
        response.raise_for_status()
        data = response.json()
        self.set_token(data['token'])
        return data

    def upload_file(self, encrypted_file_path, encrypted_key_path,
                   recipient_email, file_name):
        with open(encrypted_file_path, 'rb') as f1, \
             open(encrypted_key_path, 'rb') as f2:
            files = {
                'encryptedFile': f1,
                'encryptedAESKey': f2
            }
            data = {
                'recipientEmail': recipient_email,
                'fileName': file_name
            }
            response = self.session.post(
                f'{self.base_url}/api/transfers/upload',
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()

    def get_inbox(self):
        response = self.session.get(f'{self.base_url}/api/transfers/inbox')
        response.raise_for_status()
        return response.json()

# Usage
api = DataCryptAPI('http://localhost:5000')
api.login('user@example.com', 'password123')
inbox = api.get_inbox()
```
