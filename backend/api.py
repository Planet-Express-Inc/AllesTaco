import sys

from flask import Flask, request, jsonify
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
        user="tacotest",
        password="sicheres_passwort123",
        host="tacodb",
        port=3306,
        database="taco_stack_test"

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


### Routes
@taco.route('/taco', methods=['GET'])
def taco_test():
    return "Mit der API ist alles Taco!"

@taco.route('/tacodb', methods=['GET'])
def taco_test_db():
    try:
        cur.execute("SELECT name FROM taco_stack_test LIMIT 1")
        result = cur.fetchall()
        result_string = "\n".join([str(row[0]) for row in result])
    except mariadb.Error as e:
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
    return result_string


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
    sys.stdout = open('logs/flask_output.log', 'w')
    sys.stderr = open('logs/flask_error.log', 'w')

    # Run
    taco.run(host='0.0.0.0', port=5000, debug=debug)