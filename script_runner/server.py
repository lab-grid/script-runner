"""Sets up a flask-restx server for running the swabseq analysis R-script."""

import os

from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_restx import Api
# https://github.com/noirbizarre/flask-restplus/issues/565#issuecomment-562610603
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__, static_folder='static', static_url_path='')
app.wsgi_app = ProxyFix(app.wsgi_app)


# Configuration ---------------------------------------------------------------

app.config['AUTH_PROVIDER'] = os.environ.get('AUTH_PROVIDER', 'auth0')
app.config['AUTH0_DOMAIN'] = os.environ.get('AUTH0_DOMAIN', '')
app.config['AUTH0_CLIENT_ID'] = os.environ.get('AUTH0_CLIENT_ID', 'Msk8I4Ad2ujE76MwOatsmmvEEds5v50h')
app.config['AUTH0_API_AUDIENCE'] = os.environ.get('AUTH0_API_AUDIENCE', '')
app.config['AUTH0_AUTHORIZATION_URL'] = os.environ.get('AUTH0_AUTHORIZATION_URL', '')
app.config['AUTH0_TOKEN_URL'] = os.environ.get('AUTH0_TOKEN_URL', '')
app.config['RESTX_JSON'] = {'cls': JSONEncoder}  # Add support for serializing datetime/date
app.config['SERVER_VERSION'] = os.environ.get('SERVER_VERSION', 'local')
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME', app.config.get('SERVER_NAME'))
# app.config['RSCRIPT_THREADS'] = int(os.environ.get('RSCRIPT_THREADS', '8'))
# app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND', None)
# app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL', None)


# API Documentation -----------------------------------------------------------

authorizations = {
    'token': {
        'type': 'oauth2',
        'flow': 'accessCode',
        'audience': app.config['AUTH0_API_AUDIENCE'],
        'domain': app.config['AUTH0_DOMAIN'],
        'clientId': app.config['AUTH0_CLIENT_ID'],
        'authorizationUrl': app.config['AUTH0_AUTHORIZATION_URL'],
        'tokenUrl': app.config['AUTH0_TOKEN_URL'],
        'scopes': {}
    }
}
api = Api(
    app,
    title='Swabseq Analysis API',
    version='0.1.0',
    authorizations=authorizations,
)
CORS(app)
