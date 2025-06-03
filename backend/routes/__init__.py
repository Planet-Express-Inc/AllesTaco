# Static
from .static import static_bp

# Get Blueprints from v1
from .v1 import v1_blueprints

def register_blueprints(app):
    # Load default static (no version)
    app.register_blueprint(static_bp)
    # Load v1 bps
    for bp in v1_blueprints:
        app.register_blueprint(bp)
        print("Loaded (v1): " + bp.name)