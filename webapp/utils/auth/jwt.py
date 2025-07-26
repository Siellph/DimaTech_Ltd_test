import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TypedDict, cast

from authlib.jose import JoseError, jwt
from sanic.exceptions import Unauthorized
from sanic.request import Request

from conf import settings


class JwtTokenT(TypedDict):
    uid: str
    exp: int
    user_id: int
    role: str


@dataclass
class JwtAuth:
    secret: str
    alg: str = 'HS256'

    def create_token(self, user_id: int, role: str) -> str:
        payload = {
            'uid': uuid.uuid4().hex,
            'exp': int((datetime.now(timezone.utc) + timedelta(days=6)).timestamp()),
            'user_id': user_id,
            'role': role,
        }
        return jwt.encode({'alg': self.alg}, payload, self.secret).decode('utf-8')

    def decode_token(self, token: str) -> JwtTokenT:
        try:
            claims = jwt.decode(token, self.secret)
            claims.validate()  # проверка exp и других полей
            return cast(JwtTokenT, claims)
        except JoseError:
            raise Unauthorized('Invalid or expired token')

    def get_current_user(self, request: Request) -> JwtTokenT:
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise Unauthorized('Missing or invalid Authorization header. Unauthorized.')

        token = auth_header.split(' ', 1)[1]
        return self.decode_token(token)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)
