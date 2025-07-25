from sanic import Blueprint

bp_account = Blueprint('account', url_prefix='/api/user')
bp_transaction = Blueprint('transaction', url_prefix='/api/auth')
