from .main_views import main_bp
from .auth_views import auth_bp
from .product_views import product_bp
from .cart_views import cart_bp
from .order_views import order_bp
from .review_views import review_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(review_bp)

