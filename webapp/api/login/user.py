from sanic import Request
from sanic.log import logger
from sanic.response import HTTPResponse, json
from sanic_ext.extensions.openapi import openapi

from webapp import ErrorResponse, protected
from webapp.api.login.router import bp_user
from webapp.crud import user as crud_user
from webapp.schema.login.user import UserCreate, UserRead, UserUpdate


@bp_user.post('/')
@openapi.body({'application/json': UserCreate})
@openapi.secured('token')
@openapi.description('Create a new user')
@openapi.response(status=201, content=UserRead, description='User created successfully')
@openapi.response(status=400, content=ErrorResponse, description='Invalid request body')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=403, content=ErrorResponse, description='Access denied. Only admin user')
@protected()
async def create_user(request: Request):
    user = request.ctx.user
    logger.info('User %s attempts to create a new user', user.get('user_id'))
    if user['role'] != 'admin':
        logger.warning('Access denied for user %s: not admin', user.get('user_id'))
        return json({'error': 'Access denied. Only admin user'}, status=403)
    try:
        user_in = UserCreate(**request.json)
        async with request.ctx.session as session:
            db_user = await crud_user.create_user(session, user_in)
        logger.info('User %s created new user %s', user.get('user_id'), db_user.user_id)
        return json(UserRead.model_validate(db_user, from_attributes=True).model_dump(mode='json'), status=201)
    except ValueError as e:
        logger.error('ValueError while creating user by %s: %s', user.get('user_id'), str(e))
        return json({'error': str(e)}, status=400)
    except Exception as e:
        logger.exception('Internal Server Error while creating user by %s: %s', user.get('user_id'), str(e))
        return json({'error': 'Internal Server Error'}, status=500)


@bp_user.get('/')
@openapi.secured('token')
@openapi.description('List all users')
@openapi.response(status=200, content=UserRead, description='List of users')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=403, content=ErrorResponse, description='Access denied. Only admin user')
@protected()
async def list_users(request: Request):
    user = request.ctx.user
    logger.info('User %s requests user list', user.get('user_id'))
    if user['role'] != 'admin':
        logger.warning('Access denied for user %s: not admin', user.get('user_id'))
        return json({'error': 'Access denied. Only admin user'}, status=403)
    async with request.ctx.session as session:
        users = await crud_user.get_all_users(session)
        logger.info('User %s listed all users', user.get('user_id'))
        return json([UserRead.model_validate(user, from_attributes=True).model_dump(mode='json') for user in users])


@bp_user.delete('/<user_id:int>')
@openapi.secured('token')
@openapi.description('Delete a user')
@openapi.response(status=204, description='User deleted successfully')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=403, content=ErrorResponse, description='Access denied. Only admin user')
@openapi.response(status=404, content=ErrorResponse, description='User not found')
@protected()
async def delete_user(request: Request, user_id: int):
    user = request.ctx.user
    logger.info('User %d attempts to delete user %d', user.get('user_id'), user_id)
    if user['role'] != 'admin':
        logger.warning('Access denied for user %d: not admin', user.get('user_id'))
        return json({'error': 'Access denied. Only admin user'}, status=403)
    async with request.ctx.session as session:
        deleted = await crud_user.delete_user(session, user_id)
        if not deleted:
            logger.warning('User %d not found for deletion by %d', user_id, user.get('user_id'))
            return json({'error': 'User not found'}, status=404)
    logger.info('User %d deleted user %d', user.get('user_id'), user_id)
    return HTTPResponse(status=204)


@bp_user.get('/<user_id:int>')
@openapi.secured('token')
@openapi.description('Get user details by ID')
@openapi.response(status=200, content=UserRead, description='User details')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=403, content=ErrorResponse, description='Access denied. Only admin user')
@openapi.response(status=404, content=ErrorResponse, description='User not found')
@protected()
async def get_user(request: Request, user_id: int):
    user = request.ctx.user
    logger.info('User %d requests info for user %d', user.get('user_id'), user_id)
    if user['role'] != 'admin':
        logger.warning('Access denied for user %d: not admin', user.get('user_id'))
        return json({'error': 'Access denied. Only admin user'}, status=403)
    async with request.ctx.session as session:
        user_db = await crud_user.get_user_by_id(session, user_id)
        if not user_db:
            logger.warning('User %d not found (requested by %d)', user_id, user.get('user_id'))
            return json({'error': 'User not found'}, status=404)
    logger.info('User %d retrieved info for user %d', user.get('user_id'), user_id)
    return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))


@bp_user.patch('/update/<user_id:int>')
@openapi.secured('token')
@openapi.body({'application/json': UserUpdate})
@openapi.description('Update user details')
@openapi.response(status=200, content=UserRead, description='User updated successfully')
@openapi.response(status=400, content=ErrorResponse, description='Invalid input data')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=403, content=ErrorResponse, description='Access denied. Only admin user')
@openapi.response(status=404, content=ErrorResponse, description='User not found')
@protected()
async def update_user(request: Request, user_id: int):
    user = request.ctx.user
    logger.info('User %d attempts to update user %d', user.get('user_id'), user_id)
    if user['role'] != 'admin':
        logger.warning('Access denied for user %d: not admin', user.get('user_id'))
        return json({'error': 'Access denied. Only admin user'}, status=403)
    async with request.ctx.session as session:
        try:
            user_db = await crud_user.update_user(session, user_id, UserUpdate(**request.json))
            if not user_db:
                logger.warning('User %d not found for update by %d', user_id, user.get('user_id'))
                return json({'error': 'User not found'}, status=404)
        except ValueError as e:
            logger.error('ValueError while updating user %d by %d: %s', user_id, user.get('user_id'), str(e))
            return json({'error': str(e)}, status=400)
        logger.info('User %d updated user %d', user.get('user_id'), user_id)
        return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))


@bp_user.patch('/me/update')
@openapi.secured('token')
@openapi.body({'application/json': UserUpdate})
@openapi.description('Update own user details')
@openapi.response(status=200, content=UserRead, description='User updated successfully')
@openapi.response(status=400, content=ErrorResponse, description='Invalid input data')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=404, content=ErrorResponse, description='User not found')
@protected()
async def update_me(request: Request):
    user = request.ctx.user
    logger.info('User %d attempts to update own profile', user.get('user_id'))

    async with request.ctx.session as session:
        try:
            user_db = await crud_user.update_user(session, user['user_id'], UserUpdate(**request.json))
            if not user_db:
                logger.warning('User %d not found for self-update', user.get('user_id'))
                return json({'error': 'User not found'}, status=404)
        except ValueError as e:
            logger.error('ValueError while updating self (%d): %s', user.get('user_id'), str(e))
            return json({'error': str(e)}, status=400)
        logger.info('User %d updated own profile', user.get('user_id'))
        return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))


@bp_user.get('/me')
@openapi.secured('token')
@openapi.description('Get own user details')
@openapi.response(status=200, content=UserRead, description='User details')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=404, content=ErrorResponse, description='User not found')
@protected()
async def me(request: Request):
    user = request.ctx.user
    logger.info('User %d requests own profile', user.get('user_id'))

    async with request.ctx.session as session:
        user_db = await crud_user.get_user_by_id(session, user['user_id'])
        if not user_db:
            logger.warning('User %d not found for /me', user.get('user_id'))
            return json({'error': 'User not found'}, status=404)
        logger.info('User %d retrieved own profile', user.get('user_id'))
        return json(UserRead.model_validate(user_db, from_attributes=True).model_dump(mode='json'))
