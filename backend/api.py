import sys
import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import time

import mariadb

#from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException


taco = Flask(__name__)

# Swagger base config
"""
swagger_config = {
    "spec": {
        "openapi": "3.0.3", 
        "info": {
            "title": "Chat Support - 1.0",
            "description": "Chat Support API 1.0",
            "version": "1.0.0",
        },
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}
taco.config["SWAGGER"] = swagger_config
taco.config["SWAGGER"]['openapi'] = '3.0.3'

# Load yaml
swagger = Swagger(chat, template_file='swagger/swagger.yaml')
"""
CORS(taco)


# Connect to Database
# Connect to MariaDB Platform
try:
    # Wait for DB
    time.sleep(5)
    conn = mariadb.connect(
        user="taco",
        password="erb6dbfnsm47ptk90i9sw87",
        #host="tacodb",
        ############################################################## TEST
        host="194.164.63.79",
        port=3306,
        database="allestacoDB"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

## END DB



# Fix for Proxy
taco.wsgi_app = ProxyFix(
    taco.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


# Default ok for 200
default_ok = {"status": "ok"}



# Executor with senetization
# Example:
# SELECT ? FROM artikel WHERE id=?, ["preis","1"]
def execute_query(query: str, param: list) -> json:
    try:
        cur.execute(query, param)
        #result_string = "\n".join([str(row[0]) for row in result])
        ############################ CRASH HIER BEI INSERT!
        ## bsp: INSERT INTO benutzer(vorname, nachname, benutzername, email, rolle, password_encrypt) VALUES ("test","test","test","test","käufer","test"); 
        ## Abfrage einbauen ob SELECT oder -> INSERT bzw. ohne Return Value
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        result = [dict(zip(columns, row)) for row in data]
        result_json = json.dumps(result, indent=2)
    except mariadb.Error as e:
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
        ##### RETURN FOR ERROR???
    return result_json

def is_json_empty(json_obj):
    return len(json_obj) <= 2


def json_exctract_and_validate(json_obj:json, keys: list):
    result = {}
    for key in keys:
        try:
            result[key] = json_obj[0].get(key)
        except Exception as e:
            print(e)
            return False
    return result

# sort parameters for sql query
def sort_parameters(input: dict, sort:list) -> list:
    out = []
    for item in sort:
        if item in input:
            out.append(input[item])
        else:
            print("Item not found: " + item)
    return out


### Routes

### Routes for testing  #######
@taco.route('/v1/system/status/api', methods=['GET'])
def taco_test():
    return "Mit der API ist alles Taco!"

@taco.route('/v1/system/status/db', methods=['GET'])
def taco_test_db():
    try:
        cur.execute("SELECT name FROM taco_stack_test LIMIT 1")
        result = cur.fetchall()
        result_string = "\n".join([str(row[0]) for row in result])
    except mariadb.Error as e:
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
    print(result_string) ##### DEBUG
    return result_string

### End testing

# Favicon, because we can. And less errors for modern browsers
@taco.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(taco.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@taco.route('/v1/login', methods=['POST'])
def login():
    pass

@taco.route('/v1/logoff', methods=['POST'])
def logoff():
    pass

@taco.route('/v1/user/username/check/<username>', methods=['POST','GET'])
def check_username(username):
    if is_json_empty(execute_query("SELECT benutzer_id FROM benutzer WHERE benutzername=?", [username])):
        return "False"
    return "True"

@taco.route('/v1/user/register', methods=['POST'])
def register():
    json_data = request.get_json()
    needed_parameters = ["vorname", "nachname", "benutzername", "email", "rolle", "password_encrypt"]
    data = json_exctract_and_validate(json_data, needed_parameters)
    print(data) ############
    if not data:
        return "Error"
    data = sort_parameters(data, needed_parameters)
    result = execute_query("INSERT INTO benutzer(vorname, nachname, benutzername, email, rolle, password_encrypt) VALUES (?, ?, ?, ?, ?, ?)", data)
    print(result)
    #return str(result)
    return "bla"

@taco.route('/v1/article/get', methods=['POST'])
def get_article():
    pass

@taco.route('/v1/article/add', methods=['POST'])
def new_article():
    pass

@taco.route('/v1/article/delete', methods=['POST'])
def delete_article():
    pass

@taco.route('/v1/cart/get', methods=['POST'])
def get_cart():
    pass

@taco.route('/v1/cart/add', methods=['POST'])
def add_cart():
    pass

@taco.route('/v1/cart/remove', methods=['POST'])
def remove_cart():
    pass



# Gerneric errror handler
@taco.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__': # pragma: no cover
    # Disable debug, when deployed in a container, for production use
    debug = False
    debug = True ###############################################################################################
    if len( sys.argv ) > 1:
        first_arg = str(sys.argv[1])
        if first_arg.lower() == "debug":
            debug=True
            print("Debug enabled!")
    
    # Logging
    #sys.stdout = open('logs/flask_output.log', 'w')
    sys.stderr = open('logs/flask_error.log', 'w')

    # Run
    taco.run(host='0.0.0.0', port=5000, debug=debug)