from sanic import Blueprint

bp_user = Blueprint('user', url_prefix='/user')
bp_auth = Blueprint('auth', url_prefix='/auth')
