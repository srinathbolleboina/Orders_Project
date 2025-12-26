"""
Health Check Routes - For monitoring and DevOps
"""
from flask import Blueprint, jsonify
from app import db
import logging

bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'service': 'orders-api'
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503


@bp.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint with version info"""
    return jsonify({
        'api': 'Orders Management API',
        'version': '1.0.0',
        'status': 'running'
    }), 200
