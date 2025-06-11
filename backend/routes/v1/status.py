from flask import Blueprint, jsonify

from functions import *

status_bp = Blueprint('status', __name__, url_prefix='/v1')


### Routes for testing  #######
@status_bp.route('/system/status/api', methods=['GET'])
def taco_test():
    return "Mit der API ist alles Taco!"

# State of database
@status_bp.route('/system/status/db', methods=['GET'])
def taco_test_db():
    try:
        result_string = execute_query("SELECT name FROM taco_stack_test LIMIT 1", [])
        result_string = str(result_string[0]["name"]).replace('"','')
        return jsonify(result_string), 200
    except mariadb.Error as e:
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
        print(result_string)
    return jsonify(result_string), 500
