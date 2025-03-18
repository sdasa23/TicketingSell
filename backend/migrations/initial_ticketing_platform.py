from web3 import HTTPProvider, Web3
import json
import time
import os
from solcx import compile_standard, install_solc

# connect to Ganache test network
def initial_env(web3_address:str ,chain_id:int, publisher_account_hash:str, userKey:str, contracts_path: str):
    w3 = Web3(HTTPProvider(web3_address))
    block = w3.eth.get_block('latest')

    userAcc = w3.to_checksum_address(publisher_account_hash)

    Migrations = os.path.join(contracts_path, "Migrations.sol")
    with open(Migrations, "r") as file:
        Migrations = file.read()

    FestToken = os.path.join(contracts_path, "FestToken.sol")
    with open(FestToken, "r") as file:
        FestToken = file.read()

    FestiveTicketsFactory = os.path.join(contracts_path, "FestiveTicketsFactory.sol")
    with open(FestiveTicketsFactory, "r") as file:
        FestiveTicketsFactory = file.read()

    FestivalNFT = os.path.join(contracts_path, "FestivalNFT.sol")
    with open(FestivalNFT, "r") as file:
        FestivalNFT = file.read()

    FestivalMarketplace = os.path.join(contracts_path, "FestivalMarketplace.sol")
    with open(FestivalMarketplace, "r") as file:
        FestivalMarketplace = file.read()


    install_solc("0.8.29")

    # compile the solidity files by sole
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Migrations.sol": {"content": Migrations},
                        "FestToken.sol": {"content": FestToken},
                        "FestiveTicketsFactory.sol": {"content": FestiveTicketsFactory},
                        "FestivalNFT.sol": {"content": FestivalNFT},
                        "FestivalMarketplace.sol": {"content": FestivalMarketplace},
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

    bytecode = compiled_sol["contracts"]["FestToken.sol"]["FestToken"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["FestToken.sol"]["FestToken"]["abi"]

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

web3_address = 'http://127.0.0.1:8545'
publisher_account_hash = '0xC459cc3AC9f8462Be2EF00aAD02fAc7af2e97b14'
userKey = '0xda09f8cdec20b7c8334ce05b27e6797bef01c1ad79c59381666467552c5012e3'
chain_id = 1337
contracts_path = "../contracts"
token_contract_address = initial_env(web3_address,chain_id, publisher_account_hash, userKey, contracts_path)
print(token_contract_address)