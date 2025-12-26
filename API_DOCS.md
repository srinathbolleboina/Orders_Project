# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"
  }
}
```

### Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

### Get Profile
**GET** `/auth/profile`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"
  }
}
```

---

## Product Endpoints

### Get All Products
**GET** `/products`

**Query Parameters:**
- `category` (optional): Filter by category
- `search` (optional): Search by name

**Response:** `200 OK`
```json
{
  "products": [...],
  "count": 10
}
```

### Get Product by ID
**GET** `/products/:id`

**Response:** `200 OK`
```json
{
  "product": {
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "stock_quantity": 50
  }
}
```

### Create Product (Admin Only)
**POST** `/products`

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "name": "New Product",
  "description": "Product description",
  "price": 49.99,
  "stock_quantity": 100,
  "category": "Electronics"
}
```

**Response:** `201 Created`

### Update Product (Admin Only)
**PUT** `/products/:id`

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "name": "Updated Product",
  "price": 59.99
}
```

**Response:** `200 OK`

### Delete Product (Admin Only)
**DELETE** `/products/:id`

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`

---

## Cart Endpoints

### Get Cart
**GET** `/cart`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "cart_items": [...],
  "total": 149.98,
  "count": 2
}
```

### Add to Cart
**POST** `/cart/add`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response:** `201 Created`

### Update Cart Item
**PUT** `/cart/:cart_item_id`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response:** `200 OK`

### Remove from Cart
**DELETE** `/cart/:cart_item_id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

## Order Endpoints

### Get User Orders
**GET** `/orders`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "orders": [...],
  "count": 5
}
```

### Get Order by ID
**GET** `/orders/:id`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

### Checkout
**POST** `/orders/checkout`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "shipping_address": "123 Main St, City, State 12345",
  "payment_method": "credit_card"
}
```

**Response:** `201 Created`

### Cancel Order
**POST** `/orders/:id/cancel`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

## Admin Endpoints

### Get Dashboard
**GET** `/admin/dashboard`

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`
```json
{
  "statistics": {
    "total_users": 100,
    "total_products": 50,
    "total_orders": 200,
    "total_revenue": 50000.00
  },
  "recent_orders": [...]
}
```

### Get All Orders (Admin)
**GET** `/admin/orders`

**Headers:** `Authorization: Bearer <admin_token>`

**Query Parameters:**
- `status` (optional): Filter by status

**Response:** `200 OK`

### Update Order Status
**PUT** `/admin/orders/:id/status`

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "status": "shipped"
}
```

**Response:** `200 OK`

---

## Health Check

### Health Check
**GET** `/health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "database": "connected",
  "service": "orders-api"
}
```

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**
```json
{
  "error": "Missing required field: email"
}
```

**401 Unauthorized**
```json
{
  "error": "Invalid or missing token"
}
```

**403 Forbidden**
```json
{
  "error": "Admin access required"
}
```

**404 Not Found**
```json
{
  "error": "Product not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "message": "Error details"
}
```

---

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error
