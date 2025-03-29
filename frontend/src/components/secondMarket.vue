<template>
    <div>
      <h1>Welcome to Second-hand Market</h1>

      <button @click="showForm = !showForm">Sell Ticket(s)</button>
  
      <div v-if="showForm">
        <h2>Please input ticket information</h2>
        <form @submit.prevent="publishTicket">
          <label for="address">Event Address:</label>
          <input type="text" id="address" v-model="newTicket.event_address" required>
  
          <label for="id">Ticket Id: </label>
          <input type="text" id="id" v-model="newTicket.ticketId" required>

          <label for="price">Sale Price:</label>
          <input type="number" id="price" v-model="newTicket.sale_price" required>

          <button type="submit">Publish</button>
        </form>
      </div>
      <button type="button" @click="fetchTickets">Refresh</button>  
      <div>
        <table>
        <thead>
            <tr>
            <th></th>
            <th>Event Address</th>
            <th>Ticket ID</th>
            <th>Seller</th>
            <th>Price</th>
            <th>Buy</th>
            </tr>
            </thead>
                <tbody>
                    <template v-for="ticket in tickets" :key="ticket[0]">
                        <tr>
                        <td>{{ ticket[0] }}</td>
                        <td>{{ ticket[1] }}</td>
                        <td>{{ ticket[3] }}</td>
                        <td>{{ ticket[4] }}</td>
                        <td>{{ ticket[5] }}</td>
                        <td>
                            <button @click="buyOneTicket(ticket)">Buy</button>
                        </td>
                        </tr>
                    </template>
                </tbody>
        </table>
    </div>
  
    </div>
  </template>
  
  <script setup>
  import axios from 'axios';
  import { ref, reactive, onMounted } from 'vue';
  import Web3 from "web3";

  const tickets = ref([]); 
  const showForm = ref(false); 

  const newTicket = reactive({
    event_address: '',
    saler_address: '',
    ticketId: 0,
    sale_price: 0
  });

  async function getCurrentUserAddress() {
  if (window.ethereum) {
    try {
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      const accounts = await window.ethereum.request({ method: 'eth_accounts' });
      if (accounts.length > 0) {
        console.log('Current user address:', accounts[0]);
        return accounts[0];
      } else {
        console.log('No accounts found');
        return null;
      }
    } catch (error) {
      console.error('Error fetching accounts:', error);
      return null;
    }
  } else {
    console.error('MetaMask is not installed');
    return null;
  }
}

    async function getAbi() {
        try {
            const response = await axios.get('http://localhost:8000/get-event-abi'); 
            return response.data;
        } catch (err) {
            console.error('get abi error:', err);
        }
    }

  async function add_NFT_into_wallet(token_address, tokenId, image){
    await window.ethereum.request({
      "method": "wallet_watchAsset",
      "params": {
        type: "ERC721",
        options: {
          address: token_address,
          tokenId : tokenId,
          image: image
        }
      }
    })
  }

  async function approveNFT(contractAddress,toAddress) {
    const contractABI = await getAbi();
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(contractABI, contractAddress);
    try {
        const userAddress = await getCurrentUserAddress();

        const transaction = await contract.methods
        .setApprovalForAll(toAddress, true)
        .send({ from: userAddress, gasPrice: 10000000 });

        console.log("Transaction sent:", transaction.transactionHash);
    } catch (error) {
        console.error("Error approving NFT:", error);
    }
}

  const fetchTickets = async () => {
    try {
      const response = await axios.get('http://localhost:8000/get-all-tickets-on-sale'); 
      tickets.value = response.data;
    } catch (error) {
      console.error('Request event information error:', error);
    }
  };
  
  const publishTicket = async () => {
    try {
        newTicket.saler_address = await getCurrentUserAddress();
        console.log(newTicket);
        const response = await axios.post('http://localhost:8000/second-market/sale', newTicket); 
        const contractAddress = newTicket.event_address;
        const marketAddress = response.data;
        console.log(contractAddress);
        console.log(marketAddress);
        await approveNFT(contractAddress,marketAddress);
        resetForm(); 
        fetchTickets();
    } catch (error) {
      console.error('Poat evenet error :', error);
    }
  };
  
    const buyOneTicket = async(ticketInf) =>{
        try{
            const user_address = await getCurrentUserAddress();
            const buyInf = {
                event_address: ticketInf[1],
                market_address: ticketInf[3],
                buyer_address: user_address,
                ticketId:  ticketInf[2]
            };
            const buyId = await axios.post('http://localhost:8000/second-market/purchase', buyInf);
            console.log(buyId.data);
            fetchTickets();
            await add_NFT_into_wallet(ticketInf[1], String(buyId.data), '')
        } catch (error) {
            console.error('Buy ticket error:', error);
        }
        
    }

  const resetForm = () => {
    newTicket.name = '';
    newTicket.levels = [
      {
        name: '',
        price: 0,
        quantity: 0
      }
    ];
    showForm.value = false; 
  };
  
  onMounted(fetchTickets);
  </script>
  
  <style>

body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #ffffff;
  min-height: 100vh;
}

.container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

button {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  font-size: 1rem;
  margin: 0.5rem;
}

button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
}

form {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  color: #ffffff;
}

input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

input:focus {
  outline: none;
  border-color: #4a90e2;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 2rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  overflow: hidden;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: bold;
}

tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.detail-card {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.detail-card div {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  h3 {
    font-size: 1.25rem;
  }

  form {
    padding: 1rem;
  }

  table {
    font-size: 0.875rem;
  }

  th, td {
    padding: 0.75rem;
  }
}
  </style>