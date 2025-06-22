# Config for Origins

# Origins for CORS
origins=["http://127.0.0.1:5501", "http://localhost:5501", "https://allestaco.niclas-sieveneck.de"]

# Secret for cookies
secret_key = "super_secret_124g+#f43g"

# Swagger config for flasgger
swagger_config = {
    "spec": {
        "openapi": "3.0.3", 
        "info": {
            "title": "Alles Taco - 1.0",
            "description": "Alles Taco API 1.0",
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