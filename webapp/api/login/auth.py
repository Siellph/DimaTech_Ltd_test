from sanic import Request
from sanic.log import logger
from sanic.response import json
from sanic_ext.extensions.openapi import openapi

from webapp import ErrorResponse
from webapp.api.login.router import bp_auth
from webapp.crud.user import get_user_by_email
from webapp.schema.login.auth import LoginRequest, LoginResponse
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import verify_password


@bp_auth.post('/login')
@openapi.body({'application/json': LoginRequest})
@openapi.description('User login endpoint')
@openapi.response(status=200, content=LoginResponse, description='Login successful')
@openapi.response(status=400, content=ErrorResponse, description='Invalid login data')
@openapi.response(status=401, content=ErrorResponse, description='Invalid email or password')
async def login(request: Request):
    logger.info('Login attempt received')
    try:
        data = LoginRequest(**request.json)
    except Exception as e:
        logger.warning('Invalid login data: %s', e)
        return json({'error': 'Invalid data'}, status=400)

    async with request.ctx.session as session:
        user = await get_user_by_email(session, data.email)
        if not user:
            logger.warning('Login failed: user not found (%s)', data.email)
            return json({'error': 'Invalid email or password'}, status=401)
        if not verify_password(data.password, user.hashed_password):
            logger.warning('Login failed: invalid password for %s', data.email)
            return json({'error': 'Invalid email or password'}, status=401)

        token = jwt_auth.create_token(user.user_id, user.role)
        logger.info('User %s logged in successfully', data.email)
        return json(LoginResponse(access_token=token).model_dump())
