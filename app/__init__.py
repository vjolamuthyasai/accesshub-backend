from flask import Flask


def create_app():
    app = Flask(__name__)

    # Register blueprints (routes)
    from app.services.routes.routes import main
    app.register_blueprint(main)

    return app