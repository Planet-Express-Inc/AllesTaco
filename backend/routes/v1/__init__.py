from .user import user_bp
from .article import article_bp
from .status import status_bp
from .user_cart import user_cart_bp
from .user_purchase import user_purchase_bp
from .user_reviews import user_reviews_bp
from .article_views import article_views_bp

v1_blueprints = [user_bp, article_bp, status_bp, user_cart_bp, user_purchase_bp, user_reviews_bp, article_views_bp]