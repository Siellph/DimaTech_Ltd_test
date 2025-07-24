from sanic import Request
from sanic.response import json
from sanic_ext.extensions.openapi import openapi

from webapp.api.login.router import bp_user
from webapp.crud import user as crud_user
from webapp.db.postgres import async_session
from webapp.schema.login.user import UserCreate, UserRead


@bp_user.post('/')
@openapi.body({'application/json': UserCreate})
async def create_user(request: Request):
    try:
        user_in = UserCreate(**request.json)

        async with async_session() as session:
            db_user = await crud_user.create_user(session, user_in)

        return json(UserRead.model_validate(db_user, from_attributes=True).model_dump(mode='json'), status=201)

    except ValueError as e:
        return json({'error': str(e)}, status=400)

    except Exception as e:
        return json({'error': f'Internal Server Error {e}'}, status=500)


@bp_user.get('/')
async def list_users(request: Request):
    async with async_session() as session:
        users = await crud_user.get_all_users(session)
        return json([UserRead.model_validate(user, from_attributes=True).model_dump(mode='json') for user in users])
