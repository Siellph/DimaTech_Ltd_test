from sanic import Request
from sanic.response import json
from sanic_ext.extensions.openapi import openapi

from webapp import protected
from webapp.api.login.router import bp_user
from webapp.crud import user as crud_user
from webapp.schema.login.user import UserCreate, UserRead, UserUpdate


@bp_user.post('/')
@openapi.body({'application/json': UserCreate})
@openapi.secured('token')
@protected()
async def create_user(request: Request):
    user = request.ctx.user
    if user['role'] != 'admin':
        return json({'error': 'Access denied. Only admin user'}, status=403)
    try:
        user_in = UserCreate(**request.json)

        async with request.ctx.session as session:
            db_user = await crud_user.create_user(session, user_in)

        return json(UserRead.model_validate(db_user, from_attributes=True).model_dump(mode='json'), status=201)

    except ValueError as e:
        return json({'error': str(e)}, status=400)

    except Exception:
        return json({'error': 'Internal Server Error'}, status=500)


@bp_user.get('/')
@openapi.secured('token')
@protected()
async def list_users(request: Request):
    user = request.ctx.user
    if user['role'] != 'admin':
        return json({'error': 'Access denied. Only admin user'}, status=403)
    async with request.ctx.session as session:
        users = await crud_user.get_all_users(session)
        return json([UserRead.model_validate(user, from_attributes=True).model_dump(mode='json') for user in users])


@bp_user.delete('/<user_id:int>')
@openapi.secured('token')
@protected()
async def delete_user(request: Request, user_id: int):
    user = request.ctx.user
    if user['role'] != 'admin':
        return json({'error': 'Access denied. Only admin user'}, status=403)

    async with request.ctx.session as session:
        delete = await crud_user.delete_user(session, user_id)
        if delete is False:
            return json({'error': 'User not found'}, status=404)
    return json({'message': 'User deleted successfully'}, status=204)


@bp_user.get('/<user_id:int>')
@openapi.secured('token')
@protected()
async def get_user(request: Request, user_id: int):
    user = request.ctx.user
    if user['role'] != 'admin':
        return json({'error': 'Access denied. Only admin user'}, status=403)

    async with request.ctx.session as session:
        user_db = await crud_user.get_user_by_id(session, user_id)
        if not user_db:
            return json({'error': 'User not found'}, status=404)

    return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))


@bp_user.patch('/update/<user_id:int>')
@openapi.secured('token')
@openapi.body({'application/json': UserUpdate})
@protected()
async def update_user(request: Request, user_id: int):
    user = request.ctx.user
    if user['role'] != 'admin':
        return json({'error': 'Access denied. Only admin user'}, status=403)

    async with request.ctx.session as session:
        try:
            user_db = await crud_user.update_user(session, user_id, UserUpdate(**request.json))
            if not user_db:
                return json({'error': 'User not found'}, status=404)
        except ValueError as e:
            return json({'error': str(e)}, status=400)
        return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))


@bp_user.patch('/me/update')
@openapi.secured('token')
@openapi.body({'application/json': UserUpdate})
@protected()
async def update_me(request: Request):
    user = request.ctx.user
    if not user:
        return json({'error': 'User not authenticated'}, status=401)

    async with request.ctx.session as session:
        try:
            user_db = await crud_user.update_user(session, user['user_id'], UserUpdate(**request.json))
            if not user_db:
                return json({'error': 'User not found'}, status=404)
        except ValueError as e:
            return json({'error': str(e)}, status=400)
        return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))


@bp_user.get('/me')
@openapi.secured('token')
@protected()
async def me(request: Request):
    user = request.ctx.user
    async with request.ctx.session as session:
        user_db = await crud_user.get_user_by_id(session, user['user_id'])
        if not user_db:
            return json({'error': 'User not found'}, status=404)

        return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))
