from flask import Flask

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # [Optional] Configure your Flask app here
    # app.config['SOME_SETTING'] = 'some value'

    # Import and register your blueprints or routes here
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    return app
