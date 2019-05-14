import os
from flask import Flask


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=False)
    # existing code omitted

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import dpp

    @app.route('/')
    def index():
        return 'This is Python Doodle DPP_09'

    app.register_blueprint(dpp.bp, url_prefix='/doodle')

    return app
