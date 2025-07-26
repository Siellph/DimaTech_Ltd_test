import hashlib

from conf import settings


def check_signature(data: dict) -> bool:
    keys_order = ['account_id', 'amount', 'transaction_id', 'user_id']
    raw_string = ''.join(str(data[k]) for k in keys_order) + settings.SECRET_KEY
    gen_signature = hashlib.sha256(raw_string.encode()).hexdigest()
    return data.get('signature') == gen_signature
