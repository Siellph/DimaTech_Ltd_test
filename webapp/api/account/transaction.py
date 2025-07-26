from sanic import Request, json
from sanic.log import logger
from sanic_ext.extensions.openapi import openapi

from webapp import ErrorResponse, protected
from webapp.api.account.router import bp_transaction
from webapp.crud import transaction as crud_transaction
from webapp.schema.account.transaction import TransactionCreate, TransactionRead
from webapp.utils.signature import check_signature


@bp_transaction.get('/my/<account_id:int>')
@openapi.secured('token')
@openapi.description('Get transactions by account ID')
@openapi.response(status=200, content=TransactionRead, description='List of transactions for the specified account')
@openapi.response(status=404, content=ErrorResponse, description='No transactions found for the specified account')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@protected()
async def get_transactions_by_account(request: Request, account_id: int):
    logger.info('Received request to get transactions for account %d', account_id)
    user = request.ctx.user

    async with request.ctx.session as session:
        transactions = await crud_transaction.get_transactions_by_account_id(session, account_id, user['user_id'])
        if not transactions:
            logger.info('No transactions found for account %d', account_id)
            return json({'error': 'No transactions found for this account'}, status=404)

    logger.info('Transactions retrieved for account %d', account_id)
    return json(
        [
            TransactionRead.model_validate(transaction, from_attributes=True).model_dump(mode='json')
            for transaction in transactions
        ]
    )


@bp_transaction.get('/my')
@openapi.secured('token')
@openapi.description('Get all transactions for the authenticated user')
@openapi.response(status=200, content=TransactionRead, description='List of transactions for the authenticated user')
@openapi.response(status=404, content=ErrorResponse, description='No transactions found for the user')
@openapi.response(status=401, content=ErrorResponse, description='User not authenticated')
@protected()
async def get_transactions(request: Request):
    user_id = request.ctx.user['user_id'] if request.ctx.user else 'unknown'
    logger.info('Received request to get transactions for user %d', user_id)

    async with request.ctx.session as session:
        transactions = await crud_transaction.get_transactions_by_user_id(session, request.ctx.user['user_id'])
        if not transactions:
            logger.info('No transactions found for user %d', request.ctx.user['user_id'])
            return json({'error': 'No transactions found for this user'}, status=404)
    logger.info('Transactions retrieved for user %d', request.ctx.user['user_id'])
    return json(
        [
            TransactionRead.model_validate(transaction, from_attributes=True).model_dump(mode='json')
            for transaction in transactions
        ]
    )


@bp_transaction.post('/webhook/payment')
@openapi.body(TransactionCreate)
@openapi.description('Create a new transaction')
@openapi.response(status=201, content=TransactionRead, description='Transaction created successfully')
@openapi.response(status=400, content=ErrorResponse, description='Invalid transaction data or signature')
async def create_transaction(request: Request):
    logger.info('Received transaction creation request: %s', request.json)

    transaction_data = request.json

    if not check_signature(transaction_data):
        logger.error('Invalid signature for transaction data: %r', transaction_data)
        return json({'error': 'Invalid signature'}, status=400)

    async with request.ctx.session as session:
        try:
            transaction = await crud_transaction.create_transaction(session, transaction_data)
        except ValueError as e:
            logger.error('Transaction creation failed: %s', str(e))
            return json({'error': str(e)}, status=400)
    logger.info('Transaction created successfully: %s', transaction.transaction_id)
    return json(TransactionRead.model_validate(transaction, from_attributes=True).model_dump(mode='json'), status=201)
