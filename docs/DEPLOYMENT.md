# DataCrypt Deployment Guide

## 🚀 Overview

This guide covers deployment of both DataCrypt Local and Remote components across different environments and platforms.

## 📋 Prerequisites

### System Requirements

**Local Component**:

- Python 3.8+
- 100MB disk space
- 512MB RAM

**Remote Component**:

- Node.js 18+
- MongoDB 5.0+
- 1GB RAM
- 10GB disk space

### External Services

- **AWS S3**: File storage
- **SMTP Service**: Email delivery (Gmail, SendGrid, etc.)
- **Domain**: For production deployment

## 🛠️ Development Deployment

### Local Development Setup

#### 1. Clone Repository

```bash
git clone <repository-url>
cd Datacrypt-final-year-project
```

#### 2. Local Component Setup

```bash
cd DataCrypt-Local

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

#### 3. Remote Component Setup

```bash
cd DataCrypt-Remote

# Install frontend dependencies
npm install

# Install backend dependencies
cd server
npm install
cd ..

# Create environment files
cp .env.example .env
cp server/.env.example server/.env
```

#### 4. Configure Environment Variables

**Frontend (.env)**:

```env
VITE_API_URL=http://localhost:5000
```

**Backend (server/.env)**:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/datacrypt

# JWT Authentication
JWT_SECRET=your-development-secret-key

# AWS S3 (optional for development)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket

# Email (optional for development)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Client URL
CLIENT_URL=http://localhost:5173
```

#### 5. Start Development Servers

```bash
# Start both frontend and backend
npm run dev:both

# Or start separately
npm run dev          # Frontend only
npm run server       # Backend only
```

### Docker Development Setup

#### 1. Create Docker Compose File

```yaml
# docker-compose.dev.yml
version: "3.8"

services:
  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: datacrypt

  backend:
    build:
      context: ./DataCrypt-Remote/server
      dockerfile: Dockerfile.dev
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/datacrypt
      - NODE_ENV=development
    depends_on:
      - mongodb
    volumes:
      - ./DataCrypt-Remote/server:/app
      - /app/node_modules

  frontend:
    build:
      context: ./DataCrypt-Remote
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:5000
    depends_on:
      - backend
    volumes:
      - ./DataCrypt-Remote:/app
      - /app/node_modules

volumes:
  mongodb_data:
```

#### 2. Create Dockerfiles

**Backend Dockerfile.dev**:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5000

CMD ["npm", "run", "dev"]
```

**Frontend Dockerfile.dev**:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
```

#### 3. Run with Docker

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Stop services
docker-compose -f docker-compose.dev.yml down
```

## 🚀 Production Deployment

### Option 1: Cloud Platform Deployment

#### Vercel + Railway Deployment

**Frontend (Vercel)**:

1. **Connect to Vercel**:

   ```bash
   cd DataCrypt-Remote
   npm install -g vercel
   vercel login
   ```

2. **Deploy**:

   ```bash
   vercel --prod
   ```

3. **Configure Environment Variables**:
   - Go to Vercel Dashboard
   - Project Settings → Environment Variables
   - Add `VITE_API_URL=https://your-backend-domain.com`

**Backend (Railway)**:

1. **Connect to Railway**:

   ```bash
   cd DataCrypt-Remote/server
   npm install -g @railway/cli
   railway login
   ```

2. **Deploy**:

   ```bash
   railway init
   railway up
   ```

3. **Configure Environment Variables**:
   ```bash
   railway variables set MONGODB_URI=mongodb+srv://...
   railway variables set JWT_SECRET=your-production-secret
   railway variables set AWS_ACCESS_KEY_ID=your-aws-key
   railway variables set AWS_SECRET_ACCESS_KEY=your-aws-secret
   railway variables set AWS_REGION=us-east-1
   railway variables set AWS_S3_BUCKET_NAME=your-bucket
   railway variables set SMTP_HOST=smtp.gmail.com
   railway variables set SMTP_PORT=587
   railway variables set SMTP_USER=your-email@gmail.com
   railway variables set SMTP_PASS=your-app-password
   railway variables set CLIENT_URL=https://your-frontend-domain.com
   ```

#### AWS Deployment

**EC2 + RDS + S3 Setup**:

1. **Launch EC2 Instance**:

   ```bash
   # Connect to EC2
   ssh -i your-key.pem ubuntu@your-ec2-ip

   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # Install PM2
   sudo npm install -g pm2
   ```

2. **Deploy Backend**:

   ```bash
   # Clone repository
   git clone <repository-url>
   cd Datacrypt-final-year-project/DataCrypt-Remote/server

   # Install dependencies
   npm install

   # Create production environment file
   nano .env
   ```

3. **Configure PM2**:

   ```bash
   # Create ecosystem file
   nano ecosystem.config.js
   ```

   ```javascript
   module.exports = {
     apps: [
       {
         name: "datacrypt-backend",
         script: "index.js",
         instances: "max",
         exec_mode: "cluster",
         env: {
           NODE_ENV: "production",
           PORT: 5000,
         },
       },
     ],
   };
   ```

4. **Start Application**:

   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

5. **Configure Nginx**:

   ```bash
   sudo apt-get install nginx
   sudo nano /etc/nginx/sites-available/datacrypt
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

   ```bash
   sudo ln -s /etc/nginx/sites-available/datacrypt /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option 2: Docker Production Deployment

#### 1. Create Production Dockerfiles

**Backend Dockerfile**:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 5000

CMD ["npm", "start"]
```

**Frontend Dockerfile**:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Nginx Configuration**:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://backend:5000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

#### 2. Create Production Docker Compose

```yaml
# docker-compose.prod.yml
version: "3.8"

services:
  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: datacrypt
    restart: unless-stopped

  backend:
    build:
      context: ./DataCrypt-Remote/server
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/datacrypt
      - NODE_ENV=production
      - JWT_SECRET=${JWT_SECRET}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=${AWS_REGION}
      - AWS_S3_BUCKET_NAME=${AWS_S3_BUCKET_NAME}
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASS=${SMTP_PASS}
      - CLIENT_URL=${CLIENT_URL}
    depends_on:
      - mongodb
    restart: unless-stopped

  frontend:
    build:
      context: ./DataCrypt-Remote
      dockerfile: Dockerfile
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=${VITE_API_URL}
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  mongodb_data:
```

#### 3. Deploy with Docker

```bash
# Create .env file for production
cp .env.example .env
# Edit .env with production values

# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### Option 3: Kubernetes Deployment

#### 1. Create Kubernetes Manifests

**Namespace**:

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: datacrypt
```

**ConfigMap**:

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: datacrypt-config
  namespace: datacrypt
data:
  NODE_ENV: "production"
  PORT: "5000"
  AWS_REGION: "us-east-1"
  SMTP_HOST: "smtp.gmail.com"
  SMTP_PORT: "587"
```

**Secret**:

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: datacrypt-secrets
  namespace: datacrypt
type: Opaque
data:
  JWT_SECRET: <base64-encoded-secret>
  MONGODB_URI: <base64-encoded-uri>
  AWS_ACCESS_KEY_ID: <base64-encoded-key>
  AWS_SECRET_ACCESS_KEY: <base64-encoded-secret>
  AWS_S3_BUCKET_NAME: <base64-encoded-bucket>
  SMTP_USER: <base64-encoded-user>
  SMTP_PASS: <base64-encoded-password>
  CLIENT_URL: <base64-encoded-url>
```

**Backend Deployment**:

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datacrypt-backend
  namespace: datacrypt
spec:
  replicas: 3
  selector:
    matchLabels:
      app: datacrypt-backend
  template:
    metadata:
      labels:
        app: datacrypt-backend
    spec:
      containers:
        - name: backend
          image: datacrypt-backend:latest
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: datacrypt-config
            - secretRef:
                name: datacrypt-secrets
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

**Backend Service**:

```yaml
# backend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: datacrypt-backend-service
  namespace: datacrypt
spec:
  selector:
    app: datacrypt-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP
```

**Frontend Deployment**:

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datacrypt-frontend
  namespace: datacrypt
spec:
  replicas: 2
  selector:
    matchLabels:
      app: datacrypt-frontend
  template:
    metadata:
      labels:
        app: datacrypt-frontend
    spec:
      containers:
        - name: frontend
          image: datacrypt-frontend:latest
          ports:
            - containerPort: 80
          env:
            - name: VITE_API_URL
              value: "http://datacrypt-backend-service"
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
```

**Ingress**:

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: datacrypt-ingress
  namespace: datacrypt
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: datacrypt.your-domain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: datacrypt-frontend-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: datacrypt-backend-service
                port:
                  number: 80
```

#### 2. Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
kubectl apply -f ingress.yaml

# Check deployment status
kubectl get pods -n datacrypt
kubectl get services -n datacrypt
kubectl get ingress -n datacrypt
```

## 🔧 Environment Configuration

### Production Environment Variables

```env
# Server Configuration
NODE_ENV=production
PORT=5000

# Database
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/datacrypt

# JWT Authentication
JWT_SECRET=your-super-secure-production-secret-key

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-production-aws-access-key
AWS_SECRET_ACCESS_KEY=your-production-aws-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-production-bucket

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-production-email@gmail.com
SMTP_PASS=your-production-app-password

# Client URL
CLIENT_URL=https://your-production-domain.com

# Optional: Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=info
```

### Security Considerations

1. **Environment Variables**:

   - Never commit secrets to version control
   - Use secure secret management
   - Rotate secrets regularly

2. **SSL/TLS**:

   - Always use HTTPS in production
   - Configure proper SSL certificates
   - Enable HSTS headers

3. **Database Security**:

   - Use strong passwords
   - Enable network security
   - Regular backups

4. **AWS S3 Security**:
   - Configure bucket policies
   - Enable server-side encryption
   - Use IAM roles when possible

## 📊 Monitoring and Logging

### Application Monitoring

**PM2 Monitoring**:

```bash
# Monitor application
pm2 monit

# View logs
pm2 logs

# Restart application
pm2 restart all
```

**Docker Monitoring**:

```bash
# View container stats
docker stats

# View logs
docker-compose logs -f

# Monitor resources
docker system df
```

**Kubernetes Monitoring**:

```bash
# View pod logs
kubectl logs -f deployment/datacrypt-backend -n datacrypt

# Monitor resources
kubectl top pods -n datacrypt

# Check events
kubectl get events -n datacrypt
```

### Health Checks

**Backend Health Check**:

```bash
curl https://your-api-domain.com/health
```

**Frontend Health Check**:

```bash
curl https://your-frontend-domain.com/
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: |
          cd DataCrypt-Remote
          npm ci
          cd server
          npm ci

      - name: Run tests
        run: |
          cd DataCrypt-Remote
          npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./DataCrypt-Remote

      - name: Deploy to Railway
        uses: bervProject/railway-deploy@v1.0.0
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: datacrypt-backend
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Issues**:

   ```bash
   # Check MongoDB connection
   mongo --host your-mongodb-host --port 27017

   # Check connection string
   echo $MONGODB_URI
   ```

2. **AWS S3 Issues**:

   ```bash
   # Test AWS credentials
   aws sts get-caller-identity

   # Test S3 access
   aws s3 ls s3://your-bucket-name
   ```

3. **Email Issues**:

   ```bash
   # Test SMTP connection
   telnet smtp.gmail.com 587

   # Check email credentials
   echo $SMTP_USER
   ```

4. **Port Issues**:

   ```bash
   # Check if port is in use
   netstat -tulpn | grep :5000

   # Kill process using port
   sudo kill -9 $(lsof -t -i:5000)
   ```

### Performance Optimization

1. **Database Optimization**:

   - Create indexes on frequently queried fields
   - Use connection pooling
   - Monitor query performance

2. **Application Optimization**:

   - Enable compression
   - Use CDN for static assets
   - Implement caching

3. **Infrastructure Optimization**:
   - Use load balancers
   - Implement auto-scaling
   - Monitor resource usage

## 📈 Scaling

### Horizontal Scaling

1. **Load Balancer Setup**:

   ```bash
   # Nginx load balancer configuration
   upstream backend {
       server backend1:5000;
       server backend2:5000;
       server backend3:5000;
   }
   ```

2. **Database Scaling**:

   - Use MongoDB Atlas for managed scaling
   - Implement read replicas
   - Consider sharding for large datasets

3. **File Storage Scaling**:
   - Use CDN for file delivery
   - Implement file compression
   - Consider multi-region S3

### Vertical Scaling

1. **Resource Allocation**:

   - Increase CPU and memory
   - Optimize application code
   - Use better hardware

2. **Caching**:
   - Implement Redis for session storage
   - Use application-level caching
   - Enable browser caching

## 🔒 Security Hardening

### Production Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Database access restricted
- [ ] Firewall configured
- [ ] Regular security updates
- [ ] Monitoring and alerting
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan
- [ ] Security audit completed
- [ ] Compliance requirements met
