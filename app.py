import os
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, csrf
from views import register_blueprints
import models # Ensure all SQLAlchemy models are registered

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints from views/
    register_blueprints(app)

    # Context processors
    @app.context_processor
    def inject_cart_count():
        from flask_login import current_user
        if current_user.is_authenticated and current_user.cart:
            return {'cart_count': current_user.cart.get_total_count()}
        return {'cart_count': 0}

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('base.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('base.html'), 500

    # Auto create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    # Initialize DB & Seed data if empty
    from seed_data import seed_database
    with app.app_context():
        seed_database()
    print("=======================================================")
    print("  관광지 안내 사이트 Flask 애플리케이션 시작 (http://localhost:5000)")
    print("=======================================================")
    app.run(debug=True, host='0.0.0.0', port=5000)

