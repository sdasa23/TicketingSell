import json

class Config:
    web3_address = 'http://127.0.0.1:8545'
    admin_address = '0xC459cc3AC9f8462Be2EF00aAD02fAc7af2e97b14'
    admin_key = '0xda09f8cdec20b7c8334ce05b27e6797bef01c1ad79c59381666467552c5012e3'
    chain_id = 1337
    token_contract_address = "0x21107f38881CC98802EA490d967E3469F8973Dc0"
    with open("../blockchain/artifacts/compiled_code.json", "r") as file:
        compiled_sol = json.load(file)

    EventToken_bytecode = compiled_sol["contracts"]["EventToken.sol"]["EventToken"]["evm"]["bytecode"]["object"]
    EventToken_abi = compiled_sol["contracts"]["EventToken.sol"]["EventToken"]["abi"]

    EventNFT_bytecode = compiled_sol["contracts"]["EventNFT.sol"]["EventNFT"]["evm"]["bytecode"]["object"]
    EventNFT_abi = compiled_sol["contracts"]["EventNFT.sol"]["EventNFT"]["abi"]

    EventMarketplace_bytecode = compiled_sol["contracts"]["EventMarketplace.sol"]["EventMarketplace"]["evm"]["bytecode"]["object"]
    EventMarketplace_abi = compiled_sol["contracts"]["EventMarketplace.sol"]["EventMarketplace"]["abi"]

    db_path = "./TrustTix.db"
config = Config()