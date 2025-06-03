from .user import user_bp
from .article import article_bp
from .status import status_bp
from .cart import cart_bp
from .user_purchase import user_purchase_bp
from .article_views import article_views_bp

v1_blueprints = [user_bp, article_bp, status_bp, cart_bp, user_purchase_bp, article_views_bp]