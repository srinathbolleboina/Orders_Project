# Orders Management Application

A full-stack Python-based Orders Management System designed for DevOps learning and practice.

## 🚀 Features

### User Features
- User registration and authentication
- Product browsing
- Shopping cart management
- Order placement and tracking
- Payment processing
- Order history

### Admin Features
- Product management (CRUD)
- Order management
- User management
- Analytics dashboard
- Payment tracking

### DevOps Features
- RESTful API with Flask
- JWT-based authentication
- Role-based access control
- Health check endpoints
- Structured logging
- Docker support
- API documentation (Swagger)
- Unit and integration tests
- Environment-based configuration

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Docker (optional, for containerization)

## 🛠️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd Orders_Project
```

### Step 2: Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 3: Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 5: Initialize Database
```bash
python backend/init_db.py
```

### Step 6: Run the Application
```bash
python backend/run.py
```

The backend API will be available at `http://localhost:5000`
Open `frontend/index.html` in your browser to access the UI.

## 🐳 Docker Setup

```bash
docker-compose up --build
```

## 📚 API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:5000/api/docs`
- Health Check: `http://localhost:5000/health`

## 🧪 Testing

```bash
pytest backend/tests/
```

## 📁 Project Structure

```
Orders_Project/
├── backend/           # Flask backend application
│   ├── app/          # Application code
│   │   ├── models/   # Database models
│   │   ├── routes/   # API endpoints
│   │   ├── services/ # Business logic
│   │   ├── middleware/ # Auth & other middleware
│   │   └── utils/    # Utility functions
│   └── tests/        # Test files
├── frontend/         # Frontend application
│   ├── css/         # Stylesheets
│   ├── js/          # JavaScript files
│   └── assets/      # Images and other assets
└── docker-compose.yml # Docker configuration
```

## 🔑 Default Credentials

**Admin:**
- Email: admin@orders.com
- Password: admin123

**Test User:**
- Email: user@orders.com
- Password: user123

## 🎯 DevOps Learning Opportunities

This application is designed to help you practice:
1. Containerization with Docker
2. CI/CD pipelines
3. Infrastructure as Code
4. Monitoring and logging
5. Testing strategies
6. Security best practices
7. Database management
8. API design and documentation

## 📝 License

MIT License - feel free to use for learning and practice!
