from flask import Blueprint, jsonify

from functions import *

user_sales_bp = Blueprint('user_sales', __name__, url_prefix='/v1')


### Get/Remove all purchases for a user
@user_sales_bp.route('/user/sales/<user_id>', methods=['GET'])
def sales(user_id):
    if not check_login():
        return jsonify(default_error_no_login), 403

    result = execute_query("SELECT kauf_id, kaeufer_id, artikel_id, anzahl, datum, verkaeufer_id, versanddaten, kaufpreis FROM abgeschlossene_kaeufe WHERE verkaeufer_id=?", [user_id])
    # Add day, month, year
    for item in result:
        date_dict = split_sql_date(str(item["datum"]))
        item.update(date_dict)
    return jsonify(result), 200
