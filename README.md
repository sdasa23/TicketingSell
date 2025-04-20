This is a group project of Bitcoin in CityUHK IS6200 

How to start?

1. start  ganache test net
ganache-cli --networkId 1 --accounts 10 --seed 1337 --port 8545 --hardfork istanbul --gasLimit  160000000000000000 --defaultBalanceEther  100000000 --gasPrice 10000

2. Migrate smart contract
cd ./blockchain/migrations/ && python3 initial_blockchain.py && cd -

3. migrate sqlite3 database
cd backend/migrations && python3 initial_db.py && cd -

4. Start backend FAST api server 
cd backend/ &&  uvicorn main:app --reload

5. Start Vue3 server(use another terminal)
cd frontend/ && npm run serve

6. Now you can visit http://localhost:8081

Project Framework

![image](https://github.com/user-attachments/assets/315258ab-3053-412e-b890-814cbe331e39)

