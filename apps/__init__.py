from flask import Flask, request

from flask_login import LoginManager

login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)
    #app.config.from_object(config)
    if config is not None:
        app.config.from_pyfile(config)
    # send CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
                ##response.headers['Authorization'] = 'xiaominggessdfs3432ds34ds32432cedsad332e23'
        return response

    from apps.Auth.Users import db
    db.init_app(app)

    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    from apps.Portal.Entrance import init_api
    init_api(app)

    return app
