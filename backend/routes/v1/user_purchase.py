from flask import Blueprint, jsonify

from functions import *

# For Helper
from datetime import datetime, timedelta

user_purchase_bp = Blueprint('user_purchase', __name__, url_prefix='/v1')

### Helper for "shipping"
def get_shipping_info() -> str:
    shipping_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")
    shipping_str = "Ihre Bestellung wird " + shipping_date + " vorraussichtlich geliefert."
    return shipping_str

### Get/Remove all purchases for a user
@user_purchase_bp.route('/user/purchase', methods=['POST', 'GET', 'DELETE'])
def purchase():
    if not check_login():
        return jsonify(default_error_no_login), 403

    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT kauf_id, kaeufer_id, artikel_id, versanddaten, kaufpreis FROM abgeschlossene_kaeufe WHERE kaeufer_id=?", [session['username']])
        return jsonify(result), 200
    
    # Add new
    if request.method == 'POST':
        json_data = request.get_json()
        needed_parameters = ["kaeufer_id", "artikel_id", "versanddaten", "kaufpreis"]
        # Add user id
        json_data["kaeufer_id"] = session['username']

        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return jsonify(default_error), 405
        
        data = sort_parameters(data, needed_parameters)
        if(execute_edit("INSERT INTO abgeschlossene_kaeufe(kaeufer_id, artikel_id, versanddaten, kaufpreis) VALUES (?, ?, ?, ?)", data)):
            return jsonify(default_ok), 201
        
        return jsonify(default_error), 405
    
    # Delete
    if request.method == 'DELETE':
        if(execute_edit("DELETE FROM abgeschlossene_kaeufe WHERE kaeufer_id=?", [session['username']])):
            return jsonify(default_ok), 204
        return jsonify(default_error), 405

# TODO: route so?
@user_purchase_bp.route('/user/purchase/cart', methods=['GET'])
def purchase_cart():
    
    if not check_login():
        return jsonify(default_error_no_login), 403

    # Get Shopping cart
    cart = execute_query("SELECT artikel_id, anzahl, verkaeufer_id FROM warenkorb WHERE benutzer_id=?", [session['username']])

    if cart == []:
        return jsonify({"status": "Nothing in cart"}), 404
    
    # iterate items in cart
    purchases = []
    shipping_str = get_shipping_info()
    for item in cart:
        # add keufer_id
        item["kaeufer_id"] = session['username']
        # Add Shipping Info
        item["versanddaten"] = shipping_str
        # Append to new list of dicts
        purchases.append(item)

    return purchases