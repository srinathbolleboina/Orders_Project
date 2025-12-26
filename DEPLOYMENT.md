# Deployment Guide

This guide covers different deployment strategies for the Orders Management Application.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Deployment](#cloud-deployment)

---

## Local Development

### Prerequisites
- Python 3.8+
- Node.js (optional, for frontend development)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Orders_Project
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Backend API: http://localhost:5000
   - Frontend: Open `frontend/index.html` in your browser
   - Health Check: http://localhost:5000/health

---

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000
   - Health Check: http://localhost:8080/health

3. **Stop the application**
   ```bash
   docker-compose down
   ```

### Production Deployment

1. **Update environment variables**
   - Edit `docker-compose.yml` to use production values
   - Set strong SECRET_KEY and JWT_SECRET_KEY

2. **Use production database**
   - Replace SQLite with PostgreSQL or MySQL
   - Update DATABASE_URL in docker-compose.yml

3. **Run in detached mode**
   ```bash
   docker-compose up -d
   ```

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

---

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, EKS, GKE, AKS)
- kubectl configured

### Deployment Steps

1. **Update secrets**
   ```bash
   # Edit k8s-deployment.yaml and update Secret values
   ```

2. **Apply Kubernetes manifests**
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

3. **Check deployment status**
   ```bash
   kubectl get pods -n orders-app
   kubectl get services -n orders-app
   ```

4. **Access the application**
   ```bash
   # Get external IP
   kubectl get service orders-frontend-service -n orders-app
   ```

5. **Scale the application**
   ```bash
   kubectl scale deployment orders-backend -n orders-app --replicas=5
   ```

6. **View logs**
   ```bash
   kubectl logs -f deployment/orders-backend -n orders-app
   ```

---

## Cloud Deployment

### AWS (Elastic Beanstalk)

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   cd backend
   eb init -p python-3.11 orders-app
   ```

3. **Create environment**
   ```bash
   eb create orders-production
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

### Azure (App Service)

1. **Install Azure CLI**
   ```bash
   # Follow Azure CLI installation guide
   ```

2. **Login to Azure**
   ```bash
   az login
   ```

3. **Create resource group**
   ```bash
   az group create --name orders-rg --location eastus
   ```

4. **Create App Service plan**
   ```bash
   az appservice plan create --name orders-plan --resource-group orders-rg --sku B1 --is-linux
   ```

5. **Create web app**
   ```bash
   az webapp create --resource-group orders-rg --plan orders-plan --name orders-app --runtime "PYTHON|3.11"
   ```

6. **Deploy code**
   ```bash
   cd backend
   az webapp up --name orders-app --resource-group orders-rg
   ```

### Google Cloud (Cloud Run)

1. **Build container**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/orders-backend
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy orders-backend \
     --image gcr.io/PROJECT_ID/orders-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## Environment Variables

### Required Variables
- `SECRET_KEY`: Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `JWT_SECRET_KEY`: JWT secret key
- `DATABASE_URL`: Database connection string

### Optional Variables
- `FLASK_ENV`: development/production
- `LOG_LEVEL`: INFO/DEBUG/WARNING/ERROR
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

---

## Database Migration

### SQLite to PostgreSQL

1. **Install PostgreSQL**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update DATABASE_URL**
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/orders_db
   ```

3. **Re-initialize database**
   ```bash
   python init_db.py
   ```

---

## Monitoring and Logging

### Health Checks
- Endpoint: `/health`
- Returns: `{"status": "healthy", "database": "connected"}`

### Logs
- Application logs are written to stdout
- Configure log aggregation (ELK, Splunk, CloudWatch)

### Metrics
- Monitor `/health` endpoint
- Track response times
- Monitor database connections

---

## Troubleshooting

### Database Connection Issues
```bash
# Check database file permissions
ls -la backend/*.db

# Reinitialize database
python backend/init_db.py
```

### Port Already in Use
```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Kill the process or use different port
```

### Docker Issues
```bash
# Clean up Docker
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up
```

---

## Security Best Practices

1. **Change default credentials** in production
2. **Use strong secret keys**
3. **Enable HTTPS** in production
4. **Use environment variables** for sensitive data
5. **Regular security updates**
6. **Implement rate limiting**
7. **Use database backups**

---

## Performance Optimization

1. **Use production database** (PostgreSQL/MySQL)
2. **Enable caching** (Redis)
3. **Use CDN** for static files
4. **Implement load balancing**
5. **Database indexing**
6. **Connection pooling**

---

For more information, see the main [README.md](README.md)
