from flask import Blueprint, jsonify

from functions import *

cart_bp = Blueprint('cart', __name__, url_prefix='/v1')


### Cart
# TODO: all, Swagger!
@cart_bp.route('/cart', methods=['GET','POST','DELETE'])
def cart():
    if not check_login():
        return jsonify(default_error_no_login), 403
    
    # session['username']
    
    if request.method == 'GET':
        result = execute_query("SELECT warenkorb_id FROM artikel WHERE kaeufer_id=?", session['username'])
        print("cart-get: ")
        print(result)
        #####
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.json
        return jsonify({"message": "POST-Methode", "data": data}), 201

    elif request.method == 'DELETE':
        return jsonify({"message": "DELETE-Methode ausgeführt"}), 204

    return default_error_not_sup, 405