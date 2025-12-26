// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
const state = {
    user: null,
    token: null,
    cart: [],
    products: [],
    orders: []
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadFromLocalStorage();
    checkAuth();
});

// Local Storage
function saveToLocalStorage() {
    localStorage.setItem('token', state.token || '');
    localStorage.setItem('user', JSON.stringify(state.user || {}));
}

function loadFromLocalStorage() {
    state.token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            state.user = JSON.parse(userStr);
        } catch (e) {
            state.user = null;
        }
    }
}

function clearLocalStorage() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    state.token = null;
    state.user = null;
}

// API Helper Functions
async function apiRequest(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (state.token) {
        headers['Authorization'] = `Bearer ${state.token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication Functions
async function login(email, password) {
    try {
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });

        state.token = data.access_token;
        state.user = data.user;
        saveToLocalStorage();

        return data;
    } catch (error) {
        throw error;
    }
}

async function register(userData) {
    try {
        const data = await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });

        return data;
    } catch (error) {
        throw error;
    }
}

function logout() {
    clearLocalStorage();
    window.location.href = 'index.html';
}

function checkAuth() {
    if (!state.token || !state.user) {
        const publicPages = ['index.html', 'login.html', 'register.html'];
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';

        if (!publicPages.includes(currentPage)) {
            window.location.href = 'login.html';
        }
    }
}

function isAdmin() {
    return state.user && state.user.role === 'admin';
}

// Product Functions
async function getProducts(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const data = await apiRequest(`/products?${params}`);
        state.products = data.products;
        return data;
    } catch (error) {
        throw error;
    }
}

async function getProduct(productId) {
    try {
        const data = await apiRequest(`/products/${productId}`);
        return data.product;
    } catch (error) {
        throw error;
    }
}

async function createProduct(productData) {
    try {
        const data = await apiRequest('/products', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
        return data;
    } catch (error) {
        throw error;
    }
}

async function updateProduct(productId, productData) {
    try {
        const data = await apiRequest(`/products/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(productData)
        });
        return data;
    } catch (error) {
        throw error;
    }
}

async function deleteProduct(productId) {
    try {
        const data = await apiRequest(`/products/${productId}`, {
            method: 'DELETE'
        });
        return data;
    } catch (error) {
        throw error;
    }
}

// Cart Functions
async function getCart() {
    try {
        const data = await apiRequest('/cart');
        state.cart = data.cart_items;
        updateCartBadge();
        return data;
    } catch (error) {
        throw error;
    }
}

async function addToCart(productId, quantity = 1) {
    try {
        const data = await apiRequest('/cart/add', {
            method: 'POST',
            body: JSON.stringify({ product_id: productId, quantity })
        });
        await getCart(); // Refresh cart
        return data;
    } catch (error) {
        throw error;
    }
}

async function updateCartItem(cartItemId, quantity) {
    try {
        const data = await apiRequest(`/cart/${cartItemId}`, {
            method: 'PUT',
            body: JSON.stringify({ quantity })
        });
        await getCart(); // Refresh cart
        return data;
    } catch (error) {
        throw error;
    }
}

async function removeFromCart(cartItemId) {
    try {
        const data = await apiRequest(`/cart/${cartItemId}`, {
            method: 'DELETE'
        });
        await getCart(); // Refresh cart
        return data;
    } catch (error) {
        throw error;
    }
}

async function clearCart() {
    try {
        const data = await apiRequest('/cart/clear', {
            method: 'DELETE'
        });
        state.cart = [];
        updateCartBadge();
        return data;
    } catch (error) {
        throw error;
    }
}

// Order Functions
async function getOrders() {
    try {
        const data = await apiRequest('/orders');
        state.orders = data.orders;
        return data;
    } catch (error) {
        throw error;
    }
}

async function getOrder(orderId) {
    try {
        const data = await apiRequest(`/orders/${orderId}`);
        return data.order;
    } catch (error) {
        throw error;
    }
}

async function checkout(orderData) {
    try {
        const data = await apiRequest('/orders/checkout', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
        await getCart(); // Refresh cart (should be empty)
        return data;
    } catch (error) {
        throw error;
    }
}

async function cancelOrder(orderId) {
    try {
        const data = await apiRequest(`/orders/${orderId}/cancel`, {
            method: 'POST'
        });
        return data;
    } catch (error) {
        throw error;
    }
}

// Admin Functions
async function getDashboard() {
    try {
        const data = await apiRequest('/admin/dashboard');
        return data;
    } catch (error) {
        throw error;
    }
}

async function getAllOrders(status = null) {
    try {
        const params = status ? `?status=${status}` : '';
        const data = await apiRequest(`/admin/orders${params}`);
        return data;
    } catch (error) {
        throw error;
    }
}

async function updateOrderStatus(orderId, status) {
    try {
        const data = await apiRequest(`/admin/orders/${orderId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
        return data;
    } catch (error) {
        throw error;
    }
}

async function getAllUsers() {
    try {
        const data = await apiRequest('/admin/users');
        return data;
    } catch (error) {
        throw error;
    }
}

async function toggleUserStatus(userId) {
    try {
        const data = await apiRequest(`/admin/users/${userId}/toggle`, {
            method: 'PUT'
        });
        return data;
    } catch (error) {
        throw error;
    }
}

// UI Helper Functions
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loading-spinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    if (badge) {
        const count = state.cart.length;
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    }
}

function formatCurrency(amount) {
    return `$${parseFloat(amount).toFixed(2)}`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Export for use in other files
window.app = {
    state,
    login,
    register,
    logout,
    checkAuth,
    isAdmin,
    getProducts,
    getProduct,
    createProduct,
    updateProduct,
    deleteProduct,
    getCart,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    getOrders,
    getOrder,
    checkout,
    cancelOrder,
    getDashboard,
    getAllOrders,
    updateOrderStatus,
    getAllUsers,
    toggleUserStatus,
    showAlert,
    showLoading,
    hideLoading,
    updateCartBadge,
    formatCurrency,
    formatDate
};
