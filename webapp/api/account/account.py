from sanic import Request, json
from sanic_ext.extensions.openapi import openapi

from webapp import protected
from webapp.api.account.router import bp_account
from webapp.crud import account as crud_account
from webapp.schema.account.account import AccountCreate, AccountRead, AccountsReadShort


@bp_account.post('/create')
@openapi.body({'application/json': AccountCreate})
@openapi.secured('token')
@protected()
async def create_account(request: Request):
    user = request.ctx.user
    if not user:
        return json({'error': 'User not authenticated'}, status=401)

    try:
        account_in = AccountCreate(**request.json)
    except ValueError as e:
        return json({'error': str(e)}, status=400)

    async with request.ctx.session as session:
        account = await crud_account.create_account(session, account_in, user['user_id'])

    return json(AccountRead.model_validate(account, from_attributes=True).model_dump(mode='json'), status=201)


@bp_account.get('/my/<account_id:int>')
@openapi.secured('token')
@protected()
async def get_account(request: Request, account_id: int):
    user = request.ctx.user
    async with request.ctx.session as session:
        if not user:
            return json({'error': 'User not authenticated'}, status=401)

        account = await crud_account.get_account_by_id(session, account_id, user['user_id'])
        if not account:
            return json({'error': 'Account not found'}, status=404)

    return json(AccountRead.model_validate(account, from_attributes=True).model_dump(mode='json'))


@bp_account.get('/my')
@openapi.secured('token')
@protected()
async def get_my_accounts(request: Request):
    user = request.ctx.user
    async with request.ctx.session as session:
        if not user:
            return json({'error': 'User not authenticated'}, status=401)

        accounts = await crud_account.get_accounts_by_user_id(session, user['user_id'])
    if not accounts:
        return json({'error': 'No accounts found for this user'}, status=404)

    return json(
        [
            AccountsReadShort.model_validate(account, from_attributes=True).model_dump(mode='json')
            for account in accounts
        ]
    )
