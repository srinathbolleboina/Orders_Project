# Contributing to Orders Management Application

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup instructions.

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 120 characters

### JavaScript (Frontend)
- Use ES6+ features
- Use meaningful variable names
- Add comments for complex logic
- Use async/await for asynchronous operations

## Testing

### Running Tests
```bash
cd backend
pytest tests/ -v
```

### Writing Tests
- Write tests for new features
- Maintain test coverage above 80%
- Test both success and failure cases
- Use descriptive test names

## Pull Request Guidelines

1. **Title**: Clear and descriptive
2. **Description**: Explain what and why
3. **Tests**: Include tests for new features
4. **Documentation**: Update docs if needed
5. **Code Review**: Address review comments

## Commit Messages

Format: `type(scope): subject`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example: `feat(auth): add password reset functionality`

## DevOps Practices to Explore

This application is designed for DevOps learning. Here are areas to explore:

### 1. Containerization
- Optimize Dockerfile
- Multi-stage builds
- Container security scanning

### 2. CI/CD
- Add more pipeline stages
- Implement automated deployments
- Add integration tests to pipeline

### 3. Monitoring
- Add Prometheus metrics
- Implement distributed tracing
- Set up alerting

### 4. Infrastructure as Code
- Terraform configurations
- Ansible playbooks
- Helm charts

### 5. Security
- Implement secrets management
- Add security scanning
- HTTPS/TLS configuration

### 6. Performance
- Database optimization
- Caching strategies
- Load testing

## Questions?

Feel free to open an issue for questions or discussions!
