from web3 import HTTPProvider, Web3
import json
import time
import os
from solcx import compile_standard, install_solc

web3_address = 'http://127.0.0.1:8545'
publisher_account_hash = '0xC459cc3AC9f8462Be2EF00aAD02fAc7af2e97b14'
userKey = '0xda09f8cdec20b7c8334ce05b27e6797bef01c1ad79c59381666467552c5012e3'
chain_id = 1337
contracts_path = "../contracts"

# connect to Ganache test network
w3 = Web3(HTTPProvider(web3_address))

def initial_env():
    Migrations = os.path.join(contracts_path, "Migrations.sol")
    with open(Migrations, "r") as file:
        Migrations = file.read()

    EventToken = os.path.join(contracts_path, "EventToken.sol")
    with open(EventToken, "r") as file:
        EventToken = file.read()

    EventTicketsFactory = os.path.join(contracts_path, "EventTicketsFactory.sol")
    with open(EventTicketsFactory, "r") as file:
        EventTicketsFactory = file.read()

    EventNFT = os.path.join(contracts_path, "EventNFT.sol")
    with open(EventNFT, "r") as file:
        EventNFT = file.read()

    EventMarketplace = os.path.join(contracts_path, "EventMarketplace.sol")
    with open(EventMarketplace, "r") as file:
        EventMarketplace = file.read()
    install_solc("0.8.29")

    # compile the solidity files by sole
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Migrations.sol": {"content": Migrations},
                        "EventToken.sol": {"content": EventToken},
                        "EventTicketsFactory.sol": {"content": EventTicketsFactory},
                        "EventNFT.sol": {"content": EventNFT},
                        "EventMarketplace.sol": {"content": EventMarketplace},
                        },
            "settings": {
                "evmVersion": "istanbul",
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        allow_paths = ["../node_modules/"],
        base_path="../node_modules/",
        solc_version="0.8.29",
    )
       #initial the token
    with open("../artifacts/compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)


def createTokenContract():
    userAcc = w3.to_checksum_address(publisher_account_hash)
    with open("../artifacts/compiled_code.json", "r") as file:
        compiled_sol = json.load(file)
    
    bytecode = compiled_sol["contracts"]["EventToken.sol"]["EventToken"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["EventToken.sol"]["EventToken"]["abi"]

    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(userAcc)

    transaction = SimpleStorage.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": userAcc,
            "nonce": nonce,
            "gas": 20000000
        }
    )

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=userKey)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # return token address
    return tx_receipt["contractAddress"]

initial_env()
token_contract_address = createTokenContract()
print(token_contract_address)