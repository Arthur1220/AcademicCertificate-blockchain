from eth_account.messages import encode_defunct
from eth_account import Account

def verify_signature(address, message, signature):
    try:
        recovered_address = Account.recover_message(message, signature=signature)
        return recovered_address.lower() == address.lower()
    except:
        return False
