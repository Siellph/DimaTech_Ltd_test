from sanic import Blueprint

bp_account = Blueprint('account', url_prefix='/account')
bp_transaction = Blueprint('transaction', url_prefix='/transaction')
