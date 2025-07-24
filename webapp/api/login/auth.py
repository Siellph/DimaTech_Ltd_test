from sanic import Request
from sanic.response import json
from sanic_ext.extensions.openapi import openapi

from webapp.api.login.router import bp_auth
from webapp.crud.user import get_user_by_email
from webapp.schema.login.auth import LoginRequest, LoginResponse
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import verify_password


@bp_auth.post('/login')
@openapi.body({'application/json': LoginRequest})
async def login(request: Request):
    try:
        data = LoginRequest(**request.json)
    except Exception:
        return json({'error': 'Неверные данные'}, status=400)

    async with request.ctx.session as session:
        user = await get_user_by_email(session, data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            return json({'error': 'Неверный email или пароль'}, status=401)

        token = jwt_auth.create_token(user.user_id, user.role)

        return json(LoginResponse(access_token=token).model_dump())
