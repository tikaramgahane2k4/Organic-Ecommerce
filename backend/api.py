from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from backend.app import mongo

api = Blueprint('api', __name__)

@api.route('/api/cart/count')
@login_required
def cart_count():
    count = sum(item.get('quantity', 1) for item in mongo.db.cart.find({'user_id': str(current_user.id)}))
    return jsonify({'count': count})
