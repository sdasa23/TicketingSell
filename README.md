How to start?

1. start  ganache test net
ganache-cli --networkId 1 --accounts 10 --seed 1337 --port 8545 --hardfork istanbul --gasLimit  160000000000000000 --defaultBalanceEther  100000000 --gasPrice 10000

2. migrate smart contract
cd ./blockchain/migrations/ && python3 initial_blockchain.py && cd -

3. migrate sqlite3 database
cd backend/migrations && python3 initial_db.py && cd -

4. start backend FAST api server 
cd backend/ &&  uvicorn main:app --reload

5. start Vue3 server(use another terminal)
cd frontend/ && npm run serve

6. Now you can visit http://localhost:8081
