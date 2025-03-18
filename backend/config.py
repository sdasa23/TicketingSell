import json

class Config:
    web3_address = 'http://127.0.0.1:8545'
    publisher_account_hash = '0xC459cc3AC9f8462Be2EF00aAD02fAc7af2e97b14'
    userKey = '0xda09f8cdec20b7c8334ce05b27e6797bef01c1ad79c59381666467552c5012e3'
    chain_id = 1337
    token_contract_address = "0x21107f38881CC98802EA490d967E3469F8973Dc0"
    with open("./artifacts/compiled_code.json", "r") as file:
        compiled_sol = json.load(file)

    FestToken_bytecode = compiled_sol["contracts"]["FestToken.sol"]["FestToken"]["evm"]["bytecode"]["object"]
    FestToken_abi = compiled_sol["contracts"]["FestToken.sol"]["FestToken"]["abi"]

    FestivalNFT_bytecode = compiled_sol["contracts"]["FestivalNFT.sol"]["FestivalNFT"]["evm"]["bytecode"]["object"]
    FestivalNFT_abi = compiled_sol["contracts"]["FestivalNFT.sol"]["FestivalNFT"]["abi"]

    FestivalMarketplace_bytecode = compiled_sol["contracts"]["FestivalMarketplace.sol"]["FestivalMarketplace"]["evm"]["bytecode"]["object"]
    FestivalMarketplace_abi = compiled_sol["contracts"]["FestivalMarketplace.sol"]["FestivalMarketplace"]["abi"]

config = Config()