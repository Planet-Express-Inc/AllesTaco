import sys

from flask import Flask
from flask_cors import CORS
import json

from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

# Uitltys
from functions import *

# Config
from config import *

# Blueprints
from routes import register_blueprints

# Flasgger
from swagger import *

# Create App
taco = Flask(__name__)

# Start Swagger/flasgger
swagger = implement_swagger(taco, swagger_config, 'swagger/swagger.yaml')

# CORS
CORS(taco, supports_credentials=True, origins=origins)

# Same Site bug
taco.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

# Fix for Proxy
taco.wsgi_app = ProxyFix(
    taco.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Secret for sessions
taco.secret_key = secret_key

### Routes
# Get from Blueprints
register_blueprints(taco)

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

# When not imported
if __name__ == '__main__':
    # Disable debug, when deployed in a container, for production use
    debug = False
    if len( sys.argv ) > 1:
        first_arg = str(sys.argv[1])
        if first_arg.lower() == "debug":
            debug=True
            print("Debug enabled!")
    
    # Logging
    if not debug:
        sys.stdout = open('logs/flask_output.log', 'w')
    sys.stderr = open('logs/flask_error.log', 'w')

    # Run
    taco.run(host='0.0.0.0', port=5000, debug=debug)