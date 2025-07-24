from sanic import Sanic

from conf import MySanicConfig
from webapp.api.login.router import bp_user


def create_app() -> Sanic:
    app = Sanic('BillingApp', config=MySanicConfig())
    app.blueprint(bp_user)
    return app
