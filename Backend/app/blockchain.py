import os
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
import json

load_dotenv()

# Carregar variáveis de ambiente
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
ADMIN_ADDRESS = os.getenv('ADMIN_ADDRESS')
ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY')
BLOCKCHAIN_URL = os.getenv('BLOCKCHAIN_URL')
CONTRACT_ABI_PATH = os.getenv('CONTRACT_ABI_PATH')

# Conectar-se à blockchain
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))

# Se estiver usando uma rede que requer o middleware POA (ex: Hardhat)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if not w3.isConnected():
    raise Exception("Não foi possível conectar à blockchain.")

# Carregar o ABI do contrato
with open(CONTRACT_ABI_PATH) as f:
    contract_data = json.load(f)
    contract_abi = contract_data['abi']

# Instanciar o contrato
contract = w3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=contract_abi)

def register_certificate(certificate_hash, student_name, issue_date, issuer_private_key):
    issuer_account = w3.eth.account.from_key(issuer_private_key)
    issuer_address = issuer_account.address
    nonce = w3.eth.get_transaction_count(issuer_address)

    txn = contract.functions.registerCertificate(
        certificate_hash,
        student_name,
        issue_date
    ).build_transaction({
        'from': issuer_address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.toWei('20', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=issuer_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt, issuer_address

def get_certificate(certificate_hash):
    try:
        cert = contract.functions.getCertificate(certificate_hash).call()
        return {
            'studentName': cert[0],
            'issueDate': cert[1],
            'issuerAddress': cert[2]
        }
    except Exception as e:
        # Certificado não encontrado
        return None

def transfer_admin(new_admin_address):
    nonce = w3.eth.get_transaction_count(ADMIN_ADDRESS)

    txn = contract.functions.transferAdmin(Web3.toChecksumAddress(new_admin_address)).build_transaction({
        'from': ADMIN_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.toWei('20', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=ADMIN_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt