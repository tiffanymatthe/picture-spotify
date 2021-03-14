import flask
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024