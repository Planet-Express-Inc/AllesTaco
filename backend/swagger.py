from flasgger import Swagger
from flask import Flask


# TODO: Swagger?
# Swagger base config



def implement_swagger(app: Flask, swagger_config, template_file) -> Swagger:
    app.config["SWAGGER"] = swagger_config
    app.config["SWAGGER"]['openapi'] = '3.0.3'
    # Load yaml
    return Swagger(app, template_file=template_file)
