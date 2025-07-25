from sanic import Request, json
from sanic_ext.extensions.openapi import openapi

from webapp import protected
from webapp.api.account.router import bp_transaction
from webapp.crud import transaction as crud_transaction
from webapp.schema.account.transaction import TransactionRead


@bp_transaction.get('/my/<account_id:int>')
@openapi.secured('token')
@protected()
async def get_transactions_by_account(request: Request, account_id: int):
    user = request.ctx.user
    if not user:
        return json({'error': 'User not authenticated'}, status=401)

    async with request.ctx.session as session:
        transactions = await crud_transaction.get_transactions_by_account_id(session, account_id, user['user_id'])
        if not transactions:
            return json({'error': 'No transactions found for this account'}, status=404)

    return json(
        [
            TransactionRead.model_validate(transaction, from_attributes=True).model_dump(mode='json')
            for transaction in transactions
        ]
    )


@bp_transaction.get('/my')
@openapi.secured('token')
@protected()
async def get_transactions(request: Request):
    if not request.ctx.user:
        return json({'error': 'User not authenticated'}, status=401)

    async with request.ctx.session as session:
        transactions = await crud_transaction.get_transactions_by_user_id(session, request.ctx.user['user_id'])
        if not transactions:
            return json({'error': 'No transactions found for this user'}, status=404)
    return json(
        [
            TransactionRead.model_validate(transaction, from_attributes=True).model_dump(mode='json')
            for transaction in transactions
        ]
    )
