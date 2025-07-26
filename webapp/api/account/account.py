from sanic import Request, json
from sanic.log import logger
from sanic_ext.extensions.openapi import openapi

from webapp import ErrorResponse, protected
from webapp.api.account.router import bp_account
from webapp.crud import account as crud_account
from webapp.schema.account.account import AccountRead, AccountsReadShort, AccountUpdate


@bp_account.get('/my/<account_id:int>')
@openapi.secured('token')
@openapi.description('Get account details by ID')
@openapi.response(status=200, content=AccountRead, description='Account details')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=404, content=ErrorResponse, description='Account not found or does not belong to the user')
@protected()
async def get_account(request: Request, account_id: int):
    user = request.ctx.user
    logger.info('Fetching account. User: %s, Account ID: %d', user, account_id)

    async with request.ctx.session as session:
        account = await crud_account.get_account_by_id(session, account_id, user['user_id'])
        account = AccountRead.model_validate(account, from_attributes=True).model_dump(mode='json')
        if not account:
            logger.warning('Account not found. Account ID: %d, User ID: %d', account_id, user['user_id'])
            return json({'error': 'Account not found'}, status=404)

    logger.info('Account fetched successfully by user %d. Account ID: %d', user['user_id'], account_id)
    return json(account)


@bp_account.patch('/my/<account_id:int>/update')
@openapi.secured('token')
@openapi.description('Update account details')
@openapi.body(AccountUpdate, required=True)
@openapi.response(status=200, content=AccountRead, description='Updated account details')
@openapi.response(status=400, content=ErrorResponse, description='Invalid input data')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@protected()
async def update_account(request: Request, account_id: int):
    user = request.ctx.user
    logger.info('Updating account. User: %s, Account ID: %d', user, account_id)

    async with request.ctx.session as session:
        account_data = AccountUpdate.model_validate(request.json, from_attributes=True)
        try:
            account = await crud_account.update_account(session, account_id, account_data, user['user_id'])
            account = AccountRead.model_validate(account, from_attributes=True).model_dump(mode='json')
        except ValueError as e:
            logger.error('Error updating account: %s', str(e))
            return json({'error': str(e)}, status=400)
    logger.info('Account updated successfully. User: %s, Account ID: %d', user, account_id)
    return json(account)


@bp_account.get('/my')
@openapi.secured('token')
@openapi.description('Get all accounts for the authenticated user')
@openapi.response(status=200, content=AccountsReadShort, description='List of accounts')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@openapi.response(status=404, content=ErrorResponse, description='No accounts found for the user')
@protected()
async def get_my_accounts(request: Request):
    user = request.ctx.user
    logger.info('Fetching all accounts for user: %s', user)

    async with request.ctx.session as session:
        accounts = await crud_account.get_accounts_by_user_id(session, user['user_id'])
        logger.debug('Accounts fetched: %s', accounts)
    if not accounts:
        logger.warning('No accounts found for user: %d', user['user_id'])
        return json({'error': 'No accounts found for this user'}, status=404)

    logger.info('Accounts returned for user: %d', user['user_id'])
    return json(
        [
            AccountsReadShort.model_validate(account, from_attributes=True).model_dump(mode='json')
            for account in accounts
        ]
    )
