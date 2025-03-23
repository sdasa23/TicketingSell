<template>
    <div>
      <h1>Welcome to first market</h1>

      <button @click="showForm = !showForm">Post new evet</button>
  
      <div v-if="showForm">
        <h2>Please input some event information</h2>
        <form @submit.prevent="publishTicket">
          <label for="name">event name:</label>
          <input type="text" id="name" v-model="newTicket.name" required>
  
          <label for="symbol">event symbol:</label>
          <input type="text" id="symbol" v-model="newTicket.symbol" required>
  
          <div v-for="(level, index) in newTicket.levels" :key="index">
            <h3>The level of ticket{{ index }}</h3>
            <label :for="`levelPrice${index}`">Price:</label>
            <input :id="`levelPrice${index}`" type="number" v-model="level.price" required>
  
            <label :for="`levelQuantity${index}`">Supply:</label>
            <input :id="`levelQuantity${index}`" type="number" v-model="level.quantity" required>
  
            <button type="button" @click="removeLevel(index)">delete level</button>
          </div>
  
          <button type="button" @click="addLevel">add level</button>
  
          <button type="submit">publish</button>
        </form>
      </div>
      <button type="button" @click="fetchTickets">fresh market</button>  
      <div>
        <table>
        <thead>
            <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Symbol</th>
            <th>address</th>
            <th>market</th>
            <th>organizer</th>
            <th>detail</th>
            </tr>
            </thead>
                <tbody>
                    <template v-for="ticket in tickets" :key="ticket[0]">
                        <tr>
                        <td>{{ ticket[0] }}</td>
                        <td>{{ ticket[1] }}</td>
                        <td>{{ ticket[2] }}</td>
                        <td>{{ ticket[3] }}</td>
                        <td>{{ ticket[4] }}</td>
                        <td>{{ ticket[5] }}</td>
                        <td>
                            <button @click="fetchDetail(ticket[0])">Request Details</button>
                        </td>
                        </tr>
                        <tr v-if="expandedId === ticket[0]">
                        <td colspan="7">
                            <div>{{ eventDetail }}</div>
                            <div>{{ eventStatus }}</div>
                            <button @click="buyOneTicket(buyLevel)">buy one</button>
                            <label for="name">event name:</label>
                            <input type="number" id="name" v-model="buyLevel" required>
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
    showForm.value = false; // 隐藏表单
  };
  
  onMounted(fetchTickets);
  </script>
  
  <style>
  /* 你可以在这里添加一些样式 */
  </style>