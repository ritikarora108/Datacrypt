# DataCrypt Remote - Web-Based File Transfer System

A full-stack web application for secure file transfer between users with end-to-end encryption, real-time notifications, and cloud storage integration.

## 🌐 Features

- **Secure File Transfer**: End-to-end encrypted file sharing
- **User Authentication**: JWT-based authentication with email verification
- **Real-time Notifications**: Socket.IO for instant file notifications
- **Cloud Storage**: AWS S3 integration for encrypted file storage
- **Email Notifications**: Automatic email alerts for file transfers
- **Modern UI**: React with TypeScript and Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (React/TS)    │◄──►│   (Node.js)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • File Upload   │    │ • API Routes    │    │ • AWS S3        │
│ • User Auth     │    │ • Socket.IO     │    │ • MongoDB       │
│ • Real-time UI  │    │ • File Storage  │    │ • SMTP Email    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- MongoDB database
- AWS S3 bucket
- SMTP email service (Gmail, SendGrid, etc.)

### Frontend Setup

```bash
cd DataCrypt-Remote

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup

```bash
cd DataCrypt-Remote/server

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start development server
npm run dev
```

### Run Both Simultaneously

```bash
# From DataCrypt-Remote directory
npm run dev:both
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `server/` directory:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/datacrypt

# JWT Authentication
JWT_SECRET=your-super-secret-jwt-key-here

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-s3-bucket-name

# Email Configuration (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Client URL
CLIENT_URL=http://localhost:5173

# Optional: QR Code for 2FA
QR_CODE_SECRET=your-qr-code-secret
```

### Frontend Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5000
```

## 📁 Project Structure

```
DataCrypt-Remote/
├── src/                    # React frontend source
│   ├── components/         # Reusable React components
│   │   ├── Navbar.tsx     # Navigation component
│   │   └── ProtectedRoute.tsx # Route protection
│   ├── contexts/          # React contexts
│   │   └── AuthContext.tsx # Authentication context
│   ├── pages/             # Page components
│   │   ├── Home.tsx       # Main dashboard
│   │   ├── SignIn.tsx     # Login page
│   │   ├── SignUp.tsx     # Registration page
│   │   └── NotFound.tsx   # 404 page
│   ├── utils/             # Utility functions
│   │   └── cryptography.ts # Crypto utilities
│   ├── App.tsx            # Main app component
│   └── main.tsx           # App entry point
├── server/                # Node.js backend
│   ├── routes/            # API route handlers
│   │   ├── auth.js        # Authentication routes
│   │   ├── transfers.js   # File transfer routes
│   │   ├── users.js       # User management routes
│   │   └── invite.js      # Invitation routes
│   ├── models/            # MongoDB schemas
│   │   ├── User.js        # User model
│   │   ├── Transfer.js    # File transfer model
│   │   └── FileSchema.js  # File metadata model
│   ├── middleware/        # Express middleware
│   │   └── auth.js        # JWT authentication middleware
│   ├── utils/             # Utility functions
│   │   ├── email.js       # Email sending utilities
│   │   └── s3.js          # AWS S3 utilities
│   └── index.js           # Server entry point
├── package.json           # Frontend dependencies
└── server/package.json    # Backend dependencies
```

## 🔐 Security Features

### Authentication & Authorization

- **JWT Tokens**: Secure session management
- **Email Verification**: TOTP-based account verification
- **Password Hashing**: bcrypt for secure password storage
- **Protected Routes**: Client and server-side route protection

### File Security

- **End-to-End Encryption**: Files encrypted client-side before upload


### Data Protection

- **CORS Protection**: Configured CORS for security
- **Secure Headers**: Security headers implementation

## 📊 API Documentation

### Authentication Endpoints

#### Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword",
  "publicKey": "user-public-key"
}
```

#### Login User

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Verify Email OTP

```http
POST /api/auth/verify-otp
Content-Type: application/json

{
  "email": "john@example.com",
  "otp": "123456"
}
```

### File Transfer Endpoints

#### Upload Encrypted File

```http
POST /api/transfers/upload
Content-Type: multipart/form-data

{
  "encryptedFile": [file],
  "encryptedAESKey": [file],
  "recipientEmail": "recipient@example.com",
  "fileName": "document.pdf"
}
```

#### Get Inbox Files

```http
GET /api/transfers/inbox
Authorization: Bearer <jwt-token>
```

#### Get Sent Files

```http
GET /api/transfers/sent?email=user@example.com
Authorization: Bearer <jwt-token>
```

### User Management Endpoints

#### Get User Public Key

```http
GET /api/users/public-key/:email
Authorization: Bearer <jwt-token>
```

#### Send Invitation

```http
POST /api/invite/send
Content-Type: application/json

{
  "email": "newuser@example.com"
}
```

## 🔄 Real-time Features

### Socket.IO Integration

The application uses Socket.IO for real-time features:

```javascript
// Client-side connection
const socket = io(API_URL, {
  withCredentials: true,
});

// Join user's personal room
socket.emit("join", userEmail);

// Listen for new file notifications
socket.on("new-file", (fileInfo) => {
  // Handle new file notification
});
```

### Real-time Events

- **new-file**: Notifies recipient when a file is uploaded
- **join/leave**: User room management for notifications

## 🎨 UI Components

### Main Dashboard (Home.tsx)

- File upload interface
- Inbox for received files
- Sent files history
- Real-time notifications

### Authentication Pages

- **SignUp**: User registration with email verification
- **SignIn**: User login with JWT authentication

### Responsive Design

- Mobile-first approach
- Tailwind CSS for styling
- Responsive navigation
- Touch-friendly interface

## 🛠️ Development

### Available Scripts

```bash
# Frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Backend
npm run server       # Start backend server
npm run dev:both     # Start both frontend and backend
```

### Development Workflow

1. **Frontend Development**

   ```bash
   cd DataCrypt-Remote
   npm run dev
   ```

2. **Backend Development**

   ```bash
   cd DataCrypt-Remote/server
   npm run dev
   ```

3. **Full Stack Development**
   ```bash
   cd DataCrypt-Remote
   npm run dev:both
   ```

### Code Quality

- **TypeScript**: Type-safe development
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **React Hooks**: Modern React patterns

## 🚀 Deployment

### Frontend Deployment (Vercel)

1. **Connect to Vercel**

   ```bash
   npm install -g vercel
   vercel login
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

### Backend Deployment

1. **Environment Setup**

   - Set production environment variables
   - Configure MongoDB Atlas
   - Set up AWS S3 bucket

2. **Deploy to Platform**
   ```bash
   npm start
   ```

### Environment Variables for Production

```env
NODE_ENV=production
MONGODB_URI=mongodb+srv://...
JWT_SECRET=production-secret
AWS_ACCESS_KEY_ID=production-key
AWS_SECRET_ACCESS_KEY=production-secret
CLIENT_URL=https://your-frontend-domain.com
```

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**

   - Check `CLIENT_URL` in environment variables
   - Verify CORS configuration in server

2. **MongoDB Connection Issues**

   - Verify `MONGODB_URI` is correct
   - Check network connectivity
   - Ensure MongoDB is running

3. **AWS S3 Upload Failures**

   - Verify AWS credentials
   - Check S3 bucket permissions
   - Ensure bucket exists in specified region

4. **Email Not Sending**
   - Check SMTP configuration
   - Verify email credentials
   - Check firewall/network settings

### Debug Mode

Enable debug logging:

```bash
DEBUG=* npm run dev
```

## 📈 Performance

### Optimization Features

- **File Compression**: Automatic file compression
- **Lazy Loading**: Component lazy loading
- **Caching**: Browser and server-side caching
- **CDN**: Static asset delivery optimization

### Monitoring

- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Response time monitoring
- **User Analytics**: Usage pattern tracking

## 🔄 Integration with Local Component

This web application works seamlessly with the DataCrypt Local component:

1. **Local Encryption**: Users encrypt files locally using the desktop app
2. **Web Upload**: Upload encrypted files through this web interface
3. **Secure Transfer**: Files are securely transferred between users
4. **Local Decryption**: Recipients decrypt files locally using their private keys

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

- Check the troubleshooting section
- Review the API documentation
- Create an issue in the repository
