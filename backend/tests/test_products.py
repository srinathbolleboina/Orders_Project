"""
Product Tests
"""
import pytest


def test_get_products(client, sample_product):
    """Test getting all products"""
    response = client.get('/api/products')
    
    assert response.status_code == 200
    assert 'products' in response.json
    assert len(response.json['products']) > 0


def test_get_product_by_id(client, sample_product):
    """Test getting single product"""
    response = client.get(f'/api/products/{sample_product.id}')
    
    assert response.status_code == 200
    assert response.json['product']['name'] == 'Test Product'


def test_create_product_admin(client, admin_headers):
    """Test creating product as admin"""
    response = client.post('/api/products', 
        headers=admin_headers,
        json={
            'name': 'New Product',
            'price': 49.99,
            'stock_quantity': 20,
            'category': 'Electronics'
        }
    )
    
    assert response.status_code == 201
    assert response.json['product']['name'] == 'New Product'


def test_create_product_unauthorized(client, auth_headers):
    """Test creating product as regular user (should fail)"""
    response = client.post('/api/products',
        headers=auth_headers,
        json={
            'name': 'New Product',
            'price': 49.99
        }
    )
    
    assert response.status_code == 403


def test_update_product_admin(client, admin_headers, sample_product):
    """Test updating product as admin"""
    response = client.put(f'/api/products/{sample_product.id}',
        headers=admin_headers,
        json={
            'name': 'Updated Product',
            'price': 79.99
        }
    )
    
    assert response.status_code == 200
    assert response.json['product']['name'] == 'Updated Product'


def test_delete_product_admin(client, admin_headers, sample_product):
    """Test deleting product as admin"""
    response = client.delete(f'/api/products/{sample_product.id}',
        headers=admin_headers
    )
    
    assert response.status_code == 200
