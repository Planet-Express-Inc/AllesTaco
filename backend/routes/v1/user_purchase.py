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
        result = execute_query("SELECT kauf_id, kaeufer_id, artikel_id, anzahl, verkaeufer_id, versanddaten, kaufpreis FROM abgeschlossene_kaeufe WHERE kaeufer_id=?", [session['username']])
        return jsonify(result), 200
    
    # New One
    if request.method == 'POST':
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
            # Get infos from article
            article_info = execute_query("SELECT preis, bestand FROM artikel WHERE artikel_id=?", [item["artikel_id"]])[0]
            price_of_one = int(article_info["preis"])
            # Check amount
            if int(article_info["bestand"]) < int(item["anzahl"]):
                return jsonify({"error": "Article amount less than demanded.", "artikel_id": str(item["artikel_id"]), "bestand": str(article_info["bestand"]), "anzahl": str(item["anzahl"])}), 409
            # Get price for all
            item["kaufpreis"] = price_of_one * int(item["anzahl"])

            # Append to new list of dicts
            purchases.append(item)
        
        # Another loop, after checking all availability. Buying
        for item in cart:
            # Lower Stock
            if not execute_edit("UPDATE artikel SET bestand = bestand - ? WHERE artikel_id = ?", [item["anzahl"], item["artikel_id"]]):
                return jsonify({"error": "while updating stock of id " + item["artikel_id"]}), 409
            
            # Sort
            needed_parameters = ["kaeufer_id", "artikel_id", "anzahl", "verkaeufer_id", "versanddaten", "kaufpreis"]
            data = sort_parameters(item, needed_parameters)
            if not execute_edit("INSERT INTO abgeschlossene_kaeufe(kaeufer_id, artikel_id, anzahl, verkaeufer_id, versanddaten, kaufpreis) VALUES (?, ?, ?, ?, ?, ?)", data):
                return jsonify({"error": "while inserting to abgeschlossene_kaeufe, id " + item["artikel_id"]}), 409
            
            if not execute_edit("DELETE FROM warenkorb WHERE benutzer_id=? AND artikel_id=?", [session['username'], item["artikel_id"]]):
                return jsonify({"error": "while deleting cart, id " + item["artikel_id"]}), 409
        
        
        return jsonify(default_ok), 201


    # Delete
    if request.method == 'DELETE':
        if(execute_edit("DELETE FROM abgeschlossene_kaeufe WHERE kaeufer_id=?", [session['username']])):
            return jsonify(default_ok), 204
        return jsonify(default_error), 405

