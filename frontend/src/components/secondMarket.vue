<template>
    <div>
      <h1>Welcome to second market</h1>

      <button @click="showForm = !showForm">I want sale</button>
  
      <div v-if="showForm">
        <h2>Please input ticket information</h2>
        <form @submit.prevent="publishTicket">
          <label for="address">event address:</label>
          <input type="text" id="address" v-model="newTicket.event_address" required>
  
          <label for="id">TicketId: </label>
          <input type="text" id="id" v-model="newTicket.ticketId" required>

          <label for="price">sale price:</label>
          <input type="number" id="price" v-model="newTicket.sale_price" required>

          <button type="submit">publish</button>
        </form>
      </div>
      <button type="button" @click="fetchTickets">fresh market</button>  
      <div>
        <table>
        <thead>
            <tr>
            <th></th>
            <th>eventAddress</th>
            <th>ticketId</th>
            <th>market</th>
            <th>saler</th>
            <th>price</th>
            <th>buy</th>
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
                            <button @click="buyOneTicket(ticket)">buy</button>
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
    showForm.value = false; // 隐藏表单
  };
  
  onMounted(fetchTickets);
  </script>
  
  <style>
  /* 你可以在这里添加一些样式 */
  </style>