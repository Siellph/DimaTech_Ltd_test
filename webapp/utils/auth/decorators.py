from functools import wraps

from sanic.exceptions import Unauthorized
from sanic.log import logger
from sanic.request import Request
from sanic.response import json

from webapp.utils.auth.jwt import jwt_auth


def protected():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                user_data = jwt_auth.get_current_user(request)
                request.ctx.user = user_data
            except Unauthorized as e:
                logger.warning('Protected route %s is not authorized', request.path)
                return json({'error': str(e)}, status=401)
            logger.info('User %s accessed protected route %s', request.ctx.user.get('user_id'), request.path)
            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator
