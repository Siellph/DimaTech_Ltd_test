from sanic import Blueprint, Sanic
from sqlalchemy.ext.asyncio import AsyncSession

from conf import MySanicConfig
from webapp.api.account.router import bp_account, bp_transaction
from webapp.api.login.router import bp_auth, bp_user
from webapp.db.postgres import async_session


def create_app() -> Sanic:
    app = Sanic('BillingApp', config=MySanicConfig())

    @app.middleware('request')
    async def open_session(request):
        request.ctx.session = await async_session().__aenter__()

    @app.middleware('response')
    async def close_session(request, response):
        session: AsyncSession = getattr(request.ctx, 'session', None)
        if session:
            await session.__aexit__(None, None, None)

    content = Blueprint.group(bp_user, bp_auth, bp_account, bp_transaction, url_prefix='/api/v1')
    app.blueprint(content)

    app.ext.openapi.add_security_scheme(
        'token',
        'http',
        scheme='bearer',
        bearer_format='JWT',
    )

    return app
