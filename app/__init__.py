from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='secret')
    app.config['UPLOAD_FOLDER'] = './uploads'
    # max file size 5mb
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import form
    app.register_blueprint(form.bp)

    return app
