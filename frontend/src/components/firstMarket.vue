<template>
  <div class="container">
    <h1>Welcome to First Market</h1>

    <button @click="showForm = !showForm">Post New Event</button>

    <div v-if="showForm">
      <h2>Please Input Event Information</h2>
      <form @submit.prevent="publishTicket">
        <label for="name">Event Name:</label>
        <input type="text" id="name" v-model="newTicket.name" required>

        <label for="symbol">Event Symbol:</label>
        <input type="text" id="symbol" v-model="newTicket.symbol" required>

        <div v-for="(level, index) in newTicket.levels" :key="index">
          <h3>Ticket Level {{ index }}</h3>
          <label :for="`levelPrice${index}`">Price:</label>
          <input :id="`levelPrice${index}`" type="number" v-model="level.price" required>

          <label :for="`levelQuantity${index}`">Supply:</label>
          <input :id="`levelQuantity${index}`" type="number" v-model="level.quantity" required>

        </div>
        <button type="button" @click="removeLevel(index)">Delete Level</button>
        <button type="button" @click="addLevel">Add Level</button>
        <button type="submit">Publish</button>
      </form>
    </div>

    <button type="button" @click="fetchTickets">Refresh Market</button>

    <div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Symbol</th>
            <th>Address</th>
            <th>Organizer</th>
            <th>Detail</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="ticket in tickets" :key="ticket[0]">
            <tr>
              <td>{{ ticket[0] }}</td>
              <td>{{ ticket[1] }}</td>
              <td>{{ ticket[2] }}</td>
              <td>{{ ticket[3] }}</td>
              <td>{{ ticket[5] }}</td>
              <td>
                <button @click="fetchDetail(ticket[0])">Request Details</button>
              </td>
            </tr>
            <tr v-if="expandedId === ticket[0]">
              <td colspan="7">
                <div class="detail-card">
                  <div>Organizer: {{ eventDetail.organizer }}</div>
                  <div>Name: {{ eventDetail.name }}</div>
                  <div>Symbol: {{ eventDetail.symbol }}</div>
                  <div>Max Ticket Level: {{ eventDetail.maxTicketLevel }}</div>
                  <div>Ticket Prices: {{ eventDetail.ticketPriceList.join(', ') }}</div>
                  <div>Ticket Supplies: {{ eventDetail.ticketSupplyList.join(', ') }}</div>
                  <div>Current Ticket IDs: {{ eventStatus.currentTicketIds }}</div>
                  <div>Tickets For Sale: {{ eventStatus.ticketsForSale.join(', ') }}</div>
                  <div>Ticket Exist Counter: {{ eventStatus.ticketExistCounterList.join(', ') }}</div>
                  <div>Ticket Sold Counter: {{ eventStatus.ticketSoldtCounterList.join(', ') }}</div>
                  <button @click="buyOneTicket(buyLevel)">Buy One</button>
                  <label for="buyLevel">Ticket Level:</label>
                  <input type="number" id="buyLevel" v-model="buyLevel" required>
                </div>
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
  const expandedId = ref(null); 
  const buyLevel = ref(null);
  const eventDetail = reactive({
    organizer: '',
    name: '',
    symbol: '',
    maxTicketLevel: 0,
    ticketPriceList: [],
    ticketSupplyList: []
  });
  const eventStatus = reactive({
    currentTicketIds: 0,
    ticketsForSale: [],
    ticketExistCounterList: [],
    ticketSoldtCounterList: []
  });
  
  const newTicket = reactive({
    name: '',
    symbol: '',
    levels: [
      {
        name: '',
        price: 0,
        quantity: 0
      }
    ]
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

  async function transformTicketForm(newTicket){
    const user_address = await getCurrentUserAddress();
    const transformed = {
    festName: newTicket.name,
    festSymbol: newTicket.symbol,
    maxTicketLevel: newTicket.levels.length -1, 
    ticketPriceList: newTicket.levels.map(level => level.price), 
    ticketSupplyList: newTicket.levels.map(level => level.quantity), 
    organiser: user_address
    };
    return transformed;
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
      const response = await axios.get('http://localhost:8000/get-all-events'); 
      tickets.value = response.data;
    } catch (error) {
      console.error('Request event information error:', error);
    }
  };
  
  const publishTicket = async () => {
    try {
        const eventInf = await transformTicketForm(newTicket);
        const response = await axios.post('http://localhost:8000/create-new-event', eventInf); 
        const contractAddress = response.data.event_address;
        const marketAddress = response.data.market_address;
        console.log(contractAddress);
        console.log(marketAddress);
        await approveNFT(contractAddress,marketAddress);
        resetForm(); 
        fetchTickets();
    } catch (error) {
      console.error('Poat evenet error :', error);
    }
  };
  
  const fetchDetail = async (id) => {
        expandedId.value = expandedId.value === id ? null : id;

        try {
            const response1 = await axios.get('http://localhost:8000/search-event-inf', {
                params: { event_address: tickets.value[id-1][3] }
            }); 
            eventDetail.value = response1.data;
            console.log(eventDetail.value)
            const response2 = await axios.get('http://localhost:8000/search-event-status', {
                params: { event_address: tickets.value[id-1][3] }
            }); 
            eventStatus.value = response2.data;
            console.log(eventStatus.value)
        
        } catch (error) {
            console.error('Request event information error:', error);
        }
    };

    const buyOneTicket = async(level) =>{
        console.log(level)
        try{
            const user_address = await getCurrentUserAddress();
            const buyInf = {
                event_address: tickets.value[expandedId.value-1][3],
                market_address: tickets.value[expandedId.value-1][4],
                buyer_address: user_address,
                buy_level:  Number(level)
            };
            const buyId = await axios.post('http://localhost:8000/first-market/purchase', buyInf);
            console.log(buyId.data);
            await add_NFT_into_wallet(tickets.value[expandedId.value-1][3], String(buyId.data), '')
        } catch (error) {
            console.error('Buy ticket error:', error);
        }
        
    }

  const addLevel = () => {
    newTicket.levels.push({
      name: '',
      price: 0,
      quantity: 0
    });
  };
  
  const removeLevel = (index) => {
    newTicket.levels.splice(index, 1);
  };
  
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