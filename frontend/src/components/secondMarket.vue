<template>
  <div class="container">
    <h1>Welcome to Second-hand Market</h1>

    <div class="center-buttons">
      <button @click="showForm = !showForm">Sell Ticket(s)</button>
      <button type="button" @click="fetchTickets">Refresh</button>
    </div>

    <div v-if="showForm">
      <h2>Please input ticket information</h2>
      <form @submit.prevent="publishTicket">
        <label for="address">Event Address:</label>
        <input type="text" id="address" v-model="newTicket.event_address" required>
  
        <label for="id">Ticket Id: </label>
        <input type="text" id="id" v-model="newTicket.ticketId" required>

        <label for="price">Sale Price:</label>
        <input type="number" id="price" v-model="newTicket.sale_price" required>

        <div class="form-actions">
          <button type="submit">Publish</button>
        </div>
      </form>
    </div>

    <div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Event Address</th>
            <th>Ticket ID</th>
            <th>Seller</th>
            <th>Price</th>
            <th>Action</th>
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
  import Swal from 'sweetalert2';

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

  async function getTokenAbi() {
        try {
            const response = await axios.get('http://localhost:8000/get-token-abi'); 
            return response.data;
        } catch (err) {
            console.error('get token abi error:', err);
        }
    }

  async function getTokenAddress() {
        try {
            const response = await axios.get('http://localhost:8000/get-token-address'); 
            return response.data["address"];
        } catch (err) {
            console.error('get token address error:', err);
        }
    }

  async function approveToken(toAddress, price) {
    const contractABI = await getTokenAbi();
    const contractAddress = await getTokenAddress();
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(contractABI, contractAddress);
    try {
        const userAddress = await getCurrentUserAddress();

        const transaction = await contract.methods
                                    .approve(toAddress, price)
                                    .send({ from: userAddress, gasPrice: 10000000 });

        console.log("Transaction sent:", transaction.transactionHash);
    } catch (error) {
        console.error("Error approving NFT:", error);
    }
  }

    const buyOneTicket = async(ticketInf) => {
      let buyId; 
      let eventAddress; 
      
      try {
          const user_address = await getCurrentUserAddress();
          eventAddress = ticketInf[1]; 
            const buyInf = {
                event_address: ticketInf[1],
                market_address: ticketInf[3],
                buyer_address: user_address,
                ticketId:  ticketInf[2]
            };
          await approveToken(ticketInf[3] , ticketInf[5]);
          const response = await axios.post('http://localhost:8000/second-market/purchase', buyInf);
          buyId = response.data;
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          const result = await Swal.fire({
              title: 'Success!',
              text: `Ticket purchased successfully! Your ticket's id is ${buyId}`,
              icon: 'success',
              showCancelButton: true,
              confirmButtonText: 'Add into MetaMask',
              cancelButtonText: 'OK',
          });

          if (result.isConfirmed) {
              console.log(eventAddress)
              console.log(buyId);
              await add_NFT_into_wallet(ticketInf[1], String(buyId), '');
          }

          await fetchTickets();
          
      } catch (error) {
          console.error('Buy ticket error:', error);
          
          let errorMessage = error.message;
          if (eventAddress && buyId) {
              errorMessage += '\n Please add the ticket manually.' +
                            '\n Address: '+ eventAddress +
                            '\nID: '+ buyId;
          } else if (eventAddress) {
              errorMessage += `\n Event Address: ${eventAddress}` +
                            `\n Purchase may not have completed.`;
          }
          
          await Swal.fire({
              title: 'Error!',
              text: errorMessage,
              icon: 'error'
          });
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
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f5f5f7; 
  color: #2c3e50; 
  min-height: 100vh;
  line-height: 1.6;
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
  font-weight: 600;
  color: #2c3e50;
  letter-spacing: -0.5px;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #3a3a3c;
}

button {
  background-color: #3a3a3c;
  color: #f5f5f7;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease-out;
  font-size: 1rem;
  margin: 0.5rem;
  font-weight: 500;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

button:hover {
  background-color: #4a4a4c;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

form {
  background-color: rgba(255, 255, 255, 0.95); 
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e5ea; 
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  color: #4a4a4c;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  font-size: 1rem;
  background-color: white;
  color: #2c3e50;
  transition: border-color 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #7a73d8; 
  box-shadow: 0 0 0 2px rgba(122, 115, 216, 0.2);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 2rem;
  background-color: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

tr:hover {
  background-color: #f8f9fa; 
}

.detail-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  margin-top: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid #f0f0f0;
}

.detail-card div {
  margin-bottom: 0.75rem;
  color: #4a4a4c;
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
    padding: 1.5rem;
  }

  table {
    font-size: 0.875rem;
  }

  th, td {
    padding: 0.875rem;
  }
  
  .container {
    padding: 1.5rem;
  }
}
.center-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem; 
  margin: 1.5rem 0;
}
</style>