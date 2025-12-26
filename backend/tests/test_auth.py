"""
Authentication Tests
"""
import pytest


def test_register_success(client):
    """Test successful user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'password123',
        'first_name': 'New',
        'last_name': 'User'
    })
    
    assert response.status_code == 201
    assert 'user' in response.json
    assert response.json['user']['email'] == 'newuser@example.com'


def test_register_duplicate_email(client, auth_headers):
    """Test registration with duplicate email"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    
    assert response.status_code == 409


def test_login_success(client, auth_headers):
    """Test successful login"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'user' in response.json


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401


def test_get_profile(client, auth_headers):
    """Test getting user profile"""
    response = client.get('/api/auth/profile', headers=auth_headers)
    
    assert response.status_code == 200
    assert 'user' in response.json


def test_get_profile_unauthorized(client):
    """Test getting profile without authentication"""
    response = client.get('/api/auth/profile')
    
    assert response.status_code == 401
