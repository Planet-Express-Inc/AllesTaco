from flask import Blueprint, jsonify

from functions import *

article_bp = Blueprint('article', __name__, url_prefix='/v1')


### Article
@article_bp.route('/article/<article_id>', methods=['GET', 'DELETE'])
@article_bp.route('/article', methods=['POST'])
def article(article_id=None):
    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT artikel_id, titel, verkaeufer_id, beschreibung, preis, status, bestand, kategorie FROM artikel WHERE artikel_id=?", [article_id])
        return result
    
    # Add new
    if request.method == 'POST':
        if not check_login():
            return default_error_no_login
        
        json_data = request.get_json()
        needed_parameters = ["titel", "verkaeufer_id", "beschreibung", "preis", "bild", "status", "bestand", "kategorie"]
        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return default_error
        
        data = sort_parameters(data, needed_parameters)
        execute_edit("INSERT INTO artikel(titel, verkaeufer_id, beschreibung, preis, bild, status, bestand, kategorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        return default_ok
    
    # Delete
    if request.method == 'DELETE':
        if not check_login():
            return default_error_no_login
        
        execute_edit("DELETE FROM artikel WHERE artikel_id=?", [article_id])
        return default_ok

# Picture for article
# TODO: Post for Picure? Or via JSON (-> Article POST)
@article_bp.route('/article/picture/<article_id>', methods=['GET'])
def get_article_picture(article_id):
    result = download_data("SELECT bild FROM artikel WHERE artikel_id=?", [article_id], article_id)
    return result